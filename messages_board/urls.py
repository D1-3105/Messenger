from django.urls import path
from .views import MsgBoardView, dialog_view
urlpatterns = [
    path('', MsgBoardView.as_view(),name='all_messages'),
    path('id<int:pk>', dialog_view, name='detail_dialog'),
]
