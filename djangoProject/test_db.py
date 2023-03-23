from votacao.models import Questao, Opcao
from django.db.models import Sum, Max

votos_totais = Opcao.objects.aggregate(Sum('votos'))

print(f"O número total de votos foi: {votos_totais}\n")

questoes = Questao.objects.all()

for q in questoes:
    opcao_mais_votada = Opcao.objects.filter(questao_id=q.id).aggregate(Max('votos'))
    print(f"Questão: {q.questao_texto}\nOpção mais votada: {opcao_mais_votada['votos__max']}\n\n")
