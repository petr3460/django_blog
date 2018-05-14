from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.TextField(verbose_name='текст статьи')
    title = models.CharField(max_length=200, verbose_name='название статьи')
    created_date = models.DateTimeField(default=timezone.now)

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
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text