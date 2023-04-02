from django.urls import path
from . import views

app_name = 'votacao'
urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),
    # ex votacao/criarquestao
    path("criarquestao", views.criarquestao, name='criarquestao'),
    # ex votacao/1/criarquestao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),
    # ex: votacao/register
    path('register/', views.register, name='register'),
    # ex: votacao/login
    path('login/', views.login, name='login'),
    # ex: votacao/logout
    path('logout/', views.logout, name='logout'),
    # ex: votacao/personalinfo
    path('personalinfo/', views.personalinfo, name='personalinfo'),
    # ex votacao/3/excluirquestao
    path('<int:questao_id>/excluirquestao', views.excluirquestao, name='excluirquestao'),
    # ex votacao/3/1/excluiropcao
    path('<int:questao_id>/<int:opcao_id>/exluiropcao', views.excluiropcao, name='excluiropcao'),



]

