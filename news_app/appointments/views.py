from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View

from .models import Appointment


# обрабатывает запрос и сохраняет новые объекты в БД (в базе данных), models.py
class AppointmentView(View):
    # получаем шаблон для ввода данных
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    # отправляем на сервер нашу информацию и сохраняем в БД
    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # блок для отправки писем из базы данных любому адресату
        # создали объект в БД, и отправляем его поля по почте, то есть сформировать из них само письмо, для удобства
        # имя клиента сделаем темой, выделим ее жирным шрифтом и чтоб показывалось в письме первым, далее идет само
        # сообщение содержащее краткую суть проблемы и в заключении добавить дату записи. И всё это отправлялось на
        # почту любому адресату

        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='factoryskill@yandex.ru',  # почта с которой отправляем письма
            recipient_list=['ges1987@list.ru'],  # список получателей, например, секретарь, врач и т. д.
            # fail_silently=False,  # если сервак с почтой сломался, чтоб наш код в ошибку тоже не упал
        )

        return redirect('make_appointment')
        # return redirect - дословно означает, что мы должны сделать после выполнения данной функции (def post)
        # конкретно тут: при переходе по адресу http://127.0.0.1:8000/appointment/ (в урлах проекта настроили), мы
        # отправляем запрос get, активируется функция def get, результатом которой является выдача шаблона (странички)
        # make_appointment.html, в данному шаблоне у нас собрана простецкая форма, мы эту форму заполняем, и нажимаем
        # на кнопку, которая данные с нашей формы (с полей) преобразует в строчку и отсылает на сайт, на сервер,
        # который в свою очередь разбирает эту строчку на составляющие, помещает в нашу базу данных в нужные
        # ячейки таблицы (БД). То есть создали объект (=строчка) в нашей таблице (=база данных). В конце, мы просим
        # опять перейти на данную страницу make_appointment после return

        # получаем наш html
        # html_content = render_to_string(
        #     'appointment_created.html',
        #     {
        #         'appointment': appointment,
        #     }
        # )

        # msg = EmailMultiAlternatives(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     body=appointment.message,  # это то же, что и message
        #     from_email='peterbadson@yandex.ru',
        #     to=['skavik46111@gmail.com'],  # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        #
        # msg.send()  # отсылаем
