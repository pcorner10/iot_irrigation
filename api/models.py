from django.db import models

# Create your models here.
# the kind of data we want to store in our database are:
# Temperature, Humidity, Lux, Soil Moisture, Time
# we will use the models to create a table in our database
# and the fields will be the columns of the table

class SensorData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    lux = models.FloatField()
    soil_moisture = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.temperature) + " " + str(self.humidity) + " " + str(self.lux) + " " + str(self.soil_moisture) + " " + str(self.time)
