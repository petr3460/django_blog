from rest_framework import serializers
from .models import Article
import pdb


class ArticleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, article):
        request = self.context.get('request')
        image_url = article.image.url
        #pdb.set_trace()
        absolute_uri = request.get_host() + '/static/' + image_url
        return absolute_uri
    class Meta:
        model = Article
        fields = ('author', 'text', 'title', 'created_date', 'tags', 'image', 'likes')



