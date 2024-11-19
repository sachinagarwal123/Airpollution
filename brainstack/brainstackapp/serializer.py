from rest_framework import serializers
from .models import AirPollution

class AirPollutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirPollution
        fields = "__all__"
