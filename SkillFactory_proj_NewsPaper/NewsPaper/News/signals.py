from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def news_created(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        if instance.content_category == 'AR':
            return

        emails = User.objects.filter(
            subscriber__category__in=instance.post_category.all()
        ).values_list('email', flat=True)

        emails = set(emails)

        subject = f'Опубликована новость на сайте NewsPaper'

        text_content = (
            f'{instance.content_title}\n\n'
            f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )

        html_content = (
            f'{instance.content_title}<br><br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка на новость</a>'
        )

        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
