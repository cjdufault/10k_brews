"""ten_k_brews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # browse urls
    path('browse/<str:type_filter>', views.browse, name='browse'),
    path('search/', views.search, name='search'),

    # detail page urls
    path('establishment/<int:establishment_pk>', views.establishment_detail, name='establishment_detail'),
    path('establishment/set_visited/<int:establishment_pk>/<str:visited>', views.set_visited, name='set_visited'),
    path('drink/<int:drink_pk>', views.drink_detail, name='drink_detail'),

    # form urls
    path('new_drink/<int:establishment_pk>', views.new_drink_form, name='new_drink_form'),

    # account urls
    path('user/profile/<str:username>/', views.user_profile, name='user_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account_pages/login.html'), name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register')
]
