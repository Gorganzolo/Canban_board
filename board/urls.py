from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView,
    ReplyCreateView, UserRepliesListView, ReplyAcceptView, ReplyDeleteView,
    MySentRepliesListView
)

app_name = 'board'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/reply/', ReplyCreateView.as_view(), name='reply_create'),

    path('my-replies/', UserRepliesListView.as_view(), name='user_replies'),
    path('reply/<int:pk>/accept/', ReplyAcceptView.as_view(), name='reply_accept'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),

    path('my-sent-replies/', MySentRepliesListView.as_view(), name='my_sent_replies'),
]