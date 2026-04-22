from django.urls import path
from users import views

urlpatterns = [
    path('logout/', views.LogoutViewSet.as_view(), name='logout')
]