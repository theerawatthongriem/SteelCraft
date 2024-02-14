from members.models import *

def favorite_count(request):
    if request.user.is_authenticated:
        favorite_count = Favorite.objects.filter(user=request.user).count()
    else:
        favorite_count = [0]
    return favorite_count