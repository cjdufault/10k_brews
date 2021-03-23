from django.shortcuts import get_object_or_404
from .models import Establishment, UserData


# returns the % of establishments of a given type (or all, if no type) that a user has visited
def percent_visited(user, establishment_type=None):
    user_data = get_object_or_404(UserData, user=user)

    if not user_data:   # returns None if userdata not found for user
        return None

    if not establishment_type:  # get all if no establishment type
        total = Establishment.objects.count()
        visited = user_data.user_establishments.count()
    else:
        total = Establishment.objects.filter(type=establishment_type).count()
        visited = user_data.user_establishments.filter(type=establishment_type).count()

    return (visited / total) * 100
