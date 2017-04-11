from django.conf.urls import url

from .views import UserCreateView, VerifyView, ChangePasswordView, LoginView


urlpatterns = [

    url(r'^login$',
        LoginView.as_view(),
        name='login'),

    url(r'^change-password$',
        ChangePasswordView.as_view(),
        name='change_password'),

    url(r'^register$',
        UserCreateView.as_view(),
        name="register"),

    url(r'^verify/(?P<pk>\d+)$',
        VerifyView.as_view(),
        name='verify'),

]
