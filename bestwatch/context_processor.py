from bestwatch.models import Genres

def explore_menu(request):
    all_genres = Genres.objects.all()
    return {'all_genres' : all_genres }

