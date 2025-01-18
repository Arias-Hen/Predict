from django.shortcuts import render, redirect
from .models import Users
import csv
import json
import os
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import load_data, save_data
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForms, RegistrationForm
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.auth import get_user_model
from .models import Valoracion

def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'inicio.html')

def cfunciona(request):
    return render(request, 'cfunciona.html')

def casos(request):
    return render(request, 'casos.html')

@login_required
def valoraciones(request):
    options = []
    user = request.user
    user_id = user.uniqueid
    user_nombre = user.nombre
    print(f"EL ID DEL USUARIO: {user_id}")
    print(f"EL ID DEL USUARIO: {user}") 
    try:
        with open('distritos.csv', newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            cities = set()  
            for row in reader:
                if 'ciudad' in row:
                    cities.add(row['ciudad'])

            options = [{'id': ciudad, 'name': ciudad} for ciudad in cities]

        if options:
            options_json = json.dumps(options)
        else:
            options_json = '[]'

    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        options_json = '[]'

    return render(request, 'valoraciones.html', {'options_json': options_json, 'user_id': user_id, 'user_nombre': user_nombre})

@csrf_exempt
@login_required
def ventas(request):
    user_id = request.user.uniqueid
    context = []  
    context_json = '{}' 
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            context = {
                'modo': data.get('modo', ''),
                'ciudad': data.get('ciudad', ''),
                'distrito': data.get('distrito', ''),
                'barrio': data.get('barrio', ''),
                'tipo_vivienda': data.get('tipo_vivienda', ''),
                'm2': data.get('m2', ''),
                'num_habitaciones': data.get('num_habitaciones', ''),
                'num_banos': data.get('num_banos', ''),
                'planta': data.get('planta', ''),
                'terraza': data.get('terraza', ''),
                'balcon': data.get('balcon', ''),
                'ascensor': data.get('ascensor', ''),
                'estado': data.get('estado', ''),
                'precio_minimo': data.get('precio_minimo', ''),
                'precio_esperado': data.get('precio_esperado', ''),
                'precio_maximo': data.get('precio_maximo', ''),
                'precio_esperado_unico': data.get('precio_esperado_unico', ''),
                
            }
            
            request.session['context_json'] = json.dumps(context)
            
            context_json = json.dumps(context)
        except json.JSONDecodeError:
            context['error'] = 'Datos JSON inválidos.'

    context_json = request.session.get('context_json', '{}')

    options = []
    try:
        with open('distritos.csv', newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            cities = set()  
            for row in reader:
                if 'ciudad' in row:
                    cities.add(row['ciudad'])

            options = [{'id': ciudad, 'name': ciudad} for ciudad in cities]

        if options:
            options_json = json.dumps(options)
        else:
            options_json = '[]'
    
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        options_json = '[]'
    valoraciones = []
    try:
        valoraciones_qs = Valoracion.objects.filter(iduser=user_id)
        for val in valoraciones_qs:
            valoraciones.append({
                'modo': val.modo,
                'ciudad': val.ciudad,
                'distrito': val.distrito,
                'barrio': val.barrio,
                'tipo_vivienda': val.tipo_vivienda,
                'm2': val.metros_cuadrados,
                'num_habitaciones': val.num_habitaciones,
                'num_banos': val.num_banos,
                'planta': val.planta,
                'terraza': val.terraza,
                'balcon': val.balcon,
                'ascensor': val.ascensor,
                'estado': val.estado_inmueble,
                'fecha_guardado': val.fecha_guardado.strftime('%d/%m/%Y'),
            })
    except FileNotFoundError:
        print("Archivo de valoraciones no encontrado.")
    return render(request, 'ventas.html', {'options_json': options_json, 'context_json': context_json, 'valoraciones':valoraciones})

@csrf_exempt
def informes(request):
    context = []  
    context_json = '{}' 
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            context = {
                'ciudad': data.get('ciudad', ''),
                'distrito': data.get('distrito', ''),
                'barrio': data.get('barrio', ''),
                'tipo_vivienda': data.get('tipo_vivienda', ''),
                'm2': data.get('m2', ''),
                'num_habitaciones': data.get('num_habitaciones', ''),
                'num_banos': data.get('num_banos', ''),
                'planta': data.get('planta', ''),
                'terraza': data.get('terraza', ''),
                'balcon': data.get('balcon', ''),
                'ascensor': data.get('ascensor', ''),
                'estado': data.get('estado', ''),
                'precio_minimo': data.get('precio_minimo', ''),
                'precio_esperado': data.get('precio_esperado', ''),
                'precio_maximo': data.get('precio_maximo', ''),
                'precio_esperado_unico': data.get('precio_esperado_unico', ''),
                
            }
            
            request.session['context_json'] = json.dumps(context)
            
            context_json = json.dumps(context)
        except json.JSONDecodeError:
            context['error'] = 'Datos JSON inválidos.'

    context_json = request.session.get('context_json', '{}')

    options = []
    try:
        with open('distritos.csv', newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            cities = set()  
            for row in reader:
                if 'ciudad' in row:
                    cities.add(row['ciudad'])

            options = [{'id': ciudad, 'name': ciudad} for ciudad in cities]

        if options:
            options_json = json.dumps(options)
        else:
            options_json = '[]'
    
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        options_json = '[]'
    valoraciones = []
    file_path = os.path.join(settings.BASE_DIR, 'home', 'valoraciones.json')

    try:
        with open(file_path, 'r') as file:
            valoraciones = json.load(file)
    except FileNotFoundError:
        print("Archivo de valoraciones no encontrado.")
    return render(request, 'informes.html', {'options_json': options_json, 'context_json': context_json, 'valoraciones':valoraciones})

def generarinf(request):
    return render(request, 'generarinf.html')

def get_distritos(request, ciudad):
    distritos = []
    try:
        with open('distritos.csv', newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['ciudad'] == ciudad:
                    distritos.append({'id': row['distrito'], 'name': row['distrito']})

        return JsonResponse({'distritos': distritos})

    except Exception as e:
        print(f"Error al leer el archivo CSV para distritos: {e}")
        return JsonResponse({'distritos': []})
    
def get_barrios(request, distrito):
    barrios = []
    try:
        with open('distrito_barrio.csv', newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['distrito'] == distrito:
                    barrios.append({'id': row['barrio'], 'name': row['barrio']})

        return JsonResponse({'barrio': barrios})

    except Exception as e:
        print(f"Error al leer el archivo CSV para barrios: {e}")
        return JsonResponse({'barrio': []})
    
def guardar_valoracion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Crear una nueva instancia de Valoracion y guardarla en la base de datos
            nueva_valoracion = Valoracion.objects.create(
                idv = data.get("idv"),
                iduser = data.get("iduser"),
                modo=data.get("modo"),
                ciudad=data.get("ciudad"),
                distrito=data.get("distrito"),
                barrio=data.get("barrio"),
                tipo_vivienda=data.get("tipo_vivienda"),
                metros_cuadrados=data.get("m2"),
                num_habitaciones=data.get("num_habitaciones"),
                num_banos=data.get("num_banos"),
                planta=data.get("planta"),
                terraza=bool(data.get("terraza")), 
                balcon=bool(data.get("balcon")),   
                ascensor=bool(data.get("ascensor")), 
                estado_inmueble=data.get("estado"),
            )

            return JsonResponse({
                "message": "Valoración guardada correctamente",
                "data": {
                    "idv" : nueva_valoracion.idv,
                    "iduser": nueva_valoracion.iduser,
                    "modo": nueva_valoracion.modo,
                    "ciudad": nueva_valoracion.ciudad,
                    "distrito": nueva_valoracion.distrito,
                    "barrio": nueva_valoracion.barrio,
                    "tipo_vivienda": nueva_valoracion.tipo_vivienda,
                    "metros_cuadrados": nueva_valoracion.metros_cuadrados,
                    "num_habitaciones": nueva_valoracion.num_habitaciones,
                    "num_banos": nueva_valoracion.num_banos,
                    "planta": nueva_valoracion.planta,
                    "terraza": nueva_valoracion.terraza,
                    "balcon": nueva_valoracion.balcon,
                    "ascensor": nueva_valoracion.ascensor,
                    "estado_inmueble": nueva_valoracion.estado_inmueble,
                    "fecha_guardado": nueva_valoracion.fecha_guardado,
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def user_login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', '/home/valoraciones/')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Cuenta desactivada. Contacta al administrador.')
            else:
                messages.error(request, 'Credenciales inválidas.')
    else:
        form = LoginForms()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Users.objects.filter(usuario=cd['username']).exists():
                messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.')
            else:
                try:
                    new_user = Users(
                        usuario=cd['username'],
                        empresa='Mi Empresa',
                        nombre=cd['username'],
                        password=make_password(cd['password']),
                        estado=True
                    )
                    new_user.save()
                    messages.success(request, 'Registro exitoso! Ahora puedes iniciar sesión.')
                    return redirect('/home/login')
                except IntegrityError:
                    messages.error(request, 'Hubo un error al registrar el usuario. Intenta nuevamente.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def exportar_excel(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            seleccionados = body.get('seleccionados', [])

            if not seleccionados:
                return HttpResponse("No hay datos seleccionados", status=400)

            df = pd.DataFrame(seleccionados)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="valoraciones_seleccionadas.xlsx"'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Datos Seleccionados')

            return response
        except Exception as e:
            print(f"Error al exportar Excel: {e}")
            return HttpResponse(f"Error interno: {e}", status=500)
    else:
        return HttpResponse("Método no permitido", status=405)

def contacto(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        correo_electronico = request.POST.get('correo_electronico')
        telefono = request.POST.get('telefono')
        nombre_empresa = request.POST.get('nombre_empresa')
        cargo_rol = request.POST.get('cargo_rol')
        motivo_consulta = request.POST.get('motivo_consulta')
        terms = request.POST.get('terms')

        if terms != 'on':
            return JsonResponse({"message": "Debe aceptar los términos y condiciones"}, status=400)

        asunto = "Solicitud de demostración gratuita"
        mensaje = f"""
        Nombre Completo: {nombre_completo}
        Correo Electrónico: {correo_electronico}
        Teléfono: {telefono}
        Nombre de la Empresa: {nombre_empresa}
        Cargo/Rol: {cargo_rol}
        Motivo de la Consulta: {motivo_consulta}
        """
        try:
            send_mail(
                asunto,
                mensaje,
                correo_electronico, 
                ['jhonhendrick.ja@gmail.com'], 
                fail_silently=False,
            )
            return JsonResponse({"message": "Formulario enviado correctamente. ¡Gracias por tu interés!"})
        except Exception as e:
            return JsonResponse({"message": f"Hubo un error al enviar el correo: {e}"}, status=500)

    return render(request, 'contacto.html')
