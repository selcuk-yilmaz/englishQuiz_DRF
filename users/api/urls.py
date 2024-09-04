from django.urls import include, path

from .views import RegisterView, logout, SiteUsersView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path("auth/register/",RegisterView.as_view(),name="register"),
    path("auth/logout/",logout,name="logout_user"),
    path("all-users/", SiteUsersView.as_view()),
]