from django.conf.urls import include, url


urlpatterns = [
    url("", include("member.urls", namespace="member")),
]
