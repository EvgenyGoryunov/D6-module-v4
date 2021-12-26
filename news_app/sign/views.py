from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User  # модель формы, которую реализует данный дженерик;
    form_class = BaseRegisterForm  # форма, которая будет заполняться пользователем;
    success_url = '/'  # URL, на который нужно направить пользователя после успешного ввода данных в форму.


# view для апгрейда аккаунта до Premium - для добавления в группу premium. Для данной задачи не существует
# дженерика, а писать класс-представление для такой задачи избыточно, поэтому напишем функцию-представление.
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def become_author(request):
    # Получили объект (логин, или тупо имя) текущего пользователя из переменной запроса
    user = request.user
    # Вытащили premium-группу из модели Group
    authors_group = Group.objects.get(name='authors')
    # Дальше проверяем, находится ли пользователь в этой группе (вдруг кто-то решил перейти по этому URL, уже имея
    # Premium)
    if not request.user.groups.filter(name='authors').exists():
        # И если он не в группе — добавляем.
        authors_group.user_set.add(user)
    #     В конце перенаправляем пользователя на корневую страницу,
    # используя метод redirect. Далее берем кнопку с этой функцией
    return redirect('/')


# Предоставление прав пользователям
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

from django.views.generic.edit import CreateView
class AddProduct(PermissionRequiredMixin, CreateView):
    permission_required = ('shop.add_product',)

# Если пользователь, который вызвал это представление относится к группе content-manager и для нее предоставлено
# это право, то представление выполнится, как и планировалось. Если же пользователь таких прав не имеет, то Django
# выбросит исключение PermissionDenied и пользователя перенаправит на страницу с ошибкой 403