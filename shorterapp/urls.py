from django.urls import path
from shorterapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shortened_url/', views.shortened_url, name='shortened_url'),
    path('<str:shortened_part>', views.redirect_url_view, name='redirect'),
]