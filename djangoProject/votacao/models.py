from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


# Questao:
# texto da questão e data de publicação
class Questao(models.Model):
    questao_texto = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.questao_texto

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)
# Opcao:
# texto da opção e número de votos
# chave estrangeira muitos-para-um pois uma Questao pode ter várias instancias de Opcao
class Opcao(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto

##
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=50)
    numero_votos = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
