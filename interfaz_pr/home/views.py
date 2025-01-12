from django.shortcuts import render, redirect
from .models import Task
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


def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'inicio.html')

def cfunciona(request):
    return render(request, 'cfunciona.html')

def casos(request):
    return render(request, 'casos.html')



def valoraciones(request):
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

    return render(request, 'valoraciones.html', {'options_json': options_json})

@csrf_exempt
def ventas(request):
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
            nueva_valoracion = {
                "modo":data.get("modo"),
                "ciudad": data.get("ciudad"),
                "distrito": data.get("distrito"),
                "barrio": data.get("barrio"),
                "tipo_vivienda": data.get("tipo_vivienda"),
                "metros_cuadrados": data.get("m2"),
                "num_habitaciones": data.get("num_habitaciones"),
                "num_banos": data.get("num_banos"),
                "planta": data.get("planta"),
                "terraza": data.get("terraza"),
                "balcon": data.get("balcon"),
                "ascensor": data.get("ascensor"),
                "estado_inmueble": data.get("estado"),
                "fecha_guardado": datetime.now().strftime('%d/%m/%Y')  
            }
    
            folder_path = os.path.join(settings.BASE_DIR, 'home')
            file_path = os.path.join(folder_path, 'valoraciones.json')

            if not os.path.exists(folder_path):
                print("Carpeta no existe, creando...")
                os.makedirs(folder_path)

            try:
                with open(file_path, 'r') as file:
                    valoraciones = json.load(file)
            except FileNotFoundError:
                print("Archivo no encontrado, creando uno nuevo...")
                valoraciones = []

            valoraciones.append(nueva_valoracion)

            with open(file_path, 'w') as file:
                json.dump(valoraciones, file, indent=4)
                print("Datos guardados en el archivo:", file_path)

            return JsonResponse({"message": "Valoración guardada correctamente", "data": nueva_valoracion})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def user_login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/home/valoraciones')
                else:
                    messages.error(request, 'Tu cuenta está desactivada. Por favor, contacta al administrador.')
            else:
                messages.error(request, 'No se pudo completar el inicio de sesión. Intenta nuevamente.')
    else:
        form = LoginForms()
    return render(request, 'login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.error(request, 'Registration successful! You can now log in.')
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

