from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin  # модуль Д5, чтоб ограничить права доступа
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView

from .filters import NewsFilter  # фильтр (с файла filters.py)
from .forms import NewsForm
from .models import Post, Category


# дженерик для главной страницы
class NewsList(ListView):
    model = Post  # (2)
    template_name = 'news_list.html'
    context_object_name = 'posts'  # (3)
    ordering = ['-dateCreation']
    paginate_by = 5

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст, то есть чтоб переменная 'filter' появилась на странице
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для поиска статей
class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст странички
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для получения деталей о посте
class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context1 = super().get_context_data(**kwargs)

        if not self.request.user.groups.filter(name='authors').exists():
            print()
            context['is_not_subscribe'] = not self.request.user.groups.filter(name='authors').exists()
            print(context)
            return context
        if self.request.user.groups.filter(name='authors').exists():
            context1['is_subscribe'] = self.request.user.groups.filter(name='authors').exists()
            return context1


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы
class NewsAddView(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    success_url = '/news/'


# дженерик для редактирования объекта
class NewsEditView(UpdateView):
    template_name = 'news_edit.html'
    form_class = NewsForm
    success_url = '/news/'  # после редактирования статьи перейдем по указанному адресу, то есть у нас это главная

    def get_object(self, **kwargs):  # (4)
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новости
class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'  # после удаления нашей статьи перейдем по указанному адресу


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk')
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')

@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk')
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')



# Модуль Д5 - Ограничения прав доступа
# (1)
class AddNews(PermissionRequiredMixin, NewsAddView):
    permission_required = ('newapp.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsEditView):
    permission_required = ('newapp.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDeleteView):
    permission_required = ('newapp.delete_post',)

#
#
# (1)
# через запятую указываем какие права хотим ограничить, предварительно в админ панели создали необходимые ограничения,
# а в данном месте мы накладываем ограничения конкретно на представление, то есть выводы страничек сайта, если
# пользователь не входит в нужную группу, ему вылетает страница с ошибкой 403 (страница недоступна вам)
# Существует определенное соглашение для именования разрешений: <app>.<action>_<model>, пример 'newapp.add_post'
# После того, как мы написали наши ограничения, нужно в urls изменить выводы преставлений, указав на новые
#
# (2)
# указываем модель, объекты которой мы будем выводить
# указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно
# пользователю должны вывестись наши объекты
#
# (3)
# это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку
# объектов через HTML-шаблон
#
# (4)
# метод get_object используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся


# def add_subscribe(request, **kwargs):
#     GET = request.GET
#     # pk = kwargs.get('pk_pk')
#     # id = kwargs.get('post.id')
#     pk = request.GET.get('pk_pk')
#     # qwerty = request.GET.get("id", "pk")
#     # print("GET:", dir(request))
#     print("GET:", GET)
#     print("ПиКей:", pk)
#     # print("IdIdId:", id)
#     # print("qwerty:", qwerty)
#
#     # print(request.pk)
#     # print("ЮЗЕР:", request.user)
#     Category.objects.get(pk=Post.objects.get(pk=pk).category.id).subscribers.add(request.user)
#     # Category.objects.get(pk=Post.objects.get(pk=id).category.id).subscribers.add(request.user)
#     return redirect('/news/')


# def add_subscribe(request, **kwargs):
#     pk = request.GET.get('pk')
#     print(pk)
#     Category.objects.get(pk=Post.objects.get(pk=pk).category.id).subscribers.add(request.user)
#     return redirect('/news/')

#
# def subscribe():
#     return redirect('/news/')


# def get_object(self, **kwargs):  # (4)
# id = self.kwargs.get('pk')
# print("id поста:", id)
# print("id категории:", Post.objects.get(pk=id).category.id)
# print("Название категории:", Post.objects.get(pk=id).category)
# return Post.objects.get(pk=id).category.id
# qaz=Post.objects.get(pk=id)
# return id
# return Post.objects.get(pk=id)

# print("id поста:", get_object)

# def qaz(self, get_object):
#     print("Функция гет гет:", Post.objects.get(pk=get_object).category)
#     return Post.objects.get(pk=get_object).category.id