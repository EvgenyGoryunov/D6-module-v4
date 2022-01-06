from django.urls import path
from .views import AppointmentView, AppointView#, add_subscribe_t, del_subscribe_t

urlpatterns = [

    # модуль Д6 - отправка писем
    # http://127.0.0.1:8000/appointment/  - путь в данном случае
    path('', AppointmentView.as_view(), name='make_appointment'),
    path('appoint/', AppointView.as_view(), name='test'),

    # модуль Д6 - подписка на рассылку на статью
    # path('add_subscribe_t/', add_subscribe_t, name='add_subscribe_t'),
    # path('del_subscribe_t/', del_subscribe_t, name='del_subscribe_t'),

]
