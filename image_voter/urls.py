from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('choice/', views.choice, name='choice'),
    path('results/', views.results, name='results'),
    path('vote/', views.vote, name='vote'),
]