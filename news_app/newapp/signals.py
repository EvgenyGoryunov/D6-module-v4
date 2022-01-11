from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.http import request
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category


# создаём функцию обработчик с параметрами под регистрацию сигнала
# выполняет действие при каком-либо действии пользователя, в нашем случае - сохранение в БД записи
@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, created, **kwargs):

    global subscriber
    sub_text = instance.text
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    subscribers = category.subscribers.all()
    # host = settings.ALLOWED_HOSTS
    post = instance


    for subscriber in subscribers:
        print('Адреса рассылки:', subscriber.email)

    html_content = render_to_string(
        'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
        from_email='factoryskill@yandex.ru',
        to=[subscriber.email]
    )

    msg.attach_alternative(html_content, 'text/html')
    # print('Письмо от сигнала')
    # print(html_content)

    msg.send()
    #
    return redirect('/news/')
