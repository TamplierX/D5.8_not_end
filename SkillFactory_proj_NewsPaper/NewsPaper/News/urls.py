from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch, NewsCreate, NewsEdit, NewsDelete, ArticlesCreate, ArticlesEdit, ArticlesDelete,
    subscriptions,
)

app_name = 'news'
urlpatterns = [
    path('news/', PostList.as_view(), name='news_list'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_details'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
