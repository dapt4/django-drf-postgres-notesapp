from django.urls import path
from . import views

urlpatterns = [
    path('note', views.note),
    path('note/<int:id>', views.edit_note),
    path('login',views.login),
    path('register', views.register)
]
