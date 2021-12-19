from django.urls import path, include
from .views import NewsList, NewsDetailView, NewsSearch, AddNews, ChangeNews, DeleteNews


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # Ссылка на детали новости
    path('search/', NewsSearch.as_view(), name='news_search'),

    # модуль Д5
    # добавлено новое представление во view с ограничением прав доступа, изначально ограничиваем права в админ панели,
    # там нужно из огромного списка выбрать наше приложения (newapp) и варианты ограничения, такие как
    # Can add post например (выбрал еще Can change post, Can delete post)
    path('add/', AddNews.as_view(), name='news_add'),
    path('edit/<int:pk>', ChangeNews.as_view(), name='news_edit'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
]