from django.urls import path
from .views import RegisterView, LoginView, user_detail, user_organisations, create_organisation

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<int:id>', user_detail, name='user_detail'),
    path('api/organisations', user_organisations, name='user_organisations'),
    path('api/organisations/create', create_organisation, name='create_organisation'),
]
