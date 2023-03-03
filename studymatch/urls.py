from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey, name='survey'),
    path('thanks/', views.survey_thanks, name='survey_thanks'),
]
