from datetime import datetime

from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
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

        # Автоотправка сообщений, пока временно оключено, чтоб другой способ проверить (ниже) - отправка шаблона
        # send_mail(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=appointment.message,  # сообщение с кратким описанием проблемы
        #     from_email='factoryskill@yandex.ru',  # почта с которой отправляем письма
        #     recipient_list=['ges1987@list.ru'],  # список получателей, например, секретарь, врач и т. д.
        #     # fail_silently=False,  # если сервак с почтой сломался, чтоб наш код в ошибку тоже не упал
        # )

        # Пример с отправкой сообщений с шаблонов внутри
        # # получаем наш html, чтоб запихнуть его в наше сообщение и отправить, предварительно создав шаблон
        # html_content = render_to_string(
        #     'appointment_created.html',
        #     {
        #         'appointment': appointment,
        #     }
        # )

        # # отправка целой странички (шаблона) в письме
        # msg = EmailMultiAlternatives(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     body=appointment.message,  # это то же, что и message
        #     from_email='factoryskill@yandex.ru',
        #     to=['ges1987@list.ru'],  # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        #
        # msg.send()  # отсылаем

        # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо, его
        # автоматом возьмем из базы данных пользователей со статусом админ, либо другим, кого укажем, нужно добавить
        # настройки в сеттинги проекта
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
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


# если подчеркивается красным - ничего страшного, работать будет и так
from newapp.models import Category

class AppointView(View):
    def get(self, request, *args, **kwargs):
        # формируем запрос из БЗ из модели Category и присваиваем его результаты переменной categorys
        # запрос формируется следующим образом:
        # _____________1________2______3______4_________5___________________6_______________7________________8
        categorys = Category.objects.all().values('subscribers', 'subscribers__username', 'name', 'subscribers__email')
        # 1-из модели Category (файл models.py приложения news_app) 2-взять объекты, значения(objects) 3-все(all())
        # 4-по полям (либо столбикам, либо колонкам таблицы) на названиями 5, 6, 7, 8
        return render(request, 'test.html', {
            'subs': categorys   # чтоб получить все значения из БД будем проходиться циклом в html страничке
        })
