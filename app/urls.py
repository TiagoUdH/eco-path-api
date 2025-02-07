from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PublicUserDetailView, update_want_collect, CustomTokenObtainPairView, UserCollectionRequestListView, CollectionRequestCreateView, UnattendedCollectionRequestView, UnattendedRequestsView, MarkCollectionAsCompletedView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/<int:user_id>/', PublicUserDetailView.as_view(), name='public_user_detail'),
    path('api/update_want_collect/<int:user_id>/', update_want_collect, name='update_want_collect'),
    path('api/user/<int:user_id>/collections/', UserCollectionRequestListView.as_view(), name='user-collection-requests'),
    path('api/collection-request/', CollectionRequestCreateView.as_view(), name='collection-request-create'),
    path('api/unattended-collection-request/<int:user_id>/', UnattendedCollectionRequestView.as_view(), name='unattended-collection-request'),
    path('api/unattended-requests/', UnattendedRequestsView.as_view(), name='unattended-requests'),
    path('api/collection-request/<int:pk>/mark-completed/', MarkCollectionAsCompletedView.as_view(), name='mark-collection-completed'),
]
