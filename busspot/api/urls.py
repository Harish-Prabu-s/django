from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, BusViewSet, RouteViewSet, BookingViewSet, register_user
from .views import SignupView
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'buses', BusViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api/", include(router.urls)),
    path('register/', register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
]
