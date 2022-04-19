from django.http import HttpResponse
from django.shortcuts import render

from django import forms

def index(request):
    if request.method == 'POST':
        ctx = {
            'pegaID': None,
            'pegaApiID': None,
            'checker': None,
            'pegaApiContent': None
        }
        if request.POST.get('PegaID'):
            requestPegaID = request.POST.get('PegaID')

            ctx['pegaID'] = requestPegaID
            ctx['pegaApiID'] = f"https://api.pegaxy.io/race/history/pega/{requestPegaID}"
            ctx['checker'] = 0

            return render(request, 'directories/pegachart.html', ctx)
        elif request.POST.get('PegaApiContent'):
            requestPegaApiContent = request.POST.get('PegaApiContent')

            ctx['pegaApiContent'] = requestPegaApiContent

            print(ctx['pegaApiContent'])
        
            return render(request, 'directories/pegachart.html', ctx)
    else:
        return render(request, 'directories/pegachart.html')