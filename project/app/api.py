from django.http import JsonResponse
from .models import Article
from .serializers import ArticleSerializer

def client_get_article(request):
    articles = ArticleSerializer(
        Article.objects.all(),
        many=True,
        context={'request':request}
    ).data
    return JsonResponse({'articles': articles})
