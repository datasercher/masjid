from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('check-balance/', views.check_balance, name='check_balance'),
    path('create-person-list/', views.create_person_list, name='create_person_list'),
    path('view-person-list/', views.view_person_list, name='view_person_list'),
    path('deposit-sellery/', views.deposit_sellery, name='deposit_sellery'),
    path('upload-person-list/', views.upload_person_list, name='upload_person_list'),




]
