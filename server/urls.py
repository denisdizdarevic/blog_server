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
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_extensions.routers import ExtendedDefaultRouter

from blog.views import PostViewSet, UserViewSet, TagViewSet, AttachmentViewSet, CommentViewSet
from server import settings

router = ExtendedDefaultRouter()
router.register(r'user', UserViewSet)
postRoute = router.register(r'post', PostViewSet)
postRoute.register(r'tag', TagViewSet, basename='post-tag', parents_query_lookups=['post'])
postRoute.register(r'attachment', AttachmentViewSet, basename='post-attachment', parents_query_lookups=['post'])
postRoute.register(r'comment', CommentViewSet, basename='post-comment', parents_query_lookups=['post'])

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('openapi', get_schema_view(
        title="Blog Server",
        description="Blog Server API",
        version="1.0.0",
        url=settings.BASE_URL
    ), name='openapi-schema'),
]
