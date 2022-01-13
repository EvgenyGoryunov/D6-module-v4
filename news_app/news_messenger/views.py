from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View

from newapp.models import Category, Post


# класс рассылки новостей подписчикам в зависимости от категории их подписки
class mailing(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'test_test.html')

    def post(self, request):
        pole_test = request.POST['test']
        if pole_test:
            pole_test = pole_test
        else:
            pole_test = 1

        pole_test2 = request.POST['test2']
        if pole_test2:
            pole_test2 = pole_test2
        else:
            # предыдущия неделя находится так
            pole_test2 = datetime.datetime.now().isocalendar()[1] - 1

        pole_spisok1 = Category.objects.get(pk=pole_test)

        pole_spisok2 = Category.objects.get(pk=pole_test).subscribers.all()
        for qwe in pole_spisok2:
            pass

        pole_spisok3 = Post.objects.filter(category_id=pole_test, dateCreation__week=pole_test2).values('pk', 'title',
                                                                                                        'dateCreation')
        # pole_spisok3 = Post.objects.filter(category_id=pole_test, author_id=pole_test2).values('pk', 'title', 'dateCreation')

        news_from_category = []
        for news in pole_spisok3:
            new = (f'{news.get("title")}, {news.get("dateCreation")}, http://127.0.0.1:8000/news/{news.get("pk")}')
            news_from_category.append(new)

        return render(request, 'test_test.html', {
            'pole_test_html': pole_test,
            'pole_test_html2': pole_test2,
            "pole_spisok_html1": pole_spisok1,
            "pole_spisok_html2": pole_spisok2,
            "pole_spisok_html3": pole_spisok3,
            "news_by_category": news_from_category,
        })