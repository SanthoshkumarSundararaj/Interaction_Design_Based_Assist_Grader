from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='grader-home'),
    path('about/', views.about, name='grader-about'),
    path('main/', views.main, name='grader-main'),
    path('upload/',views.upload, name='grader-upload'),
    path('dev/', views.dev, name='grader-dev'),
    path('devfeed/', views.devfeed, name='grader-devfeed'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)