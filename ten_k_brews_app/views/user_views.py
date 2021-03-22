from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import Establishment, Drink, UserData, percent_visited
from ..forms import UserRegistrationForm, EstablishmentSearchForm
from ..constants import MINNESOTA_COORDINATES, WIDE_ZOOM_LEVEL
import environ

search_form = EstablishmentSearchForm   # for search bar used in title_bar.html

# read environment variables -- requires a .env file in the views/ directory
env = environ.Env()
environ.Env.read_env()
mapbox_token = env('MAPBOX_TOKEN')


def user_profile(request, username):
    user = User.objects.get_by_natural_key(username)
    user_data = UserData.objects.get(user=user)

    places_visited = user_data.user_establishments.all().order_by('name')
    drinks_added = Drink.objects.filter(user=user).order_by('name')
    drinks_drunk = user_data.user_drinks.all().order_by('name')

    visited_percents = {
        'all': f'{percent_visited(user):.0f}',
        'breweries': f'{percent_visited(user, Establishment.BREWERY):.0f}',
        'wineries': f'{percent_visited(user, Establishment.WINERY):.0f}',
        'distilleries': f'{percent_visited(user, Establishment.DISTILLERY):.0f}',
        'cideries': f'{percent_visited(user, Establishment.CIDERY):.0f}'
    }

    return render(request, 'account_pages/user_profile.html',
                  {'user': user, 'search_form': search_form, 'places_visited': places_visited,
                   'visited_percents': visited_percents, 'drinks_drunk': drinks_drunk, 'drinks_added': drinks_added,
                   'focus_lat': MINNESOTA_COORDINATES[0], 'focus_lon': MINNESOTA_COORDINATES[1],
                   'zoom_level': WIDE_ZOOM_LEVEL, 'map_establishments': places_visited, 'mapbox_token': mapbox_token})


def register(request):
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])

            # make and save data object for the user
            user_data = UserData(user=user)
            user_data.save()

            if user:
                login(request, user)
                return redirect('user_profile', username=user.username)
            else:
                messages.add_message(request, messages.ERROR, 'Unable to log in new user')
        else:
            messages.add_message(request, messages.INFO, 'Please check the data you entered')
            # include invalid form with error messages added to it. Error messages will be displayed by the template.
            return render(request, 'account_pages/register.html',
                          {'form': registration_form, 'search_form': search_form})

    registration_form = UserRegistrationForm()
    return render(request, 'account_pages/register.html',
                  {'registration_form': registration_form, 'search_form': search_form})


def logout_user(request):
    username = request.user.username
    logout(request)
    return render(request, 'account_pages/logout.html', {'username': username, 'search_form': search_form})
