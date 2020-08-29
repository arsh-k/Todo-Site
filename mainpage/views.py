from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#Home Page
def home(request):
    return render(request, 'mainpage/home.html')

#Authentication
def signupuser(request):
    if request.method == "GET":
        return render(request, 'signup/register.html', {'form' : UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'signup/register.html', {'form' : UserCreationForm(), 'error' : 'The entered username ALREADY EXISTS'})
        else:
            return render(request, 'signup/register.html', {'form' : UserCreationForm(), 'error' : 'The Passwords DO NOT MATCH'})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == "GET":
        return render(request, 'login/loginpage.html', {'form' : AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login/loginpage.html', {'form': AuthenticationForm(), 'error': 'USER DOES NOT EXIST. Incorrect password or username may have been entered. '})
        else:
            login(request, user)
            return redirect('currenttodos')

# Todo Page
@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user = request.user, completion__isnull = True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form' : TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', { 'form' : TodoForm(), 'error' : 'Data error!' })

@login_required
def viewtodo(request, mytodo_pk):
    mytodo = get_object_or_404(Todo, pk = mytodo_pk, user=request.user )
    if request.method == 'GET':
        form = TodoForm(instance = mytodo)
        return render(request, 'todo/mytodo.html', { 'mytodo' : mytodo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=mytodo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/mytodo.html', {'mytodo' : mytodo, 'form' : form, 'error' : 'Data error!'})

@login_required
def completedtodo(request, mytodo_pk):
    todo = get_object_or_404(Todo, pk= mytodo_pk, user = request.user)
    if request.method == 'POST':
        todo.completion = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, mytodo_pk):
    todo = get_object_or_404(Todo, pk= mytodo_pk, user = request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user = request.user, completion__isnull = False).order_by('-completion')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

@login_required
def clearcompleted(request):
    todos = Todo.objects.filter(user = request.user, completion__isnull = False)
    if request.method == 'POST':
        todos.delete()
        return redirect('completedtodos')
