from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
@login_required            
def tasks(request):
   tasks = Task.objects.filter(user = request.user, date_completed__isnull=True)

   return render(request, 'tasks.html', {'tasks': tasks})   

#Seccion de creacion de tareas 
@login_required   
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

#Pagina para ver los detalles de las tareas
@login_required        
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})

    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error actualizando la tarea"})

#Funcion para completar una tarea
@login_required  
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save
        return redirect('tasks') 

#Pagina de lista de tareas completadas
@login_required  
def tasks_completed(request):
   tasks = Task.objects.filter(user = request.user, date_completed__isnull=False).order_by('-date_completed')

   return render(request, 'tasks.html', {'tasks': tasks})   

#Funcion para eliminar una tarea
@login_required  
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')                  

#Funcion para cerrar sesion
@login_required                  
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
