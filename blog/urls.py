from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDetailView, PostDeleteView, PostAdminListView

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('admin/', PostAdminListView.as_view(), name='list_admin'),
    path('new/', PostCreateView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='delete'),
]
