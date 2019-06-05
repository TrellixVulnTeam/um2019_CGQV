from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from Usuario.forms import SignupForm, SigninForm
from Publicacion.forms import PublicacionForm

# Views

def frontpage(request):
  if request.user.is_authenticated: 
    #si ya esta logeado que vaya al perfil del usuario
    return redirect('/' + request.user.username + '/')
  else:
    if request.method == 'POST': #si estoy queriendo loguearme
      if 'signupform' in request.POST:
        #si es por signUP
        signupform = SignupForm(data=request.POST)
        signinform = SigninForm()
        
        if signupform.is_valid():
          username = signupform.cleaned_data['username']
          password = signupform.cleaned_data['password1']
          signupform.save()
          user = authenticate(username=username, password=password)
          login(request, user)
          return redirect('/')
      else:
        #si es por signIN
        signupform = SignupForm()
        signinform = SigninForm(data=request.POST)

        if signinform.is_valid():
          login(request, signinform.get_user())
          return redirect('/')
    else:
      #muestro pelado
      signupform = SignupForm()
      signinform = SigninForm()
  
    return render(request, 'frontpage.html', {'signupform': signupform, 'signinform': signinform})

def signout(request):
  logout(request)
  return redirect('/')

def profile(request, username): 
  if request.user.is_authenticated:
    user = User.objects.get(username=username)
    
    if request.method == 'POST':
      form = PublicacionForm(data=request.POST)

      if form.is_valid():
        Publicacion = form.save(commit=False)
        Publicacion.user = request.user
        Publicacion.save()
        
        redirecturl = request.POST.get('redirect', '/')

        return redirect(redirecturl)
    else:
      form = PublicacionForm()

    return render(request, 'profile.html', {'form': form, 'user': user})
  else:
    return redirect('/')