from django.core.mail import mail_managers, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.template.loader import render_to_string

from .models import Post, Category


# создаём функцию обработчик с параметрами под регистрацию сигнала
# выполняет действие при каком-либо действии пользователя, в нашем случае - сохранение в БД записи
@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, created, **kwargs):
    global subscriber
    # instance_category = instance.category.first()
    # print(instance_category)

    # if instance_category and not created:
    #     post_id = instance.pk
    #     print(post_id)
    #     emails_in_dict = instance_category.users.all().values('email')
    #     emails = []
    #     print(emails_in_dict)

    category_pk = instance.pk
    sub_text = instance.text
    category = Category.objects.get(pk=category_pk)
    subscribers = category.subscribers.all()
    sub_title = instance.title
    host = instance.META.get('HTTP_HOST')

    # for user_email in emails_in_dict:
    #     emails.append(user_email['email'])

    for subscriber in subscribers:
        print('Адреса рассылки:', subscriber.email)

    html = render_to_string(
        'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': sub_title, 'host': host})

    # html = render_to_string(
    #     'newspaper/send_messages/message.html',
    #     {'post_id': post_id},
    # )

    msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='factoryskill@yandex.ru',
            to=subscriber.email
        )

    # msg.attach_alternative(html, 'text/html')
    # print('Письмо от сигнала!!!!!!', msg)
    # msg.send()
    #
    #



    #
    # print("МЕТОД POST  СРАБОТАЛ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(subject)

    # mail_managers(
    #     subject=subject,
    #     message=instance.message,
    # )

