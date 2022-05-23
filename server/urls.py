"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


def generate_api_url_include(name):
    regex = '{}/'.format(name)
    namespace = 'api-{}'.format(name)
    url_path = path(regex, include(('api.{}.urls'.format(name), name), namespace=namespace))
    return url_path


namespaces_to_include = [
    "quiz"
]


api_namespace_urls = [
    generate_api_url_include(name) for name in namespaces_to_include
]


urlpatterns = [
    path(r'api/v1/', include(api_namespace_urls))
]

urlpatterns += [
    path('{}/'.format(settings.ADMIN_URL), admin.site.urls),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.ENVIRONMENT in ('local',) and settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
