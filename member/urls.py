from django.conf.urls import url

from .views import UserCreateView, VerifyView, ChangePasswordView, LoginView, \
    ResetView, ResetChangePasswordView, TeamViewSet, InviteView


urlpatterns = [

    url(r'^team/invite$',
        InviteView.as_view(),
        name='invite'),

    url(r'^team$',
        TeamViewSet.as_view({"get": "retrieve", "post": "post"}),
        name='team'),

    url(r'^reset/change-password$',
        ResetChangePasswordView.as_view(),
        name='reset_change_password'),

    url(r'^reset$',
        ResetView.as_view(),
        name='reset_password'),

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
