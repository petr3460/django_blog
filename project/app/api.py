from django.http import JsonResponse
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

def client_get_article(request):
    articles = ArticleSerializer(
        Article.objects.all(),
        many=True,
        context={'request':request}
    ).data
    return JsonResponse({'articles': articles})


def client_get_comment(request, article_id):
    comments = CommentSerializer(
        Comment.objects.filter(article_id=article_id),
        many=True,
        context={'request':request}
    ).data
    return JsonResponse({'comments': comments})
