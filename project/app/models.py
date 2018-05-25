from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.TextField(verbose_name='текст статьи')
    title = models.CharField(max_length=200, verbose_name='название статьи')
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, verbose_name='тег')
    image = models.ImageField(null=True, blank=True, upload_to='static/img/')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def comments(self):
        return self.comments.all()

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    created_date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, verbose_name='статья', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='img/avatars/', default='static/default_avatar.png')



    