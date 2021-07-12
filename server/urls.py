"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.schemas import get_schema_view
from rest_framework_extensions.routers import ExtendedDefaultRouter

from blog.views import PostViewSet, UserViewSet, CommentViewSet, TagListView, AuthView
from server import settings

router = ExtendedDefaultRouter()
router.register(r'auth', AuthView, basename='auth')
router.register(r'user', UserViewSet)
router.register(r'tag', TagListView, basename='tag')
postRoute = router.register(r'post', PostViewSet)
postRoute.register(r'comment', CommentViewSet, basename='post-comment', parents_query_lookups=['post'])

import mimetypes
mimetypes.add_type("application/javascript", ".js", True)

urlpatterns = [
    path('api/', include(router.urls)),
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/openapi', get_schema_view(
        title="Blog Server",
        description="Blog Server API",
        version="1.0.0",
    ), name='openapi-schema'),
    re_path('^media(?P<path>.*)/$', serve, kwargs={'document_root': settings.MEDIA_ROOT}),
    re_path('^(?P<path>.*)/$', serve, kwargs={'document_root': settings.CLIENT_ROOT}),
    path('', serve, kwargs={'path': 'index.html', 'document_root': settings.CLIENT_ROOT}),
]
