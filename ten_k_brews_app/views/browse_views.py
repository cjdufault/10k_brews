from django.shortcuts import render, redirect
from ..forms import EstablishmentSearchForm, EstablishmentSearchByLocationForm
from ..models import Establishment
from ..constants import MINNESOTA_COORDINATES, WIDE_ZOOM_LEVEL
from ten_k_brews_app.utilities.detect_mobile import is_mobile
from ten_k_brews_app.utilities.osm_geolocator import get_coordinates
from ten_k_brews_app.utilities.geo_search import get_closest_establishments
import environ

# read environment variables -- requires a .env file in the views/ directory
env = environ.Env()
environ.Env.read_env()
mapbox_token = env('MAPBOX_TOKEN')


def home(request):
    establishments = Establishment.objects.all()
    return render(request, 'browse_pages/home.html', {'search_form': EstablishmentSearchForm,
                                                      'focus_lat': MINNESOTA_COORDINATES[0],
                                                      'focus_lon': MINNESOTA_COORDINATES[1],
                                                      'zoom_level': WIDE_ZOOM_LEVEL, 'mobile_zoom': WIDE_ZOOM_LEVEL - 1,
                                                      'map_establishments': establishments,
                                                      'mapbox_token': mapbox_token, 'mobile': is_mobile(request)})


def browse(request, type_filter):
    # get establishments to list based on user selection
    if type_filter == 'all':
        list_title = 'All:'
        establishments = Establishment.objects.all().order_by('name')
    elif type_filter == 'breweries':
        list_title = 'Breweries:'
        establishments = Establishment.objects.filter(type=Establishment.BREWERY).order_by('name')
    elif type_filter == 'wineries':
        list_title = 'Wineries:'
        establishments = Establishment.objects.filter(type=Establishment.WINERY).order_by('name')
    elif type_filter == 'distilleries':
        list_title = 'Distilleries:'
        establishments = Establishment.objects.filter(type=Establishment.DISTILLERY).order_by('name')
    elif type_filter == 'cideries':
        list_title = 'Cideries:'
        establishments = Establishment.objects.filter(type=Establishment.CIDERY).order_by('name')
    else:
        return redirect('home')     # redirect home if type_filter is something unexpected

    return render(request, 'browse_pages/list.html', {'establishments': establishments, 'list_title': list_title,
                                                      'search_form': EstablishmentSearchForm,
                                                      'mobile': is_mobile(request)})


def search(request):
    search_term = request.GET.get('search_term')

    if search_term:     # check that search term is entered
        list_title = f'Results for "{search_term}":'
        establishments = Establishment.objects.filter(name__icontains=search_term).order_by('name')
        return render(request, 'browse_pages/list.html', {'establishments': establishments, 'list_title': list_title,
                                                          'search_form': EstablishmentSearchForm,
                                                          'mobile': is_mobile(request)})

    return redirect('browse', type_filter='all')     # show /browse/all if no search term provided


def location_search_form(request):
    return render(request, 'form_pages/search_by_location.html',
                  {'search_form': EstablishmentSearchForm, 'location_search_form': EstablishmentSearchByLocationForm,
                   'mobile': is_mobile(request)})


def search_by_location(request):
    location = request.GET.get('location')
    num_results = int(request.GET.get('num_results'))

    if location:
        coordinates = get_coordinates(location)
        if coordinates:
            list_title = f'{num_results} results closest to "{location}"'
            closest = get_closest_establishments(coordinates, num_results)
            return render(request, 'browse_pages/list.html',
                          {'establishments': closest, 'list_title': list_title,
                           'search_form': EstablishmentSearchForm,
                           'mobile': is_mobile(request)})

    return redirect('browse', type_filter='all')  # show /browse/all if no location provided or no coordinates found
