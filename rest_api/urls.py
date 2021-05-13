from django.urls import path, include
from rest_framework import routers

from rest_api.viewsets import UserViewSet, PostViewSet
from tools.views import EncodeDecodeAPIView, DateParseAPIView, PprintJSONAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('encode/', EncodeDecodeAPIView.as_view()),
    path('date/', DateParseAPIView.as_view()),
    path('pprint/', PprintJSONAPIView.as_view()),
    path('', include(router.urls))
]
