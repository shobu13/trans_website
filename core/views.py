from django.shortcuts import render

from cadre_de_vie.models import Newpaper


def core_home(request):
    last_new_hall: Newpaper = Newpaper.objects.filter(est_mairie=True).order_by('date').reverse().first()
    return render(request, 'core/home.html', locals())

