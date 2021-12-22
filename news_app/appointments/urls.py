from django.urls import path

from .views import AppointmentView

urlpatterns = [

    # модуль Д6 - отправка писем
    # http://127.0.0.1:8000/appointment/
    path('', AppointmentView.as_view(), name='make_appointment'),

]
