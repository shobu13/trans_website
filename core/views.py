from django.shortcuts import render

from cadre_de_vie.models import New


def core_home(request):
    last_new_hall: New = New.objects.filter(est_mairie=True).order_by('date').reverse().first()
    return render(request, 'core/home.html', locals())

