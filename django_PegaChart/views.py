from django.http import HttpResponse
from django.shortcuts import render

from django import forms

def index(request):
    if request.method == 'POST':
        pegaID = request.POST['PegaID']

        print(f"https://api.pegaxy.io/race/history/pega/{pegaID}")

    return render(request, 'directories/pegachart.html')