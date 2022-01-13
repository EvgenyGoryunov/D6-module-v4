from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View

from newapp.models import Category, Post
from .models import Appointment

import datetime


# мои тесты
class AppointView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'test_test.html')


    def post(self, request):
        pole_test = request.POST['test']
        if pole_test:
            pole_test = pole_test
        else:
            pole_test = 1


        pole_test2 = request.POST['test2']
        if pole_test2:
            pole_test2 = pole_test2
        else:
            # предыдущия неделя находится так
            pole_test2 = datetime.datetime.now().isocalendar()[1]-1



        pole_spisok1 = Category.objects.get(pk=pole_test)


        pole_spisok2 = Category.objects.get(pk=pole_test).subscribers.all()
        for qwe in pole_spisok2:
            pass



        pole_spisok3 = Post.objects.filter(category_id=pole_test, dateCreation__week=pole_test2).values('pk', 'title', 'dateCreation')
        # pole_spisok3 = Post.objects.filter(category_id=pole_test, author_id=pole_test2).values('pk', 'title', 'dateCreation')




        news_from_category = []
        for news in pole_spisok3:
            new = (f'{news.get("title")}, {news.get("dateCreation")}, http://127.0.0.1:8000/news/{news.get("pk")}')
            news_from_category.append(new)


        return render(request, 'test_test.html', {
            'pole_test_html': pole_test,
            'pole_test_html2': pole_test2,
            "pole_spisok_html1": pole_spisok1,
            "pole_spisok_html2": pole_spisok2,
            "pole_spisok_html3": pole_spisok3,
            "news_by_category": news_from_category,
        })


        # qaz = Post.objects.filter(category_id=pole_test).values('pk').get("pk")
        # print('qaz:', qaz)
        # wsx = Post.objects.filter(category_id=pole_test).values('title').get("title")
        # print('wsx:', wsx)


        # print('pole_spisok3:', pole_spisok3)
        # print('Список статей на данную тему:')
        # pole_spisok4 = f'{qaz}, http://127.0.0.1:8000/news/{wsx}'
        # print('Список статей на данную тему:', pole_spisok4)

        # print(request)
        # print(dir(request))
        # print(request.POST['pole_test'])
        #     print(qwer.get('title'), 'http://127.0.0.1:8000/news/', qwer.get('pk'), )
        # получаем список адресов в зависимости от pk=pole_test
        # # pole_spisok2 = list(Category.objects.filter(pk=pole_test).values('subscribers__email'))
        # в данном цикле мы можем отправлять каждому пользователю или подписчику под данную категорию нужный список
        # статей, следующий этап сформировать список статей в шаблоне html
        # for qwe in pole_spisok2:
        #     print(qwe.get('subscribers__email',))

        # return redirect ('test')
        # pole_spisok2 = list(Category.objects.filter(pk=pole_test).values('subscribers__username', 'subscribers__email'))
        # print(type(pole_spisok1))
        # выывести список подписоты одной статьи (их мыло)

        # category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
        # subscribers = category.subscribers.all()

        # print('Сообщение:', pole_test)

        # subscribers = Category.objects.filter(pk=cat_id).values('subscribers__email')
        # subscribers = Category.objects.all().values('subscribers', 'subscribers__username', 'name', 'subscribers__email')
        # category = Category.objects.get(pk=Post.objects.get(pk=Post.pk).category.pk)
        # subscribers = category.subscribers.all()

        # for subscriber in subscribers:
        #     print('Адреса рассылки:', subscriber.email)

        # for qaz in subscribers:
        #     # print("имя:", qaz)
        #     print("только почта:", qaz.email)
        #     # print("ИД:", qaz.id)

        # print(subscribers)
        # subscribers = Category.objects.all()

        # for qwe in subscribers:
        #     print(qwe)
        # categorys = Category.objects.all().values('subscribers', 'subscribers__username', 'name', 'subscribers__email')
        # return render(request, 'test_test.html', {
        #     'subs': categorys  # чтоб получить все значения из БД будем проходиться циклом в html страничке
        # })


class AppointmentView(View):
    # получаем шаблон для ввода данных (make_appointment.html)
    def get(self, request, ):
        return render(request, 'make_appointment.html', {})

    # отправляем на сервер нашу информацию и сохраняем ее в БД (сохраняем новый объект класса)
    def post(self, request, ):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # переход на данную форму (представление) после выполнения кода
        return redirect('make_appointment')  # (1)

#
#
#
#
#
# (1)
# return redirect - дословно означает, что мы должны сделать после выполнения данной функции (def post)
# конкретно тут: при переходе по адресу http://127.0.0.1:8000/appointment/ (в урлах проекта настроили), мы
# отправляем запрос get, активируется функция def get, результатом которой является выдача шаблона (странички)
# make_appointment.html, в данному шаблоне у нас собрана простецкая форма, мы эту форму заполняем, и нажимаем
# на кнопку, которая данные с нашей формы (с полей) преобразует в строчку и отсылает на сайт, на сервер,
# который в свою очередь разбирает эту строчку на составляющие, помещает в нашу базу данных в нужные
# ячейки таблицы (БД). То есть создали объект (=строчка) в нашей таблице (=база данных). В конце, мы просим
# опять перейти на данную страницу make_appointment после return

# (2)
# отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо, его
# автоматом возьмем из базы данных пользователей со статусом админ, либо другим, кого укажем, нужно добавить
# настройки в сеттинги проекта


# блок для отправки писем из базы данных любому адресату
# создали объект в БД, и отправляем его поля по почте, то есть сформировать из них само письмо, для удобства
# имя клиента сделаем темой, выделим ее жирным шрифтом и чтоб показывалось в письме первым, далее идет само
# сообщение содержащее краткую суть проблемы и в заключении добавить дату записи. И всё это отправлялось на
# почту любому адресату

# Автоотправка сообщений, пока временно оключено, чтоб другой способ проверить - отправка шаблона
# send_mail(
#     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
#     # имя клиента и дата записи будут в теме для удобства
#     message=appointment.message,  # сообщение с кратким описанием проблемы
#     from_email='factoryskill@yandex.ru',  # почта с которой отправляем письма
#     recipient_list=['ges1987@list.ru'],  # список получателей, например, секретарь, врач и т. д.
#     # fail_silently=False,  # если сервак с почтой сломался, чтоб наш код в ошибку тоже не упал
# )

# Пример с отправкой сообщений с шаблоном внутри
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