from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlantaForm
from .models import Planta
import random
import requests
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'frontendapp/index.html', {
        'title': 'Inicio'
    })

def about(request):
    return render(request, 'frontendapp/about.html')

def mis_plantas(request):
    plantas = Planta.objects.all()  # Filtrar por usuario si es necesario
    return render(request, 'frontendapp/mis_plantas.html', {
        'plantas': plantas
    })

def subir_imagen(request):
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear un objeto Planta pero no guardar aún
            planta = form.save(commit=False)

            # Preparar los datos para enviar a la API
            url = "https://comunicaciones.simix.com.ar/v1/comunicaciones/public/plantas"
            files = {'imagen': request.FILES['imagen']}
            data = {
                'descripcion': planta.descripcion,
            }

            # Hacer la solicitud a la API para guardar la imagen y la descripción
            response = requests.post(url, files=files, data=data)

            # Redirigir a la página de procesamiento
            return redirect('procesando', response_code=response.status_code)

        else:
            # Si el formulario no es válido, renderiza de nuevo con el formulario y errores
            return render(request, 'frontendapp/subir_imagen.html', {'form': form})

    else:
        form = PlantaForm()

    return render(request, 'frontendapp/subir_imagen.html', {'form': form})

def procesando(request, response_code):
    if response_code == 200:
        mensaje = "La imagen se ha procesado con éxito."
        # Puedes pasar otros datos necesarios aquí, como el ID de la planta o información adicional
        return render(request, 'frontendapp/procesando.html', {
            'mensaje': mensaje,
            'ir_a_mis_plantas': True  # Indica que el botón para ir a mis plantas debe mostrarse
        })
    else:
        mensaje = "Error al procesar la imagen."
        return render(request, 'frontendapp/procesando.html', {
            'mensaje': mensaje,
            'ir_a_mis_plantas': False  # No mostrar la opción para ir a mis plantas
        })
def editar_planta(request, planta_id):
    planta = get_object_or_404(Planta, id=planta_id)
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES, instance=planta)
        if form.is_valid():
            form.save()
            return redirect('mis_plantas')
    else:
        form = PlantaForm(instance=planta)
    return render(request, 'frontendapp/editar_planta.html', {'form': form, 'planta': planta})

def eliminar_planta(request, planta_id):
    planta = get_object_or_404(Planta, id=planta_id)
    if request.method == 'POST':
        planta.delete()
        return redirect('mis_plantas')
    return render(request, 'frontendapp/eliminar_planta.html', {'planta': planta})

# Endpoints

def listar_plantas(request):
    plantas = Planta.objects.all().values('id', 'nombre', 'imagen', 'especie', 'estado', 'descripcion')
    return JsonResponse(list(plantas), safe=False)

def obtener_planta(request, id):
    # Aquí haces la solicitud GET a la API para obtener la planta analizada
    url = f"https://comunicaciones.simix.com.ar/v1/comunicaciones/public/plantas/{id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Aquí asumes que la API devuelve los campos requeridos
        return JsonResponse({
            'nombre': data['nombre'],
            'imagen': data['imagen'],
            'especie': data['especie'],
            'estado': data['estado'],
            'descripcion': data['descripcion']
        })
    else:
        # Manejar el error si la API no responde correctamente
        return JsonResponse({'error': 'No se pudo obtener la planta'}, status=400)

@csrf_exempt  # Usar solo si no tienes autenticación
def crear_planta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        planta = Planta.objects.create(
            nombre=data['nombre'],
            imagen=data['imagen'],
            especie=data.get('especie', None),
            estado=data['estado'],
            descripcion=data['descripcion']
        )
        return JsonResponse({'id': planta.id}, status=201)

@csrf_exempt  # Usar solo si no tienes autenticación
def actualizar_planta(request, id):
    planta = get_object_or_404(Planta, id=id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        planta.nombre = data['nombre']
        planta.imagen = data['imagen']
        planta.especie = data.get('especie', planta.especie)
        planta.estado = data['estado']
        planta.descripcion = data['descripcion']
        planta.save()
        return JsonResponse({'id': planta.id}, status=200)

def datos_sensor(request, planta_id):
    planta = get_object_or_404(Planta, id=planta_id)
    
    # Datos falsos para la demostración
    sensor_data = [
        {
            'fecha': datetime.datetime.now() - datetime.timedelta(days=i),
            'humedad_tierra': 30 + i,
            'humedad_aire': 50 + 2 * i,
            'temperatura_aire': 20 + 0.5 * i
        }
        for i in range(10)
    ]
    
    context = {
        'planta': planta,
        'sensor_data': sensor_data
    }
    return render(request, 'frontendapp/datos_sensor.html', context)
