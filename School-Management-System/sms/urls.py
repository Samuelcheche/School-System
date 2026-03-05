
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index, name='home'),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('employees/', include('employee.urls')),
    path('api/', include('api.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


