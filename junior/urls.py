"""junior URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static


from catalog import views


urlpatterns = [

    path('', views.HomeView.as_view(), name='home'),
    path('<slug:slug>', views.CatalogView.as_view(), name='category'),
    path('book/<slug:slug>', views.BookView.as_view(), name='book'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),

    path('robots.txt', views.robots_view)

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
