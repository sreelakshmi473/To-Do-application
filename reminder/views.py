from django.shortcuts import render,redirect
from django.views.generic import View
from reminder.forms import register,Signin,Taskform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from reminder.models import Task 
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.n   
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
   
def mylogin(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Task.objects.get(id=id)
        if obj.user != request.user:
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
   
class registerview(View):
    def get(self,request,*args,**kwargs):
        form=register()
        return render(request,"reg.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form = register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)      

        return render(request,"reg.html",{"form":form})
    
class Signview(View):
    def get(self,request,*args,**kwargs):
        form=Signin()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=Signin(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            # email=form.cleaned_data.get("email")
            user_obj=authenticate(request,username=u_name,password=pwd)
            print(user_obj)
            if user_obj:
              print("valid")
              login(request,user_obj)
              subject= "logined successfully"
            #   message = 'thankyou for login'
            #   email_from = settings.EMAIL_HOST_USER
            #   recipient_list = [user_obj.email,]
            #   send_mail(subject, message,email_from,recipient_list)
              return redirect("index")
            else:
              print("invalid")
        return render(request,"signin.html",{"form":form})
    
@method_decorator(signin_required,name = 'dispatch')
class Taskview(View):
    def get(self,request,*args,**kwargs):
        form=Taskform()
        data=Task.objects.filter(user=request.user).order_by('complete')
        return render(request,"index.html",{"form":form,"data":data})
    
    def post(self,request,*args,**kwargs):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user #it will retrn to a table user 
            form.save() # save i database
        else:
            print("get out")
        form=Taskform()
        data=Task.objects.filter(user=request.user)
        return render(request,"index.html",{"form":form,"data":data})
        
class Signout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")

@method_decorator(mylogin, name='dispatch')
class Taskupdate(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        if qs.complete == True:
            qs.complete=False
            qs.save()
        elif qs.complete == False:
            qs.complete=True
            qs.save()
        return redirect("index")

@method_decorator(mylogin, name='dispatch')
class Taskdelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.filter(id=id).delete()
        return redirect("index")
    
class user_del(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        User.objects.get(id=id).delete()
        return redirect("reg")