from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlantaForm
from .models import Planta
import random
import requests
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'frontendapp/index.html', {
        'title': 'Inicio'
    })

def about(request):
    return render(request, 'frontendapp/about.html')


def mis_plantas(request):
    response = requests.get('https://comunicaciones.simix.com.ar/v1/comunicaciones/public/plantas')

    if response.status_code == 200:
        plantas = response.json()  
    else:
        plantas = [] 

    return render(request, 'frontendapp/mis_plantas.html', {'plantas': plantas})

def subir_imagen(request):
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear un objeto Planta pero no guardar aún
            planta = form.save(commit=False)

            # Preparar los datos para enviar a la API
            url = "https://comunicaciones.simix.com.ar/v1/comunicaciones/public/planta"
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

def valores_referencia(request, planta_id):
    if request.method == 'POST':
        # Lógica para hacer el PUT a la API
        data = {
            'temperatura': request.POST.get('temperatura'),
            'humedadTierra': request.POST.get('humedadTierra'),
            'humedadAmbiente': request.POST.get('humedadAmbiente'),
        }
        # URL de la API donde se debe hacer el PUT
        url = f"https://comunicaciones.simix.com.ar/v1/comunicaciones/public/planta/{planta_id}"
        
        response = requests.put(url, json=data)

        if response.status_code in (204, 200):
            return redirect('mis_plantas')  # Redirigir a la página de mis plantas
        else:
            # Manejo de errores si el PUT falla
            return render(request, 'frontendapp/valores_referencia.html', {
                'error': 'Error al cargar valores. Inténtalo de nuevo.',
                'planta_id': planta_id
            })
    return render(request, 'frontendapp/valores_referencia.html', {'planta_id': planta_id})

def eliminar_planta(request, planta_id):
    # Comprobamos si el método es POST y si el campo oculto "_method" es DELETE
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        url = f"https://comunicaciones.simix.com.ar/v1/comunicaciones/public/planta/{planta_id}"

        # Realizamos la solicitud DELETE a la API
        response = requests.delete(url)

        # Imprimir el código de estado y el contenido de la respuesta para depuración
        print(f"DELETE status: {response.status_code}")
        print(f"DELETE response content: {response.text}")

        # Manejar los diferentes códigos de respuesta
        if response.status_code in (204, 200):  # Ajustar según la API
            return redirect('mis_plantas')  # Redirigir a la vista 'mis_plantas'
        else:
            # Si hay algún error, mostramos la página de confirmación con el error
            return render(request, 'frontendapp/eliminar_planta.html', {
                'error': 'Error al eliminar la planta. Inténtalo de nuevo.',
                'planta_id': planta_id
            })

    # Si no es POST, mostramos la página de confirmación
    return render(request, 'frontendapp/eliminar_planta.html', {'planta_id': planta_id})

