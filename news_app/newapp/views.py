from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin  # модуль Д5, для ограничения прав доступа (см ниже)
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
# модуль Д6
# класс для отправки писем, нужной инфы и в нужном представлении
from django.shortcuts import render, redirect
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.views import View  # модуль Д4
# импортируем необходимые дженерики модуль Д4
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView  # модуль Д4

from .filters import NewsFilter  # импортируем написанный нами фильтр (с файла filters.py)# модуль Д4
from .forms import NewsForm  # модуль Д1-4
from .models import Appointment  # модуль Д6
from .models import Post  # модуль Д1-4


# модуль 6
class AppointmentView(View):
    # метод гет мы получаем шаблон-форму, которую мы заполняем
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    # функция пост сохраняет данный шаблон с данными (отправляет его в базу данных, которую мы создали в моделях)
    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        msg = EmailMultiAlternatives(
            # тема письма, формируем как нам удобно
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # само сообщение
            body=appointment.message,  # это то же, что и message
            # от кого сообщение, должна быть именно ваша а не чья попало
            from_email='ges300487@yandex.ru',
            # список, кому нужно будет отправлять письма, всем и себе в том числе (как копию на всякий случай)
            to=['ges1987@list.ru'],  # это то же, что и recipients_list
            # fail_silently=False  # если какая-то ошбика или сервер умрет, пользователь не увидит ошибку
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        return redirect('appointments:make_appointment')


# модуль Д1-4
class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news_list.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку
    # объектов через HTML-шаблон
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для поиска постов
class NewsSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    template_name = 'news_search.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку
    # объектов через HTML-шаблон
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# дженерик для получения деталей о товаре
class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы
class NewsAddView(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    success_url = '/news/'


# дженерик для редактирования объекта
class NewsEditView(UpdateView):
    template_name = 'news_edit.html'
    form_class = NewsForm
    success_url = '/news/'  # после редактирования нашей статьи нас будет перебрасывать по указанному адресу

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся
    # редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новости
class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'  # после удаления нашей статьи нас будет перебрасывать по указанному адресу


# Модуль Д5 - Ограничения прав доступа
# через запятую указываем какие права хотим ограничить, предварительно в админ панели создали данные ограничения,
# а в данном месте мы накладываем ограничения конкретно на представление, то есть выводы страничек сайта, если
# пользователь не входит в нужную группу, ему летает страница с ошибкой 403 (страница недоступна)
# Существует определенное соглашение для именования разрешений: <app>.<action>_<model>, пример 'newapp.add_post'
# После того, как мы написали наши ограничения, нужно в urls изменить выводы преставлений,указав на новые классы (ниже)

class AddNews(PermissionRequiredMixin, NewsAddView):
    permission_required = ('newapp.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsEditView):
    permission_required = ('newapp.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDeleteView):
    permission_required = ('newapp.delete_post',)
