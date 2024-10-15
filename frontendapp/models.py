from django.db import models

class Planta(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='plantas/')
    especie = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)  # Campo adicional para descripción

    def __str__(self):
        return self.nombre

class SensorData(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='sensor_data')
    fecha = models.DateTimeField(auto_now_add=True)
    humedad_tierra = models.FloatField()
    humedad_aire = models.FloatField()
    temperatura_aire = models.FloatField()

    def __str__(self):
        return f"Data from {self.timestamp}"