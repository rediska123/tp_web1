"""
URL configuration for ask_rediska123 project.

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
from django.urls import path
from web import views
from ask_rediska123 import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions_view, name='new_questions'),
    path('hot', views.hot_questions_view, name='hot_questions'),
    path('tag/<str:tag_name>', views.tagged_questions_view, name='tagged_questions'),
    path('question/<int:id>', views.question_view, name='question'),
    path('login', views.login_view, name='login'),
    path('registration', views.registration_view, name='registration'),
    path('settings', views.settings_view, name='settings'),
    path('ask', views.new_question_view, name='new_question'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)