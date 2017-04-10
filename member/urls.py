from django.conf.urls import url

from .views import UserCreateView, VerifyView, ChangePasswordView, LoginView


urlpatterns = [

    url(r'^v1/login$',
        LoginView.as_view(),
        name='login'),

    url(r'^v1/password$',
        ChangePasswordView.as_view(),
        name='change_password'),

    url(r'^v1/register$', UserCreateView.as_view(), name="register"),
    url(r'^v1/verify/(?P<pk>\d+)$', VerifyView.as_view(), name='verify'),
]
