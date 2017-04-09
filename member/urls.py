from django.conf.urls import url

from .views import UserCreate


urlpatterns = [
    url(r'^v1/register$', UserCreate.as_view(), name="register"),
]
