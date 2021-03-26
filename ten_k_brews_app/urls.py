from django.urls import path
from django.contrib.auth import views as auth_views
from .views import browse_views, detail_views, user_views

urlpatterns = [
    path('', browse_views.home, name='home'),

    # browse urls
    path('browse/<str:type_filter>', browse_views.browse, name='browse'),
    path('search/', browse_views.search, name='search'),
    path('search/by_location', browse_views.search_by_location, name='search_by_location'),

    # detail page urls
    path('establishment/<int:establishment_pk>', detail_views.establishment_detail, name='establishment_detail'),
    path('establishment/set_visited/<int:establishment_pk>/<str:visited>', detail_views.set_visited, name='set_visited'),
    path('drink/<int:drink_pk>', detail_views.drink_detail, name='drink_detail'),
    path('drink/set_drunk/<int:drink_pk>/<str:drunk>', detail_views.set_drunk, name='set_drunk'),

    # form urls
    path('new_drink/<int:establishment_pk>', detail_views.new_drink_form, name='new_drink_form'),
    path('search/by_location/form', browse_views.location_search_form, name='location_search_form'),

    # account urls
    path('user/profile/<str:username>/', user_views.user_profile, name='user_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account_pages/login.html'), name='login'),
    path('accounts/logout/', user_views.logout_user, name='logout'),
    path('register/', user_views.register, name='register')
]
