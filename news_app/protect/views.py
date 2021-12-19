from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# generic-представление для отображения шаблона из папки templates, которую мы сами создали и путь до нее прописали
# в файле-настройке проекта settings.py / TEMPLATES / 'DIRS': [os.path.join(BASE_DIR, 'templates')] (+импорт модуля os),
# либо просто можно написать, 'DIRS': [BASE_DIR/'templates'], но хз, вызывало ошибку как-то раз

# данный шаблон protect/index.html запускается, если мы в приложении sign прошли аутентификацию (в соответствии
# с нашей логикой приложения),  LoginRequiredMixin - нужен для того, чтоб данный класс понял, что можно
# запускать представление, что пользователь зарегистрирован в системе
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем весь контекст из класса-родителя
        # добавили новую контекстную переменную is_not_premium, чтобы ответить на вопрос, есть ли пользователь в группе,
        # мы заходим в переменную запроса self.request, из этой переменной мы можем вытащить текущего пользователя,
        # в поле groups хранятся все группы, в которых он состоит, далее применяем фильтр к этим группам и ищем ту самую
        # имя которой premium, после чего проверяем, есть ли какие-то значения в отфильтрованном списке, метод exists()
        # вернет True, если группа premium в списке групп пользователя найдена, иначе — False,# в нашем случае
        # нужно получить наоборот — True, если пользователь не находится в этой группе, поэтому добавляем
        # отрицание not, и возвращаем контекст
        # Важно filter(name = 'authors') чтоб группы совпадали 'authors' тут = премиум в джанге
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context