from django.urls import path

from estimateapp.views import CreateEstimateView, OutputImageView, testview

app_name = 'estimateapp'

urlpatterns = [
    path('input/', CreateEstimateView.as_view(), name='create'),
    path('output/<int:pk>', OutputImageView.as_view(), name='detail'),
    path('test/', testview)
]