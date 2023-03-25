from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Questao, Opcao, Aluno
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render


VOTOS_MAXIMOS = 40


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    user = request.user
    if user.is_authenticated and not user.is_superuser:
        aluno = get_object_or_404(Aluno, user_id=user.id)
        context.update({"aluno": aluno})
    return render(request, 'votacao/index.html', context)


# ...
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def voto(request, questao_id):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        if not request.user.is_superuser:
            aluno = get_object_or_404(Aluno, user_id=request.user.id)
            if aluno.numero_votos < VOTOS_MAXIMOS:
                aluno.numero_votos += 1
                aluno.save()
            else:
                return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': f"Utilizador {request.user} atingiu o máximo de votos", })
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def criarquestao(request):
    if request.user.is_superuser:
        return render(request, 'votacao/criarquestao.html')
    raise PermissionDenied()


def gravaquestao(request):
    if request.user.is_superuser:
        try:
            input = request.POST['questao']
            questao = Questao(questao_texto=input, pub_data=timezone.now())
            questao.save()
        except:
            return render(request, 'votacao/criarquestao.html', {'error_message': "Erro ao criar questão", })
        return HttpResponseRedirect(reverse('votacao:index'))
    raise PermissionDenied()


def criaropcao(request, questao_id):
    if request.user.is_superuser:
        questao = get_object_or_404(Questao, pk=questao_id)
        return render(request, 'votacao/criaropcao.html', {'questao': questao})
    raise PermissionDenied()


def gravaopcao(request, questao_id):
    if request.user.is_superuser:
        questao = get_object_or_404(Questao, pk=questao_id)
        try:
            opcao = request.POST['opcao']
        except:
            # Apresenta de novo o form para votar
            return render(request, 'votacao/criaropcao.html',
                          {'questao': questao, 'error_message': "Erro ao criar opçao", })
        else:
            questao.opcao_set.create(opcao_texto=opcao, votos=0)
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
    raise PermissionDenied()


def register(request):
    if request.method == 'POST':
        try:
            username = str(request.POST['username'])
            email = str(request.POST['email'])
            curso = str(request.POST['curso'])
            password = str(request.POST['password'])
            u = User.objects.create_user(username=username, email=email, password=password)
            a = Aluno(user=u, curso=curso)
            a.save()

        except:
            return render(request, 'votacao/register.html', {'error_message': "Erro ao registar novo utilizador"})
        return HttpResponseRedirect(reverse('votacao:login'))
    return render(request, 'votacao/register.html')


def login(request):
    if request.method == 'POST':
        try:
            username = str(request.POST['username'])
            password = str(request.POST['password'])
            u = authenticate(request, username=username, password=password)
            if u is not None:
                django_login(request, u)
                return HttpResponseRedirect(reverse('votacao:index'))
            else:
                return render(request, 'votacao/login.html', {'error_message': "Login failed"})
        except Exception as e:
            print(str(e))
            return render(request, 'votacao/login.html', {'error_message': "Erro ao efetuar o login"})
    return render(request, 'votacao/login.html')


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))


def personalinfo(request):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
    aluno = get_object_or_404(Aluno, user_id=request.user.id)
    return render(request, 'votacao/personalinfo.html', {'aluno': aluno})


def excluirquestao(request, questao_id):
    if request.user.is_superuser:
        questao = get_object_or_404(Questao, pk=questao_id)
        try:
            questao.delete()
        except:
            return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Erro ao excluir questão", })
        else:
            return HttpResponseRedirect(reverse('votacao:index'))
    raise PermissionDenied()


def excluiropcao(request, questao_id, opcao_id):
    if request.user.is_superuser:
        questao = get_object_or_404(Questao, pk=questao_id)
        opcao = get_object_or_404(Opcao, pk=opcao_id)
        try:
            opcao.delete()
        except:
            return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Erro ao excluir opção", })
        else:
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
    raise PermissionDenied()




