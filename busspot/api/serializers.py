from rest_framework import serializers
from .models import User, Bus, Route, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = [
            'id',
            'bus_name',
            'bus_number',
            'source',
            'destination',
            'total_seats',
            'available_seats',  # if you calculate this in model
            'departure_time',
            'arrival_time',
            'fare',
            'date'
        ]

    def get_booked_seats_count(self, obj):
        return obj.bookings.count()

class RouteSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)

    class Meta:
        model = Route
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'route', 'seat_number', 'payment_status', 'created_at']
        read_only_fields = ['id', 'payment_status', 'created_at']
    def perform_create(self, serializer):
        seat = serializer.validated_data['seat_number']
        route = serializer.validated_data['route']
        if Booking.objects.filter(route=route, seat_number=seat).exists():
            raise serializers.ValidationError("Seat already booked")
        serializer.save(user=self.request.user)

    def validate(self, data):
        route = data['route']
        seat_number = data['seat_number']
        if Booking.objects.filter(route=route, seat_number=seat_number).exists():
            raise serializers.ValidationError("This seat is already booked!")
        return data
