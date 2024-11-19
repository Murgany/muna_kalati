"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = "Muna Kalati Admin"
admin.site.site_title = "Muna Kalati Admin Portal"
admin.site.index_title = "Welcome to Muna Kalati Portal"    

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('muna_kalati.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
    
]
