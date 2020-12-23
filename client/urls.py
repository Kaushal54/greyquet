from django.urls import path,include
from . import views

app_name = 'client'

urlpatterns = [
    path('signin/',views.sign_in,name='sign_in'),
    path('signout/',views.sign_out,name='sign_out'),
    path('',views.hello,name='hello'),
]