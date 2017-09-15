from django.conf.urls import url
from .views import UrlShortnerAPIView, RedirectURLView


urlpatterns = [
    url(r'^(?P<code>[a-zA-Z0-9]{5})', RedirectURLView.as_view()),
    url(r'^new/', UrlShortnerAPIView.as_view()),

]
