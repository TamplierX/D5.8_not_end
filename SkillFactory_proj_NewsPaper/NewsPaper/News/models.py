from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from .resources import CATEGORY_TYPE


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(post_rating=Sum('content_rating'))
        p_rat = 0
        p_rat += post_rat.get('post_rating')

        comment_rat = self.author_user.comment_set.aggregate(comment_rating=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_rat.get('comment_rating')

        self.author_rating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return self.author_user.username.title()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content_category = models.CharField(max_length=2, choices=CATEGORY_TYPE, default="NE")
    date_create = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    content_title = models.CharField(max_length=255)
    content_text = models.TextField()
    content_rating = models.FloatField(default=0.0)

    def like(self):
        self.content_rating += 1
        self.save()

    def dislike(self):
        self.content_rating -= 1
        self.save()

    def preview(self):
        return f'{self.content_text[0:123]}...'

    def __str__(self):
        return f'{self.content_title} {self.date_create} {self.content_text}'

    def get_absolute_url(self):
        return reverse('news:post_details', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriber',)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriber',)
    