from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlantaForm
from .models import Planta
import random
import requests
from django.http import JsonResponse
import json
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
            planta = form.save(commit=False)
            # Hacer la solicitud a la API
            url = "https://comunicaciones.simix.com.ar/v1/comunicaciones/public/planta"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                planta.nombre = data['nombre']  # Nombre de la respuesta de la API
                planta.especie = data['especie']  # Especie de la respuesta de la API
            else:
                return render(request, 'error.html', {'mensaje': 'Error al acceder a la API'})

            planta.estado = form.cleaned_data['estado']
            planta.descripcion = form.cleaned_data['descripcion']

            planta.save()
            return redirect('mis_plantas')
    else:
        form = PlantaForm()
    return render(request, 'frontendapp/subir_imagen.html', {'form': form})

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

def obtener_planta(request):
    if request.method == "POST" and request.FILES.get('imagen'):
        url = "https://comunicaciones.simix.com.ar/v1/comunicaciones/public/planta"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            nombre = data['nombre']
            especie = data['especie']
            return render(request, 'resultado.html', {'nombre': nombre, 'especie': especie})
        else:
            return render(request, 'error.html', {'mensaje': 'Error al acceder a la API'})
    
    return render(request, 'subir_imagen.html')

# Endpoints

def listar_plantas(request):
    plantas = Planta.objects.all().values('id', 'nombre', 'imagen', 'especie', 'estado', 'descripcion')
    return JsonResponse(list(plantas), safe=False)

def obtener_planta(request, id):
    planta = get_object_or_404(Planta, id=id)
    data = {
        'id': planta.id,
        'nombre': planta.nombre,
        'imagen': planta.imagen.url,
        'especie': planta.especie,
        'estado': planta.estado,
        'descripcion': planta.descripcion
    }
    return JsonResponse(data)

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

@csrf_exempt  # Usar solo si no tienes autenticación
def eliminar_planta(request, id):
    planta = get_object_or_404(Planta, id=id)
    if request.method == 'DELETE':
        planta.delete()
        return JsonResponse({'message': 'Planta eliminada'}, status=204)
