from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User  # модель формы, которую реализует данный дженерик;
    form_class = BaseRegisterForm  # форма, которая будет заполняться пользователем;
    success_url = '/'  # URL, на который нужно направить пользователя после успешного ввода данных в форму.


# view для апгрейда аккаунта до Автора - для добавления в группу Автор. Для данной задачи не существует
# дженерика, поэтому создаем функцию-представление.
@login_required
def become_author(request):
    user = request.user
    # Получили объект (логин, или тупо имя) текущего пользователя из переменной запроса
    authors_group = Group.objects.get(name='authors')
    # Вытащили автор-группу из модели Group
    if not request.user.groups.filter(name='authors').exists():
        # Дальше проверяем, находится ли пользователь в этой группе (вдруг кто-то решил перейти по этому URL,
        # уже имея статус Автора)
        authors_group.user_set.add(user)
        # И если он не в группе — добавляем.
    return redirect('/')
    # В конце перенаправляем пользователя на корневую страницу,
    # используя метод redirect. Далее берем кнопку с этой функцией


@login_required
def not_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
    return redirect('/')
