from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category


# создаём функцию обработчик с параметрами под регистрацию сигнала
# запускает выполнение кода при каком-либо действии пользователя, в нашем случае -
# сохранение в БД модели Post записи
@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, created, **kwargs):
    print()
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')

    global subscriber
    sub_text = instance.text
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    post = instance

    # для удобства вывода инфы в консоль, никакой важной функции не несет
    print('Адреса рассылки:')
    for qaz in subscribers:
        print(qaz.email)

    print()
    print()
    print()
    for subscriber in subscribers:
        # для удобства вывода инфы в консоль, никакой важной функции не несет
        print('**********************', subscriber.email, '**********************')
        print()
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='factoryskill@yandex.ru',
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')

        # для удобства вывода инфы в консоль, никакой важной функции не несет
        print()
        print(html_content)
        print()

        # код ниже временно заблокирован, чтоб пока в процессе отладки не производилась реальная рассылка писем
        # msg.send()

    return redirect('/news/')
