from sre_parse import CATEGORIES
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from  home.models import *
# Create your views here.
def register(request):
    if request.method=="POST":
        fn=request.POST['fname']
        ln=request.POST['lname']
        un=request.POST['uname']
        em=request.POST['email']
        paw=request.POST['pwd']
        cpaw=request.POST['pwd_2']
        print(fn)
        print(ln)
        print(un)
        print(em)
        print(paw)
        if paw==cpaw:
            usr=User.objects.create_user(username=un,first_name=fn,last_name=ln,email=em,password=paw)
            usr.save()
            pf=profile(usr=usr)
            pf.save()
            return redirect("lgt")
        else:
            messages.info(request,"Password not matching")
            return redirect("reg")
    return render(request,"reg.html")

def login(request):
    if(request.method=="POST"):
        uname=request.POST['uname']
        pas=request.POST['pwd']
        user=auth.authenticate(username=uname,password=pas)
        print(uname,pas,user)
        if user != None:
            if user.is_staff==True:
                auth.login(request,user)
                return redirect("repaj")
            else:
                auth.login(request,user)
            
                auth.login(request,user)
            
            return redirect('home')
        else:
              messages.info(request,"invalid credentials")
              return redirect('lgt')       
    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('home')
def Prof(request):
    dis={}
    pro=profile.objects.filter(usr_id=request.user.id)
    if len(pro)>0:
        prf=profile.objects.get(usr_id=request.user.id)
        dis['prd']=prf
    return render(request,'profile.html',dis)
def uppro(request):
    display={}
    prof=profile.objects.filter(usr_id=request.user.id)
    if len(prof)>0:
        dis=profile.objects.get(usr_id=request.user.id)
        display["data"]=dis
        if request.method=="POST":
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email=request.POST['email']
            ph_pro=request.POST['ph_no']
            state=request.POST['state']
            city=request.POST['city']
            street=request.POST['street']

            up_user=User.objects.get(id=request.user.id)
            up_user.first_name=fname
            up_user.last_name=lname
            up_user.email=email
            up_user.save()
            dis.ph_pro=ph_pro
            dis.state=state
            dis.city=city
            dis.street=street
            dis.save()
            if "imgs" in request.FILES:
                img=request.FILES["imgs"]
                dis.img_pro=img
                dis.save()
                messages.info(request,"Image uploaded successfully")
                return redirect("uppro")
            messages.info(request,"profile uploaded successfully")
            return redirect("uppro")
    return render(request,"uppro.html",display)

def RRegister(request):
    cate=Category.objects.all()
    if request.method=='POST':
        rn=request.POST['rname']
        un=request.POST['uname']
        em=request.POST['email']
        ph_pro=request.POST['ph_no']
        state=request.POST['state']
        city=request.POST['city']
        street=request.POST['street']
        pww=request.POST['pww']
        cpw=request.POST['cpw']
        cate=request.POST['ct']
        cte=get_object_or_404(Category,id=cate)
        if pww==cpw:
            if (User.objects.filter(username=un)).exists():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
                messages.info(request,"Repair Centre already exists")
                return redirect('rreg') 
            else:
                repcentre=User.objects.create_user(username=un,first_name=rn,email=em,password=pww)
                if "accept" in request.POST:
                    repcentre.is_staff=True
                    repcentre.save()
                ppf=profile(usr=repcentre,ph_pro=ph_pro,state=state,city=city,street=street)
                ppf.save()
                if "imgs" in request.FILES:
                    img=request.FILES["imgs"]
                    ppf.img_pro=img
                    ppf.save()
                    messages.info(request,"Image uploaded successfully")
                rep=repair_centre(cate=cte,usr=repcentre,profile=ppf,name_re=rn) 
                rep.save()
                messages.success(request,'CONGRATULATIONS! Your Repair Centre details are successfully added.')
                return redirect('lgt')
        else:
            messages.info(request,"Password doesnot match")
            return redirect('rreg')   
    return render(request,'RRegister.html',{"cate":cate})


























