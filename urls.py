from django.urls import path

from . import views

app_name = 'coupon'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sn>/', views.indexsn, name='indexsn'),
    path('verify/', views.verify, name='verify'),
    path('order/', views.order, name='order'),
    ]
