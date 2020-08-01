from django.urls import path
from.views import ListUsers


urlpatterns = [
    path('', ListUsers.as_view()),
    path('users/', ListUsers.as_view()),
]
