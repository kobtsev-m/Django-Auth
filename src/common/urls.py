from django.urls import path, include
from common import views


app_name = 'common'

urlpatterns = [
    path('',
         views.Home.as_view(),
         name='index'
    ),
    path('accounts/signup/',
         views.SignupView.as_view(),
         name='account_signup'
    ),
    path(
        'accounts/social/signup/',
        views.SocialSignupView.as_view(),
        name='socialaccount_signup'
    ),
    path('profile/<int:pk>/',
         views.Profile.as_view(),
         name='user-profile'
    ),
    path('settings/<int:pk>/',
         views.Settings.as_view(),
         name='user-settings'
    )
]
