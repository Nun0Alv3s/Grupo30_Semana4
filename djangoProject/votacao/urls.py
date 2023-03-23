from django.urls import path
from . import views

app_name = 'votacao'
urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),
    # ex votacao/criarquestao
    path("criarquestao", views.criarquestao, name='criarquestao'),
    # ex votacao/gravaquestao
    path("gravaquestao", views.gravaquestao, name='gravaquestao'),
    # ex votacao/1/criarquestao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),
    # ex votacao/3/gravaopcao
    path('<int:questao_id>/gravaopcao', views.gravaopcao, name='gravaopcao'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe,name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto,name='voto'),
    # ex: votacao/register
    path('register/', views.register, name='register'),
    # ex: votacao/login
    path('login/', views.login, name='login'),
    # ex: votacao/personalinfo
    path('personalinfo/', views.personalinfo, name='personalinfo')

]

