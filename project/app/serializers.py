from rest_framework import serializers
from .models import Article, Comment
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



class CommentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_date', 'article')


