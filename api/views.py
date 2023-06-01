from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .models import SensorData
from sklearn.linear_model import LinearRegression

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

  train_size = int(len(df) * 0.8)  # Usaremos el 80% de los datos para entrenamiento
  train_data = df[:train_size]
  test_data = df[train_size:]

  # Separar variables dependientes e independientes (como se mostró anteriormente)
  X_train = train_data[['temperature', 'humidity', 'lux', 'soil_moisture']]
  y_train = train_data['soil_moisture_ratio']
  X_test = test_data[['temperature', 'humidity', 'lux', 'soil_moisture']]
  y_test = test_data['soil_moisture_ratio']

  # Crear y entrenar el modelo de regresión lineal (como se mostró anteriormente)
  model = LinearRegression()
  model.fit(X_train, y_train)

  # Preparar los datos para la predicción del instante 11
  new_data = df.loc[10].to_frame().T  # Suponiendo que el dato en el instante 10 está en la fila con etiqueta 10

  # Realizar la predicción para el instante 11
  prediction_11 = model.predict(new_data[['temperature', 'humidity', 'lux', 'soil_moisture']])

  # retornar la predicción
  return JsonResponse({'prediction': prediction_11[0]})


