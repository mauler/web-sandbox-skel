from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings

from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^docs/', include_docs_urls(title='PROJECT')),
    url(r"^v1/members/", include("member.urls", namespace="member")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
