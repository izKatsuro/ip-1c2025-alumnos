# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    #Buscamos las imagenes (cards) en el servicio
    images = services.getAllImages();
    favourite_list = services.getAllFavourites(request)
    #creamos un listado de ids de favoritos para facilitar la comparacion entre cards. 
    favourite_ids = [fav.id for fav in favourite_list]
    # Agregamos el listado de los id favoritos
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourite_ids': favourite_ids })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        #Buscamos las imagenes (cards) en el servicio segun el filtro colocado
        images = services.filterByCharacter(name)
        #Buscamos los favoritos en el servicio
        favourite_list = services.getAllFavourites(request)
        #Creamos un listado de ids de favoritos para que sea mas facil comparar entre cards.
        favourite_ids = [fav.id for fav in favourite_list]
        # Agregamos el listado de los id favoritos
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourite_ids': favourite_ids })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourites = services.getAllFavourites(request)
    #print(favourites)
    return render(request, 'favourites.html', {
        'favourite_list': favourites
    })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    images = services.getAllImages(); 
    favourite_list = services.getAllFavourites(request)
    favourite_ids = [fav.id for fav in favourite_list]

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list , 'favourite_ids': favourite_ids})

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
    favourites = services.getAllFavourites(request)    
    return render(request, 'favourites.html', {
        'favourite_list': favourites
    })

@login_required
def exit(request):
    logout(request)
    return redirect('home')