from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Establishment, Drink, UserData
from ..forms import EstablishmentSearchForm, NewDrinkForm
from ..constants import LOCATION_ZOOM_LEVEL
from ten_k_brews_app.utilities.detect_mobile import is_mobile
import environ

# read environment variables -- requires a .env file in the views/ directory
env = environ.Env()
environ.Env.read_env()
mapbox_token = env('MAPBOX_TOKEN')


def establishment_detail(request, establishment_pk):
    establishment = get_object_or_404(Establishment, pk=establishment_pk)
    authenticated = request.user.is_authenticated

    if authenticated:
        user_data = UserData.objects.get(user=request.user)
        visited = establishment in user_data.user_establishments.all()
    else:
        visited = None

    drinks = Drink.objects.filter(establishment=establishment).order_by('name')

    return render(request, 'detail_pages/establishment.html',
                  {'establishment': establishment, 'drinks': drinks, 'search_form': EstablishmentSearchForm,
                   'visited': visited, 'authenticated': authenticated, 'mapbox_token': mapbox_token,
                   'focus_lat': establishment.latitude, 'focus_lon': establishment.longitude,
                   'zoom_level': LOCATION_ZOOM_LEVEL, 'mobile_zoom': LOCATION_ZOOM_LEVEL - 1,
                   'map_establishments': [establishment], 'mobile': is_mobile(request)})


# adds the establishment to the list of the establishments the user has visited
@login_required
def set_visited(request, establishment_pk, visited):
    establishment = get_object_or_404(Establishment, pk=establishment_pk)
    user_data = UserData.objects.get(user=request.user)

    currently_visited = establishment in user_data.user_establishments.all()

    if visited == 'True' and not currently_visited:     # mark visited True if not currently True
        user_data.user_establishments.add(establishment)
    elif visited == 'False' and currently_visited:      # mark visited False if not currently False
        user_data.user_establishments.remove(establishment)

    return redirect('establishment_detail', establishment_pk=establishment_pk)


def drink_detail(request, drink_pk):
    drink = get_object_or_404(Drink, pk=drink_pk)
    authenticated = request.user.is_authenticated

    if authenticated:
        user_data = UserData.objects.get(user=request.user)
        drunk = drink in user_data.user_drinks.all()
    else:
        drunk = None

    return render(request, 'detail_pages/drink.html',
                  {'drink': drink, 'search_form': EstablishmentSearchForm, 'drunk': drunk,
                   'authenticated': authenticated, 'mobile': is_mobile(request)})


# adds the drink to the list of the drinks the user has drunk
@login_required
def set_drunk(request, drink_pk, drunk):
    drink = get_object_or_404(Drink, pk=drink_pk)
    user_data = UserData.objects.get(user=request.user)

    currently_drunk = drink in user_data.user_drinks.all()  # if only

    if drunk == 'True' and not currently_drunk:       # mark visited True if not currently True
        user_data.user_drinks.add(drink)
    elif drunk == 'False' and currently_drunk:     # mark visited False if not currently False
        user_data.user_drinks.remove(drink)

    return redirect('drink_detail', drink_pk=drink_pk)


@login_required
def new_drink_form(request, establishment_pk):
    establishment = get_object_or_404(Establishment, pk=establishment_pk)

    # receive new Drink data from form
    if request.method == 'POST':
        drink_form = NewDrinkForm(request.POST, request.FILES)

        if drink_form.is_valid():
            drink = drink_form.save(commit=False)
            drink.establishment = establishment
            drink.user = request.user
            drink.save()
            return redirect('drink_detail', drink_pk=drink.pk)

    # show form to receive input
    else:
        drink_form = NewDrinkForm()

    return render(request, 'form_pages/new_drink.html',
                  {'drink_form': drink_form, 'establishment': establishment,
                   'search_form': EstablishmentSearchForm, 'mobile': is_mobile(request)})
