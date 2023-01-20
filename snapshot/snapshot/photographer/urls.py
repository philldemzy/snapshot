from django.urls import path

import views

urlpatterns = [
    path("register", views.register, name="register"),
]
