from django.http import HttpResponse
from django.shortcuts import render

from django import forms

def index(request):
    if request.method == 'POST':
        pegaID = request.POST['PegaID']

        print(pegaID)

    return render(request, 'directories/pegachart.html')