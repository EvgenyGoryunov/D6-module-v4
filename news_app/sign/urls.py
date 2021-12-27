# импортируем готовое представление «из коробки» Django на основе класса LoginView
# класс-представление для аутентификации LoginView, для выхода из системы — Logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import BaseRegisterView, not_author
from .views import become_author    # импорт для нашей кнопки проверки или добавления польз в группу премиум

# Данные url перенаправляют пользователя в зависимости от его действий в плане регистрации, либо подгружают шаблон
# для входа в систему (template_name='sign/login.html'), либо шаблон после выхода из
# системы (template_name='sign/logout.html'). Синтаксис для LoginView  и LogoutView идентичен.
# name='login' и name='logout' - имена для этих URL в целях удобства обращения к ним из шаблонов.

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),

    # При выходе с сайта (кнопку, которую мы создали раньше в шаблоне index.html) Django
    # перенаправит пользователя на страницу, указанную в параметре template_name класса LogoutView
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),

    # модифицировать файл конфигурации URL, чтобы Django мог увидеть представление, которое расширяет кол-во
    # полей при регистрации пользователя
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),

    path('become_author/', become_author, name='author'),  # для кнопки автор

    path('not_author/', not_author, name='not_author'),  # для кнопки автор

]
