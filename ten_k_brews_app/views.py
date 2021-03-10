from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Establishment, Drink
from .forms import EstablishmentSearchForm, NewDrinkForm, UserRegistrationForm, UserHasVisitedForm

search_form = EstablishmentSearchForm   # for search bar used in base.html


def home(request):
    return render(request, 'home.html', {'search_form': search_form})


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

    if search_term:
        establishments = Establishment.objects.filter(name__icontains=search_term).order_by('name')
        return render(request, 'browse_pages/list.html', {'establishments': establishments, 'search_form': search_form})

    return redirect('browse', type_filter='all')     # show /browse/all if no search term provided


def establishment_detail(request, establishment_pk):
    establishment = get_object_or_404(Establishment, pk=establishment_pk)

    visited_form = UserHasVisitedForm
    drinks = Drink.objects.filter(establishment=establishment).order_by('name')

    if establishment.users_visited.contains(request.user):
        user_has_visited = True
    else:
        user_has_visited = False

    return render(request, 'detail_pages/establishment.html',
                  {'establishment': establishment, 'drinks': drinks,
                   'search_form': search_form, 'visited_form': visited_form, 'user_has_visited': user_has_visited})


@login_required
def set_visited(request, establishment_pk, visited):
    redirect('establishment_detail', establishment_pk=establishment_pk)


def drink_detail(request, drink_pk):
    drink = get_object_or_404(Drink, pk=drink_pk)
    return render(request, 'detail_pages/drink.html', {'drink': drink, 'search_form': search_form})


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
                  {'drink_form': drink_form, 'establishment': establishment, 'search_form': search_form})


def user_profile(request, username):
    user = User.objects.get_by_natural_key(username)
    places_visited = Establishment.objects.filter(users_visited__username=user.username).order_by('name')
    drinks_added = Drink.objects.filter(user=user)
    return render(request, 'account_pages/user_profile.html',
                  {'user': user, 'search_form': search_form,
                   'places_visited': places_visited, 'drinks_added': drinks_added})


def register(request):
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                login(request, user)
                return redirect('my_user_profile')
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
