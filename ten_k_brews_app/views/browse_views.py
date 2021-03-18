from django.shortcuts import render, redirect
from ..forms import EstablishmentSearchForm
from ..models import Establishment

search_form = EstablishmentSearchForm   # for search bar used in title_bar.html


def home(request):
    return render(request, 'browse_pages/home.html', {'search_form': search_form})


def browse(request, type_filter):
    # get establishments to list based on user selection
    if type_filter == 'all':
        establishments = Establishment.objects.all().order_by('name')
    elif type_filter == 'breweries':
        establishments = Establishment.objects.filter(type=Establishment.BREWERY).order_by('name')
    elif type_filter == 'wineries':
        establishments = Establishment.objects.filter(type=Establishment.WINERY).order_by('name')
    elif type_filter == 'distilleries':
        establishments = Establishment.objects.filter(type=Establishment.DISTILLERY).order_by('name')
    elif type_filter == 'cideries':
        establishments = Establishment.objects.filter(type=Establishment.CIDERY).order_by('name')
    else:
        return redirect('home')     # redirect home if type_filter is something unexpected

    return render(request, 'browse_pages/list.html', {'establishments': establishments, 'search_form': search_form})


def search(request):
    search_term = request.GET.get('search_term')

    if search_term:     # check that search term is entered
        establishments = Establishment.objects.filter(name__icontains=search_term).order_by('name')
        return render(request, 'browse_pages/list.html', {'establishments': establishments, 'search_form': search_form})

    return redirect('browse', type_filter='all')     # show /browse/all if no search term provided
