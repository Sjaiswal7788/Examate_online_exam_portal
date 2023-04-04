from django.shortcuts import render,redirect
from django.http import HttpResponse
from examate.models import Post
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from examate.forms import UserReg
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


# Create your views here.
def about(request):
    return HttpResponse("Hello from about")

def base(request):
    return render(request,'base.html')

def contact(request):
    return render(request,'contact.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def index(request):
    return render(request,'index.html')

def header(request):
    return render(request,'header.html')

def footer(request):
    return render(request,'footer.html')


def createexam(request):

    if  request.method=="POST":
        stitle=request.POST['stitle']
        que=request.POST['que']
        date=request.POST['date']
        time=request.POST['time']
        year=request.POST['year']
        userid=request.session['user_id']
        token= str(uuid.uuid4())

        p=Post.objects.create(stitle=stitle,que=que,date=date,time=time,year=year,uid=userid,auth_token = token)
        p.save()

        subject = 'Start Your Exam'
        message =f'hi past the link to start your exam http://127.0.0.1:8000/submitexam/{token}/' + year
        
        studEmail = student.objects.filter(year = year)
        emailList = []

        for s in studEmail:
            emailList.append(s.email)


        email_from = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, email_from, emailList) 
        except Exception as e:
            print(e)
            messages.error(request, "Check your internet connection")
            return redirect('/cexam')


        return redirect('/udash')

    else:
        
        return render(request,'createexam.html')

def login(request):
    if request.method=='POST':
        uemail=request.POST['uemail']
        upass=request.POST['upass']
        u=authenticate(username=uemail,password=upass)
        
        if u is not None:
            u=User.objects.get(username=u)
            
            request.session['user_id']=u.id   

            return redirect('/udash') 
        else:
            err={}
            err['msg']="Invalid User"
            return render(request,'login.html') 
    else:
        return render(request,'login.html')
          
        

def register(request):
    if request.method=='POST':
        email=request.POST['uemail']
        upass=request.POST['upass']
        cupass=request.POST['cupass']
        
        if User.objects.filter(username = email).first():
            messages.success(request,'username is taken.')
            return redirect('/register')

       
        if User.objects.filter(email = email).first():
            messages.success(request,'email is taken.')
            return redirect('/register')
            
       

        User_obj = User.objects.create(username = email, email = email)
        User_obj.set_password(upass)
        User_obj.save()
        auth_token= str(uuid.uuid4())

        profile_obj = Profile.objects.create(user = User_obj, auth_token = auth_token)
        profile_obj.save()
        send_mail_after_register(email, auth_token)
        return redirect('/token')

        

    else:
        return render(request,'register.html')


def send_mail_after_register(email,token):
    subject = 'Your account need to verified'
    message =f'hi past the link to varify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list= [email]
    send_mail(subject, message, email_from, recipient_list) 


def edit(request,rid):
    if request.method=="POST":
        ustitle=request.POST['stitle']
        uque=request.POST['que']
        udate=request.POST['date']
        utime=request.POST['time']
        uyear=request.POST['year']

        p=Post.objects.filter(id=rid)

        p.update(stitle=ustitle,que=uque,date=udate,time=utime,year=uyear)
        
        return redirect('/udash')

    else:
        p=Post.objects.filter(id=rid)
        content={}
        content['data']=p
    
        return render(request,'editexam.html',content)

def addque(request,rid):
    
    if request.method == "POST":
        uque=request.POST['que']
        p=Post.objects.filter(id=rid)

        p.update(que=uque)
        
        return redirect('/udash')
        
    else:
        content={}
        content['id']=rid
        return render(request,'que.html',content)


def delete(request,rid):
    
    p=Post.objects.get(id=rid)   
    p.delete()
    return redirect('/udash')

def dashboard(request):
    
    if request.session.get('user_id'):
        userid=request.session['user_id']
        p=Post.objects.filter(uid=userid)
        content={}
        content['data']=p
        return render(request,'dashboard.html',content)
    else:
        return redirect('/login')

def user_logout(request):

    del request.session['user_id']
    return redirect('/login')

def mail_vari(request):
    return render(request,'mail_vari.html')

def token_send(request):
    return render(request,'token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')

    except Exception as e:
        print(e)

def error(request):
    return render(request,'error.html')


def addstudent(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email'] 
        year = request.POST['year']
    
        p=student.objects.create(name=name,email=email,year=year)
        p.save()
        return redirect('/studentdash')
    else:
        return render(request,'addstudent.html')


def sedit(request,rid):
    if request.method=="POST":
        uname=request.POST['name']
        uemail=request.POST['email']
        uyear=request.POST['year']

        p=student.objects.filter(id=rid)

        p.update(name=uname,email=uemail,year=uyear)
        
        return redirect('/studentdash')
    
    else:
        p=student.objects.filter(id=rid)
        content={}
        content['data']=p
        return render(request,'editstudent.html',content)


def studentdash(request):
        p=student.objects.all()
        content={}
        content['data']=p
        return render(request,'studentdash.html',content)


def sdelete(request,rid):
    
    p=student.objects.get(id=rid)   
    p.delete()
    return redirect('/studentdash')

def subexam(request,auth_token,rid):
    try:
        profile_obj = Post.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            p=Post.objects.filter(year=rid)
            content={}
            content['data']=p
            return render(request,'submitexam.html',content)

        else:
            return redirect('/error')

    except Exception as e:
        print(e)
    # if request.session.get('id'):
        # que=request.session['que']
    # p=Post.objects.filter(year=rid)
    # content={}
    # content['data']=p
    # return render(request,'submitexam.html',content)

    # else:
    #     return render(request,'submitexam.html')





def user_reg(request):
    if request.method=='POST':
        content={}
        fmdata=UserReg(request.POST)
        if fmdata.is_valid():
            fmdata.save()
            content['msg']="User created Successfully, Please login"
            print("User created Successfully")

        else:
            content["msg"]="failed to User create "
        
        return render(request,'user_reg.html',content)
    else:
        fm=UserReg()
        content={}
        content['regdata']=fm
        return render(request,'user_reg.html',content)


def userlogin(request):

    content={}
    content['logfmdata']=AuthenticationForm()

    if request.method=="POST":
        fmdata=AuthenticationForm(request=request, data=request.POST)
        if fmdata.is_valid():
            uname=fmdata.cleaned_data['username']
            upass=fmdata.cleaned_data['password']
            u=authenticate(username=uname, password=upass)
            # print(u)
            if u is not None:
                login(request,u)
                return redirect('/udash')
            else:
                content['msg']="Invalid Username and Password!!!"

    else:
        return render(request,'user_login.html',content)
        
    
        