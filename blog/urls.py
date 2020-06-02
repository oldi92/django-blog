from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new', views.createPostView, name='post_new'),
    path('post/<int:pk>/remove', views.PostDeleteView.as_view(), name='post_remove'),
    path('post/<int:pk>/edit', views.PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', views.draftListView, name='post_draft_list'),
    path('post/<int:pk>/comment', views.add_comments_to_post, name='add_comments_to_post'),
    path('comment/<int:pk>/remove', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/publish', views.post_publish, name='post_publish')
]
