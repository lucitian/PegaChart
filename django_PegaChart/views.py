from django.http import HttpResponse
from django.shortcuts import render

from django import forms

def index(request):
    ctx = {
        'pegaID': None,
        'pegaApiID': None,
        'checker': None
    }

    if request.method == 'POST':
        requestPegaID = request.POST['PegaID']

        ctx['pegaID'] = requestPegaID
        ctx['pegaApiID'] = f"https://api.pegaxy.io/race/history/pega/{requestPegaID}"
        ctx['checker'] = 0
        
        return render(request, 'directories/pegachart.html', ctx)
    else:
        return render(request, 'directories/pegachart.html')