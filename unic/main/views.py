import json
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from openai import OpenAI



def main(request):
    return render(request, 'main.html')


def favicon(request):
    return FileResponse(open('static/imgs/logo.svg', 'rb'))


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Извлекаем ответы на вопросы
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

        # Формируем промпт для ChatGPT
        prompt = f"""Проанализируй результаты профориентационного опроса и дай рекомендации.

Ответы респондента:

1. Тип задач: {question1}
2. Формат работы: {question2}
3. Школьный предмет: {question3}
4. Важно в профессии: {question4}
5. Баллы ЕГЭ (сумма трех предметов): {question5}

Развернутые ответы:
6. Успешный проект: {text_question1}
7. Проект с неограниченными ресурсами: {text_question2}
8. Чем бы занимался при равной оплате: {text_question3}
9. Идеальный рабочий день через 5 лет: {text_question4}
10. Пожелания к городу обучения: {text_question5}

На основе этих данных, пожалуйста:
1. Определи основные интересы и склонности человека
2. Предложи 2-3 подходящие специальности
3. Порекомендуй конкретные вузы для поступления, СТРОГО учитывая пожелания к городу обучения и баллы ЕГЭ (подбирай вузы с проходным баллом, соответствующим указанному диапазону)

Ответ представь в структурированном формате."""

        try:
            # Инициализируем клиент OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            # Отправляем запрос к ChatGPT
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты профессиональный карьерный консультант, который помогает студентам выбрать специальность и вуз для поступления. Твои рекомендации основаны на интересах, способностях и целях студента."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            # Извлекаем текст ответа
            ai_recommendation = response.choices[0].message.content

            return JsonResponse({
                'success': True,
                'recommendation': ai_recommendation
            }, status=200)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
