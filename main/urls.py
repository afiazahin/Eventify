"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from eventify.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('allevents/', event_view, name='event_view'),
    path('events/<int:event_id>/', eventdetail, name='event_detail'),
    path('event/<int:event_id>/buy/', buy_ticket, name='buy_ticket'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('user_profile/', user_profile, name='user_profile'),
    path('contact/', ContactUs, name='ContactUs'),

    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()