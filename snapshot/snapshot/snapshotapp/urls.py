from django.urls import path

from snapshotapp.views import photographer

urlpatterns = [
    path("photographer/register", photographer.register, name="register"),
    path("photographer/login", photographer.login, name="login"),
    path("photographer/media-upload", photographer.upload_media, name="upload_media")
]
