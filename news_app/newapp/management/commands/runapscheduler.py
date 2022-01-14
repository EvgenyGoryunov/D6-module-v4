import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime

from newapp.models import Category, Post


logger = logging.getLogger(__name__)


# наша задача - рассылка корреспонденции по вкусам подписчикам
def news_sender():
    print()
    print()
    print()
    print()
    print('===================================ПРОВЕРКА СЕНДЕРА===================================')
    print()
    print()

    # Первый цикл - получение из модели категории по очереди всех объектов (5 шт в моем случае)
    for category in Category.objects.all():
        # print(qaz.id, qaz.name, qaz.subscribers.all())
        # print("------------", qaz.id, qaz.name)

        # пустой список для будущего формирования списка статей, разбитых по категориям + ссылка перехода на каждую
        # статью своя уникальная рядом с названием статьи (топорный вариант ссылок, блокируется сайтами,
        # антиспам срабатывает)
        news_from_each_category = []


        # определение номера прошлой недели
        week_number_last = datetime.now().isocalendar()[1] - 1

        # Второй цикл - из первого цикла получием рк категории, и подставляем его в запрос, в первый фильтр, во второй
        # фильтр подставляем значение предыдущей недели, то есть показать статьи с датой создания предыдущей недели
        for news in Post.objects.filter(category_id=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'category_id__name'):
            # из данных запроса мы выдираем нужные нам поля (dateCreation - для тестов выводится), и из значений данных
            # полей формируем заголов и ссылку на переход на статью
            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Дата создания: {news.get("dateCreation")}, Категория: {news.get("category_id__name")}')
            # каждую строчку помещаем в список
            news_from_each_category.append(new)

        print()
        print('+++++++++++++++++++++++++++++', category.name, '++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print("Письма будут отправлены подписчикам категории:", category.name, '( id:', category.id, ')')


        subscribers = category.subscribers.all()

        # этот цикл лишь для вывода инфы об адресах подписчиков, ни на что не влияет
        print('по следующим адресам email: ')
        for qaz in subscribers:
            print(qaz.email)

        print()
        print()
        # Третий цикл - до формирование письма (имя кому отправляем получаем тут) и рассылка готового
        # письма подписчикам, которые подписаны под данной категорией
        # создаем приветственное письмо с нашим списком новых за неделю статей конкретной категории,
        # помещаем в письмо шаблон, а также передаем в шаблон нужные нам переменные
        for subscriber in subscribers:
            print('____________________________', subscriber.email, '___________________________________')
            print()
            print('Письмо, отправленное по адресу: ', subscriber.email)
            html_content = render_to_string(
                'mail_sender.html', {'user': subscriber,
                                     'text': news_from_each_category,
                                     'category_name': category.name,
                                     'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='factoryskill@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()
            print(html_content)

            # msg.send()
#
#
#
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            news_sender,
            trigger=CronTrigger(second="*/10"),
            # отправляем письма подписчикам в понедельник в 8 утра
            # trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="news_sender",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работка 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Задачник запущен")
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Задачник остановлен...")
            scheduler.shutdown()
            print('Задачник остановлен')
            logger.info("Задачник остановлен успешно!")