from django.urls import path

from .views import Signup, Profile, ObtainToken, my_profile


urlpatterns = [
    path('signup/', Signup.as_view()),
    path('auth/', ObtainToken.as_view()),
    path('profile/<pk>', Profile.as_view()),
    path('me', my_profile)
]
