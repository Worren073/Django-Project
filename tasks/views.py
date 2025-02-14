from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import TaskForm

# Create your views here.

#Pagina Home
def home(request):
    return render(request, 'home.html')

#Pagina de registro
def signup(request):

        if request.method == 'GET':
                return render(request, 'signup.html', {
            'form': UserCreationForm  
            }) 
                
        else:
            if request.POST['password1'] == request.POST['password2']:
                
                try:
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('tasks') 
                
                except:
                    return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existente', 
                    })
            
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Las contraseñas no coinciden', 
                    })

#Pagina de tareas            
def tasks(request):
   return render(request, 'tasks.html')   

#Seccion de creacion de tareas    
def create_task(request):
     
    if request.method == 'GET':
         return render(request, 'create_task.html', {
        'form': TaskForm
         })   
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Por favor provee un dato valido',
         })   
                          
                
def signout(request):
    logout(request)
    return redirect('home')

#Pagina de inicio de sesion
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'] )
        
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña incorrecta',
            })
        else:
            login(request, user)
            return redirect('tasks')
