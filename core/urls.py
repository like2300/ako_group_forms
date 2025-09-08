from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('formulaire/', views.formulaire, name='formulaire'),  
    path('configuration' , views.confige ,name="config"),
    path('exportcsv' , views.exportcsv ,name="exportcsv"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
