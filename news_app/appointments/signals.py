from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор

from .models import Appointment


# создаём функцию обработчик с параметрами под регистрацию сигнала
# выполняет действие при каком-либо действии пользователя, в нашем случае - сохранение в БД Appointment записи
@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Изменились данные {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    print("МЕТОД 999999999999 НУЖНЫЙ СРАБОТАЛ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(subject)

    mail_managers(
        subject=subject,
        message=instance.message,
    )
