import json
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



def main(request):
    return render(request, 'main.html')


def favicon(request):
    return FileResponse(open('static/imgs/logo.svg', 'rb'))


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = data = json.loads(request.body)
        q1 = data.get('question1')
        return JsonResponse({'ok': 'true'}, status=200)
