const modalOverlay = document.getElementById('modalOverlay')

modalOverlay.addEventListener('click', function(e) {
    if (e.target === modalOverlay) {
        modalOverlay.classList.remove('show')
    }
})


function submit_func() {
    const submitBtn = document.querySelector('.submit-btn')

    submitBtn.disabled = true
    submitBtn.innerHTML = '<span class="spinner"></span>'

    xhr = new XMLHttpRequest()
    xhr.open("POST", "/submit_form", true)
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8')
    xhr.responseType = 'json'

    let formData = {}

    document.getElementsByName('question1').forEach((elem) => {if (elem.checked) {formData['question1'] = elem.value}})
    document.getElementsByName('question2').forEach((elem) => {if (elem.checked) {formData['question2'] = elem.value}})
    document.getElementsByName('question3').forEach((elem) => {if (elem.checked) {formData['question3'] = elem.value}})
    document.getElementsByName('question4').forEach((elem) => {if (elem.checked) {formData['question4'] = elem.value}})
    document.getElementsByName('question5').forEach((elem) => {if (elem.checked) {formData['question5'] = elem.value}})
    
    formData['text-question1'] = document.getElementById('text-question1').value
    formData['text-question2'] = document.getElementById('text-question2').value
    formData['text-question3'] = document.getElementById('text-question3').value
    formData['text-question4'] = document.getElementById('text-question4').value
    formData['text-question5'] = document.getElementById('text-question5').value

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = xhr.response
            const modalContent = document.querySelector('.modal-content')

            if (response.success) {
                // Отображаем рекомендации от ИИ
                modalContent.innerHTML = '<h2>Рекомендации по профориентации</h2><div class="recommendation-text">' +
                    response.recommendation.replace(/\n/g, '<br>') +
                    '</div>'
            } else {
                // Отображаем ошибку
                modalContent.innerHTML = '<p>Произошла ошибка при обработке запроса: ' +
                    (response.error || 'Неизвестная ошибка') + '</p>'
            }

            modalOverlay.classList.add('show')
            submitBtn.disabled = false
            submitBtn.textContent = "Отправить"
        } else {
            console.error('Ошибка запроса:', xhr.status)
            const modalContent = document.querySelector('.modal-content')
            modalContent.innerHTML = '<p>Не удалось отправить форму. Попробуйте еще раз.</p>'
            modalOverlay.classList.add('show')
            submitBtn.disabled = false
            submitBtn.textContent = "Отправить"
        }
    }

    xhr.onerror = function() {
        console.error('Ошибка сети')
        const modalContent = document.querySelector('.modal-content')
        modalContent.innerHTML = '<p>Ошибка соединения. Проверьте подключение к интернету.</p>'
        modalOverlay.classList.add('show')
        submitBtn.disabled = false
        submitBtn.textContent = "Отправить"
    }

    xhr.send(JSON.stringify(formData))
}
