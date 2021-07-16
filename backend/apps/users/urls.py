from django.urls import include, path

from .views import RegistrationView

urlpatterns = [
    path('auth/users/', RegistrationView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
