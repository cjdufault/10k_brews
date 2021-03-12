from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Establishment(models.Model):

    # choices for establishment types
    BREWERY = 'Brewery'
    WINERY = 'Winery'
    DISTILLERY = 'Distillery'
    CIDERY = 'Cidery'
    OTHER = 'Other'

    ESTABLISHMENT_TYPES = (
        (BREWERY, 'Brewery'),   # (actual value, human readable value)
        (WINERY, 'Winery'),
        (DISTILLERY, 'Distillery'),
        (CIDERY, 'Cidery'),
        (OTHER, 'Other')
    )

    # descriptive variables
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=10000, blank=True)
    type = models.CharField(max_length=10, choices=ESTABLISHMENT_TYPES, blank=False)

    # location variables
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip_code = models.CharField(max_length=5, blank=False)

    def __str__(self):
        return f'{self.name} -- {self.type} -- {self.city}'


class Drink(models.Model):

    # choices for drink types
    BEER = 'Beer'
    WINE = 'Wine'
    LIQUOR = 'Liquor'
    CIDER = 'Cider'
    OTHER = 'Other'

    DRINK_TYPES = (
        (BEER, 'Beer'),
        (WINE, 'Wine'),
        (LIQUOR, 'Liquor'),
        (CIDER, 'Cider'),
        (OTHER, 'Other')
    )

    name = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=10, choices=DRINK_TYPES, blank=False)
    style = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=10000, blank=True)

    # foreign keys
    # what establishment makes this drink? drinks deleted when their establishment has been deleted due to CASCADE
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE)

    # user that uploaded this drink; will be set to None if User is deleted
    user = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=True)

    def __str__(self):
        string = f'{self.name} -- {self.type}'

        if self.style:
            string += f' -- {self.style}'

        return string


class UserData(models.Model):
    # what user the data is for
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, unique=True)

    user_drinks = models.ManyToManyField(Drink, blank=True)                     # drinks the user has had
    user_establishments = models.ManyToManyField(Establishment, blank=True)     # places the user has been

    def __str__(self):
        return f'{self.user} data'
