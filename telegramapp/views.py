from django.http import HttpResponse
from django.shortcuts import render

from .models import Coin


def teleg(request):
    all_dados = Coin.objects.all()
    return render(request, 'teleg.html', {'all_dados': all_dados})
    # return HttpResponse("RODANDO NORMAL")