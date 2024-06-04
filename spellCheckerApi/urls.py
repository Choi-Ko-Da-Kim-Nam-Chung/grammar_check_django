from django.urls import path
from . import views

urlpatterns = [
    path('busan', views.busanSpellChecker),
    path('jobkorea', views.jobKoreaSpellChecker),
    path('incruit', views.incruitSpellChecker),
    path('hello', views.hello)
]
