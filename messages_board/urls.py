from django.urls import path
from .views import MsgBoardView, DialogView
urlpatterns = [
    path('', MsgBoardView.as_view(),name='all_messages'),
    path('id<int:pk>', DialogView.as_view(), name='detail_dialog'),
]
