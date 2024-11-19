from django.shortcuts import render
from rest_framework.views import APIView
import pandas as pd
from .models import AirPollution
from .serializer import AirPollutionSerializer
from rest_framework.response import Response
from rest_framework import status
import os

def insert_air_pollution_data(request):
    try:
        # Load CSV file
        file_path = os.getenv("FILE_PATH", "") + "pollution_data.csv"
        if not os.path.exists(file_path):
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        load_csv = pd.read_csv(file_path)
        if "pm2.5" in load_csv.columns:
            load_csv.rename(columns={"pm2.5": "pm"}, inplace=True)

        # Convert DataFrame to a list of dictionaries
        air_pollution_data = load_csv.to_dict(orient='records')

        # Create AirPollution objects for bulk creation
        air_pollution_objects = [
            AirPollution(**data) for data in air_pollution_data
        ]

        # Bulk insert into the database
        AirPollution.objects.bulk_create(air_pollution_objects)

        return Response({"message": "Air pollution data inserted successfully."}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
