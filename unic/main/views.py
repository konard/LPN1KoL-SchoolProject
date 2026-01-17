from django.http import FileResponse
from django.shortcuts import render



def main(request):
    return render(request, 'main.html')


def favicon(request):
    return FileResponse(open('static/imgs/logo.svg', 'rb'))
