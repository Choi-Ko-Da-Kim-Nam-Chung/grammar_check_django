from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('busan', views.busanSpellChecker),
    path('jobkorea', views.jobKoreaSpellChecker),
    path('incruit', views.incruitSpellChecker)
]
