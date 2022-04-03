from django.urls import path
from tiktok.views import InfoView, StreamingView, DownloadView, CoverView


urlpatterns = [
    path('info/<str:code>/', InfoView.as_view(), name='tiktok-share-info'),
    path('info/<str:user>/video/<int:id>/', InfoView.as_view(), name='tiktok-url-info'),
    path('streaming/<str:code>/', StreamingView.as_view(), name='tiktok-share-streaming'),
    path('streaming/<str:user>/video/<int:id>/', StreamingView.as_view(), name='tiktok-url-streaming'),
    path('download/<str:code>/', DownloadView.as_view(), name='tiktok-share-download'),
    path('download/<str:user>/video/<int:id>/', DownloadView.as_view(), name='tiktok-url-download'),
    path('cover/<str:code>/', CoverView.as_view(), name='tiktok-share-cover'),
    path('cover/<str:user>/video/<int:id>/', CoverView.as_view(), name='tiktok-url-cover'),
]
