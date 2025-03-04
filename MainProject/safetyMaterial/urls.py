"""safetyMaterial URL Configuration

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
from django.urls import path,include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('admin/login/', admin.site.login, name='admin_login'),

    path('', TemplateView.as_view(template_name="index.html"), name='index'),  # root URL maps to home page
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),

    path('home/', include('home.urls')),
    path('products/', include('products.urls')),
    path('about-us/', include('about_us.urls')),
    path('contact/', include('contact.urls')),
    path('about_us/', include('about_us.urls')),
]

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib import admin

class CustomAdminLoginView(LoginView):
    def get_success_url(self):
        return ''  # Redirects to index page
admin.site.login = CustomAdminLoginView.as_view()


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






