from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import RedirectView
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urlshortner_app.models import UrlShortner
from .serializers import UrlShortnerSerializer
from rest_framework import status
from rest_framework.views import APIView

import hashlib

# Create your views here.
class UrlShortnerAPIView(LoginRequiredMixin, APIView):

    serializer_class = UrlShortnerSerializer
    queryset = UrlShortner.objects.all()
    login_url = '/admin/'

    def get(self, request, format=None):

        value = str(request.get_full_path()).split('/api/new/', 1)[1]

        # Check if URL is valid
        validate = URLValidator()
        try:
            validate(value)
        except ValidationError:
            return JsonResponse({'Error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

        # If URL already exists
        if UrlShortner.objects.filter(original_url=value).exists():
            original_url_object = get_object_or_404(UrlShortner, Q(original_url=str(value)))

            original_url = str(original_url_object.original_url)
            url = original_url.replace('https://', 'http://')

            return redirect(url)

        # If URL not exists
        original_url = value
        if not UrlShortner.objects.filter(original_url=value).exists():

            # through this, same url can not save with same encryption
            while True:

                encrypted_url = hashlib.sha512(value).hexdigest()

                sliced_start_data = encrypted_url[0:5]
                sliced_end_data = encrypted_url[-5:]

                try:

                    UrlShortner.objects.get(
                        Q(short_url__startswith=sliced_start_data) |
                        Q(short_url__endswith=sliced_end_data)
                    )
                    value = encrypted_url

                except UrlShortner.DoesNotExist:

                    # save here user id, url and encrypted value
                    if request.user.id:

                        URL = UrlShortner(user=request.user, original_url=original_url, short_url=encrypted_url)
                        URL.save(force_insert=True)
                        response_data = {"original_url": original_url, "short_url": "http://localhost:8000/api/"+encrypted_url[0:5]}
                    else:
                        # set warning if user id is null
                        response_data = {'error': 'Need to be login before save'}

                    break
        else:
            # prepare response data
            url_data = get_object_or_404(UrlShortner, original_url=value)
            response_data = {
                "original_url": url_data.original_url,
                "short_url": "http://localhost:8000/api/"+url_data.short_url[0:5]
            }

        return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLView(RedirectView):

    permanent = True

    def dispatch(self, request, *args, **kwargs):

        code = kwargs['code']
        original_url_object = get_object_or_404(UrlShortner, Q(short_url__startswith=str(code)))

        original_url = str(original_url_object.original_url)
        url = original_url.replace('https://', 'http://')

        return redirect(url)
