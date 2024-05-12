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
    path("", views.index, name='dashboard'),
    path("register", views.register, name='register'),
    path("edit_user", views.edit_user, name='edit_user'),
    path("addnew", views.addnew, name='addnew'),
    path("search", views.search, name='search'),


    path("get_komodita", views.get_komodita, name='get_komodita'),
    path("get_knkod", views.get_knkod, name='get_knkod'),
    path("get_knkod_detail", views.get_knkod_detail, name='get_knkod_detail'),
    path("save_licence", views.save_licence, name='save_licence'),

    path("get_licence", views.get_licence, name='get_licence'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)