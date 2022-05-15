"""ApiForApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.views.generic.base import RedirectView
from ThisApiForThatThing.views import MainPageView, RandomDataCall, TypeDataCall, AllTypes, \
    CrudPageView, MetaDataCall, CrudPageViewWithId

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='home'),
    path('api/random/', RandomDataCall.as_view(), name='random'),
    path('api/types/', AllTypes.as_view(), name='types'),
    path('api/types/<str:type>', TypeDataCall.as_view(), name='type'),
    path('crud/id=<int:id>', CrudPageViewWithId.as_view(), name='crud'),
    path('crud/', CrudPageView.as_view(), name='crudId'),
    path('api/meta/', MetaDataCall.as_view(), name='meta'),
]
