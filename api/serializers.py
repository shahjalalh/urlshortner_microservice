from urlshortner_app.models import UrlShortner
from rest_framework import serializers

class UrlShortnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UrlShortner
        fields = ('original_url', 'short_url')
