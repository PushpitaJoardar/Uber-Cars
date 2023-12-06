from django.urls import path

from . import views

app_name = 'uber'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('userSignUp/', views.userSignUp, name='userSignUp'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('driverSignUp/', views.driverSignUp, name='driverSignUp'),
    path('driverLogin/', views.driverLogin, name='driverLogin'),
    path('userHomePage/<int:user_id>/', views.userHomePage, name='userHomePage'),
    path('driverHomePage/<int:driver_id>/', views.driverHomePage, name='driverHomePage'),
    path('newRequest/<int:user_id>/', views.newRequest, name='newRequest'),
    path('acceptRequest/<int:request_id>/<int:driver_id>/', views.acceptRequest, name="acceptRequest"),
]