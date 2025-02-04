from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PublicUserDetailView, update_want_collect

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/<int:user_id>/', PublicUserDetailView.as_view(), name='public_user_detail'),
    path('api/update_want_collect/<int:user_id>/', update_want_collect, name='update_want_collect'),
]
