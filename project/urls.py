from django.conf.urls import include, url


urlpatterns = [
    url("^v1/members/", include("member.urls", namespace="member")),
]
