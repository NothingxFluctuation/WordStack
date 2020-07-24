"""WordStack URL Configuration

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import MainApp.views as main_views

urlpatterns = [
    path('', main_views.home, name='home'),
    path('sign_in/', main_views.sign_in, name='sign_in'),
    path('logout/', main_views.logout, name='logout'),
    path('add_word_data/', main_views.add_word_data, name='add_word_data'),
    path('add_subject_data/', main_views.add_subject_data, name='add_subject_data'),
    path('add_enterprise_data/', main_views.add_enterprise_data, name='add_enterprise_data'),
    path('handle_documents/', main_views.handle_documents, name='handle_documents'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT)