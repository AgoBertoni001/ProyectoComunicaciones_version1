"""
URL configuration for ProyectoComunicaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from frontendapp import views
import uuid
from frontendapp.views import mis_plantas, valores_referencia, eliminar_planta, procesando


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('subir-imagen/', views.subir_imagen, name='subir_imagen'),
    path('mis-plantas/', views.mis_plantas, name='mis_plantas'),
    path('about/', views.about, name='about'),
    path('valores-referencia/<uuid:planta_id>/', valores_referencia, name='valores_referencia'),
    path('eliminar-planta/<uuid:planta_id>/', views.eliminar_planta, name='eliminar_planta'),
    path('procesando/<int:response_code>/', views.procesando, name='procesando'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
