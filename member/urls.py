from django.conf.urls import url

from .views import UserCreateView, VerifyView


urlpatterns = [
    url(r'^v1/register$', UserCreateView.as_view(), name="register"),
    url(r'^v1/verify/(?P<pk>\d+)$', VerifyView.as_view(), name='verify'),
]
