from base64 import b64encode
import json
import requests
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



def main(request):
    return render(request, 'main.html')


def favicon(request):
    return FileResponse(open('static/imgs/logo.svg', 'rb'))


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = b64encode(f'api:{settings.PASSWORD}'.encode('utf-8')).decode('ascii')
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-OpenAI-Api-Key": settings.API_KEY,
            "Authorization": f'Basic {token}'
        }

        body = {
            "openai_api_url_base": "https://api.openai.com/v1/",
            "store_uuid": "804fec54-0d5b-4274-9e16-a9a4b3eceb77",
            "openai_model_name": "gpt-3.5-turbo",
            "openai_embedding_model_name": "text-embedding-ada-002",
            "instructions": "Ты - профессиональный карьерный консультант. По ответам пользователя ты должен подобрать для него подходящие ВУЗы и специальности в них. Обращай внимание на баллы поступления и предпочтения по городу. Предлагай несколько вариантов",
        }

        question1 = data.get('question1', '')
        question2 = data.get('question2', '')
        question3 = data.get('question3', '')
        question4 = data.get('question4', '')
        question5 = data.get('question5', '')
        text_question1 = data.get('text-question1', '')
        text_question2 = data.get('text-question2', '')
        text_question3 = data.get('text-question3', '')
        text_question4 = data.get('text-question4', '')
        text_question5 = data.get('text-question5', '')

        prompt = f"""
            Подбери ВУЗы и специальности по следующим ответам пользователя:
            1. Какой тип задач вам интереснее всего решать? Ответ: 
        """

        body["question"] = prompt

        r = requests.post(
            'https://api2.api2app.org/api/v1/store_question',
            headers=headers,
            data=json.dumps(body)
        )

        return JsonResponse({
            'success': True,
            'message': 'Форма успешно отправлена.'
        }, status=200)
