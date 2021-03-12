from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Establishment, Drink, UserData
from .forms import EstablishmentSearchForm, NewDrinkForm, UserRegistrationForm

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

    if search_term:     # check that search term is entered
        establishments = Establishment.objects.filter(name__icontains=search_term).order_by('name')
        return render(request, 'browse_pages/list.html', {'establishments': establishments, 'search_form': search_form})

    return redirect('browse', type_filter='all')     # show /browse/all if no search term provided


def establishment_detail(request, establishment_pk):
    establishment = get_object_or_404(Establishment, pk=establishment_pk)
    user_data = UserData.objects.get(user=request.user)

    visited = establishment in user_data.user_establishments.all()
    drinks = Drink.objects.filter(establishment=establishment).order_by('name')

    return render(request, 'detail_pages/establishment.html',
                  {'establishment': establishment, 'drinks': drinks,
                   'search_form': search_form, 'visited': visited})


# adds the establishment to the list of the establishments the user has visited
@login_required
def set_visited(request, establishment_pk, visited):
    establishment = get_object_or_404(Establishment, pk=establishment_pk)
    user_data = UserData.objects.get(user=request.user)

    currently_visited = establishment in user_data.user_establishments.all()

    if visited == 'True' and not currently_visited:       # mark visited True if not currently True
        user_data.user_establishments.add(establishment)
    elif visited == 'False' and currently_visited:     # mark visited False if not currently False
        user_data.user_establishments.remove(establishment)

    return redirect('establishment_detail', establishment_pk=establishment_pk)


def drink_detail(request, drink_pk):
    drink = get_object_or_404(Drink, pk=drink_pk)
    user_data = UserData.objects.get(user=request.user)

    drunk = drink in user_data.user_drinks.all()

    return render(request, 'detail_pages/drink.html', {'drink': drink, 'search_form': search_form, 'drunk': drunk})


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
                  {'drink_form': drink_form, 'establishment': establishment, 'search_form': search_form})


def user_profile(request, username):
    user = User.objects.get_by_natural_key(username)
    user_data = UserData.objects.get(user=user)

    places_visited = user_data.user_establishments.all().order_by('name')
    drinks_added = Drink.objects.filter(user=user).order_by('name')
    drinks_drunk = user_data.user_drinks.all().order_by('name')

    return render(request, 'account_pages/user_profile.html',
                  {'user': user, 'search_form': search_form,
                   'places_visited': places_visited, 'drinks_drunk': drinks_drunk, 'drinks_added': drinks_added})


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
