from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Questao, Opcao, Aluno
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import logout
from django.shortcuts import render, redirect


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


# ...
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
        return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')


def gravaquestao(request):
    try:
        input = request.POST['questao']
        questao = Questao(questao_texto=input, pub_data=timezone.now())
        questao.save()
    except:
        return render(request, 'votacao/criarquestao.html', {'error_message': "Erro ao criar questão", })
    return HttpResponseRedirect(reverse('votacao:index'))


def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


def gravaopcao(request, questao_id):
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


##

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


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:loginmenu'))


def personalinfo(request):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login_error.html')
    aluno = get_object_or_404(Aluno, user_id=request.user.id)
    return render(request, 'votacao/personalinfo.html', {'aluno': aluno})




