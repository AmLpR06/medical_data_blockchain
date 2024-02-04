from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from doctor.views import sign_in, sign_up, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sign_in, name='sign_in'),
    path('sign_up', sign_up, name='sign_up'),
    path('logout', logout, name='logout'),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
    path('logout/', RedirectView.as_view(url='/admin/logout/'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
