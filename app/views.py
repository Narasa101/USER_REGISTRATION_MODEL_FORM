from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from app.forms import *
from django.core.mail import send_mail

def home(request):
    return render(request,'home.html')

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if PD.is_valid() and UD.is_valid():
            pw=UD.cleaned_data['password']
            UFO=UD.save(commit=False)
            UFO.set_password(pw)
            UFO.save()

            PFO=PD.save(commit=False)
            PFO.user=UFO
            PFO.save()

            send_mail('User registration',
            'Regiistration is success full',
            'harshadvali1432@gmail.com',
            [UFO.email],fail_silently=False)


            return HttpResponse('registration is successsfull')
            
    return render(request,'registration.html',d)