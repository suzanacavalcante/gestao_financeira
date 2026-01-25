from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def cadastro(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usuario = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {usuario}')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/cadastro.html', {'form': form})

@login_required # Garante acesso somente a quem estiver logado
def profile(request):
    return render(request, 'accounts/profile.html')