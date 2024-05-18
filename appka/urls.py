from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
#from django.template.context_processors import static
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy

from myapp import settings
from . import views

app_name = 'appka'

PasswordChangeView.success_url = reverse_lazy("appka:password_change_done")
PasswordResetView.success_url = reverse_lazy("appka:password_reset_done")
PasswordResetConfirmView.success_url = reverse_lazy("appka:password_reset_complete")

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("index", views.index, name='index'),
    path("", views.dashboard, name='dashboard'),
    path("register", views.register, name='register'),
    path("edit_user", views.edit_user, name='edit_user'),

    path("licences/create", views.licence_create, name='licence_create'),
    path("licences/search", views.licence_search, name='licence_search'),
    path("licences/save", views.licence_save, name='licence_save'),
    path("licences/get", views.licence_get, name='licence_get'),

    path("get_komodita", views.get_komodita, name='get_komodita'),
    path("get_knkod", views.get_knkod, name='get_knkod'),
    path("get_country", views.get_country, name='get_country'),
    path("get_knkod_detail", views.get_knkod_detail, name='get_knkod_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)