from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-password-otp/', views.verify_password_otp, name='verify_password_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('profile/', views.profile_view, name='profile'),
    path('verify-profile-otp/', views.verify_profile_otp, name='verify_profile_otp'),
     path('manager/bookings/', views.manager_bookings, name='manager_bookings'),
]