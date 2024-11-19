from django.shortcuts import render
from rest_framework.views import APIView
import pandas as pd
from .models import AirPollution
from .serializer import AirPollutionSerializer
from rest_framework.response import Response
from rest_framework import status
import os
from django.http import JsonResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
def generate_air_pollution_diagram(request):
    try:
        # Query air pollution data
        air_pollution_data = AirPollution.objects.values("hour", "pm").order_by("hour")

        # Prepare data for the diagram
        hours = [data["hour"] for data in air_pollution_data]
        pollution_levels = [float(data["pm"]) for data in air_pollution_data]

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(hours, pollution_levels, color="blue", alpha=0.7)
        plt.xlabel("Hour")
        plt.ylabel("PM Levels")
        plt.title("Air Pollution Levels by Hour")
        plt.xticks(hours)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Save the chart to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        # Encode the image in base64 to send it in the response
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()

        # Return the diagram as base64
        return JsonResponse({"diagram": image_base64}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
