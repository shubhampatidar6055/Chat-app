from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", home_view, name='home'),
    path("profile_view/", profile_view, name="profile"),
    path("profile_edit/", profile_edit, name="profile_edit"),
    path('onboarding/', profile_edit, name="profile-onboarding"),
    path('profile_settings/', profile_settings, name='profile-settings'),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('profile_emailverify/', profile_emailverify, name='profile-emailverify'),
    path("profile_delete/", profile_delete, name='profile-delete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
