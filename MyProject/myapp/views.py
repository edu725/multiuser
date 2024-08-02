from django.shortcuts import redirect, render
from myapp.models import  *
from myapp.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from myapp.decorators import user_is_admin, user_is_client

# Create your views here.

def index(request):
    return render(request, 'myapp/index.html',{"itens": Itens.objects.all()})

def create(request):
    form = ItensForm
    if request.method == "POST":
        form = ItensForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'item cadastrada com sucesso!')
            return redirect('index')
        
    return render(request, "myapp/create.html", {"forms":form})



def edit(request, id):
    item = Itens.objects.get(pk=id)
    form = ItensForm(instance=item)
    return render(request, "myapp/update.html",{"form":form, "item":item})


def update(request, id):
    try:
        if request.method == "POST":
            item = Itens.objects.get(pk=id)
            form = ItensForm(request.POST, request.FILES, instance=item)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'item foi alterada com sucesso!')
                return redirect('index')
    except Exception as e:
        messages.error(request, e)
        return redirect('index')
            

def read(request, id):
    item = Itens.objects.get(pk=id)
    return render(request, "myapp/read.html", {"item":item})

def delete(request, id):
    item = Itens.objects.get(pk=id)
    item.delete()
    messages.success(request, 'item foi deletada com sucesso!')
    return redirect('index')

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/signup.html',{'form':form})

@login_required
@user_passes_test(user_is_admin)
def admin_page(request):
    return render(request, 'myapp/dashbord_admin.html')

@login_required
@user_passes_test(user_is_client)
def client_page(request):
    return render(request, 'myapp/dashbord_client.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashbord_admin' if user.user_type == 'admin' else 'dashbord_client')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')