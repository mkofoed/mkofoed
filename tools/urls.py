from django.urls import path

from tools.views import EncodeDecodeView, DateParseView, \
    PprintJSONView

app_name = 'tools'

urlpatterns = [
    path('encode/', EncodeDecodeView.as_view(), name='encode'),
    path('date/', DateParseView.as_view(), name='date_parse'),
    path('pprint/', PprintJSONView.as_view(), name='pprint'),
]
