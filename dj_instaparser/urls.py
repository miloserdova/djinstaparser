"""dj_instaparser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from dj_instaparser.views import ItemsList, Main, CollectItems, EditItem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view(), name='index'),
    path('create/', CollectItems.as_view(), name='create_store'),
    path('store/<str:store>/', ItemsList.as_view(), name='items_list'),
    path('edit/<int:item_id>/', EditItem.as_view(), name='edit_item')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
