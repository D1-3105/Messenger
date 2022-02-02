from django.urls import path
from .views import SignUpView, ResetPWView, ResetViaEmailView
from django.views.generic import TemplateView
urlpatterns=[
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('reset_me/', ResetViaEmailView.as_view(), name='reset_pw'),
    path('reset_me/<str:username>/<str:token>', ResetPWView.as_view(), name='reset_access_allowed'),
    path('reset_me/success', TemplateView.as_view(template_name='user/thanks.html'), name='thanks'),
]