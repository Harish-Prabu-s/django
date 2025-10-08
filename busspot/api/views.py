from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.dateparse import parse_date
from .models import User, Bus, Route, Booking
from .serializers import UserSerializer, BusSerializer, RouteSerializer, BookingSerializer
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# ------------------------------
# User ViewSet
# ------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# ------------------------------
# Bus ViewSet
# ------------------------------
class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        queryset = super().get_queryset()
        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')

        if source:
            queryset = queryset.filter(source__icontains=source)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        source = request.query_params.get("source", "").strip()
        destination = request.query_params.get("destination", "").strip()
        date_str = request.query_params.get("date", "").strip()

        if not (source and destination and date_str):
            return Response([])

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response([])

        routes = Route.objects.filter(
            source__iexact=source,
            destination__iexact=destination,
            date=date_obj
        )
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

# Booking ViewSet
# ------------------------------
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        route_id = self.request.query_params.get('route')
        if route_id:
            queryset = queryset.filter(route_id=route_id)
        return queryset

    def perform_create(self, serializer):
        # Assign logged-in user automatically
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "Booking successful!",
            "booking": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

# ------------------------------
# Register user API
# ------------------------------

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create user with proper password hashing
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data.get('email', ''),
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
        )
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]  # ✅ allow anyone

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")

        if not name or not email or not password:
            return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists():
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)