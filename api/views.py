from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .models import SensorData

# Create your views here.
@csrf_exempt
def post_sensor_data(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    nombre = data.get('name', '')
    temperatura = data.get('temperature', 0)
    humedad = data.get('humidity', 0)
    luz = data.get('lux', 0)
    humedad_suelo = data.get('soil_moisture', 0)

    new_record = SensorData(
      name=nombre,
      temperature=temperatura,
      humidity=humedad,
      lux=luz,
      soil_moisture=humedad_suelo
    )

    print(new_record)

    new_record.save()

    return JsonResponse({'status': 'ok'})
  else:
    return HttpResponse('Only POST method is allowed')


def get_sensor_data(request):
  # get data from database
  data = SensorData.objects.all()

  # convert data to dataframes
  df = pd.DataFrame(list(data.values()))

  # column names: id, name, temperature, humidity, lux, soil_moisture, time 
  # use soil_moisture as objetive variable
  # use temperature, humidity, lux as features
  # use time as index
  df = df[['temperature', 'humidity', 'lux', 'soil_moisture', 'time']]
  df.set_index('time', inplace=True)

  # compute the ratio of decrease of soil moisture
  df['soil_moisture_ratio'] = df['soil_moisture'].pct_change()

  # drop the first row
  df.dropna(inplace=True) 

  y = df['soil_moisture_ratio']
  X = df[['temperature', 'humidity', 'lux',"soil_moisture"]]

  


  # convert dataframe to json
  json_data = df.to_json(orient='records')



  return JsonResponse(json_data, safe=False)

