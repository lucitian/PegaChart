from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from .api.data_helpers import *
from .api.pega import Pega

#pega_id = None

def index(request):
    if request.method == 'POST':
        global pega_id
        ctx = {
            'pegaID': None,
            'pegaApiID': None,
            'checker': None,
            'percent_share': None,
            'pegaApiContent': None
        }
        if request.POST.get('PegaID'):
            requestPegaID = request.POST.get('PegaID')
            #pega_id = requestPegaID

            ctx['pegaID'] = requestPegaID
            ctx['pegaApiID'] = f"https://api.pegaxy.io/race/history/pega/{requestPegaID}"
            ctx['checker'] = 0

            return render(request, 'directories/pegachart.html', ctx)
        elif request.POST.get('PegaApiContent'):
            requestPercentShare = request.POST.get('PegaShare')
            requestPegaApiContent = request.POST.get('PegaApiContent')

            ctx['percent_share'] = requestPercentShare
            ctx['pegaApiContent'] = requestPegaApiContent

            print(Pega(pega_id).race_history)
            print(ctx)
        
            return render(request, 'directories/pegachart.html', ctx)
    else:
        return render(request, 'directories/pegachart.html')