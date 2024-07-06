import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Post


@shared_task
def send_notification(post_pk):
    #  Получает созданную новость.
    new_post = Post.objects.get(id=post_pk)
    #  Получаем сет категорий созданной новости.
    categories = set(new_post.values_list('post_category__category_name', flat=True))
    #  Получаем сет подписчиков на эти категории.
    users = set(User.objects.filter(subscriber__category__category_name__in=categories))

    subject = f'Опубликована новость на сайте NewsPaper'

    text_content = (
        f'{new_post.content_title}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{new_post.get_absolute_url()}'
    )

    html_content = (
        f'{new_post.content_title}<br><br>'
        f'<a href="http://127.0.0.1{new_post.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )

    for user in users:
        msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_newsletter():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    #  Получаем все статьи за неделю.
    posts = Post.objects.filter(content_category='NE', date_create__gte=last_week)
    #  Получаем сет категорий, что входят в недельную рассылку.
    categories = set(posts.values_list('post_category__category_name', flat=True))
    #  Получаем сет подписчиков на эти категории.
    users = set(User.objects.filter(subscriber__category__category_name__in=categories))

    for user in users:
        #  Смотрим, на какие категории подписан конкретный пользователь.
        category_sub = user.subscriber.values_list('category__category_name', flat=True)
        #  Фильтрует статьи, которые интересуют конкретного пользователя.
        post_category_sub = set(posts.filter(post_category__category_name__in=category_sub))

        html_content = render_to_string('weekly_articles.html',
                                        {'link': f'http://127.0.0.1:8000',
                                         'posts': post_category_sub,
                                         })
        msg = EmailMultiAlternatives(
            subject='Список статей за неделю',
            body='',
            from_email='test@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
