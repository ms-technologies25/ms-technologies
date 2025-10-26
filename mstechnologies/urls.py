from django.contrib import admin
from mstechnologies import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ms-admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('about', views.aboutUs, name="about"),
    path('contact', views.contactUs, name="contact"),
    path('shop/', include("msapps.urls")),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
