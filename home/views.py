from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect, get_object_or_404,reverse
from django.contrib import messages
from home.models import *
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    # return redirect('repairhome.html')  
    catg=Category.objects.all()
    return render(request,"home.html",{"cate":catg})
def repairhome(request):
    return render(request,"repairhome.html",{})
def aboutus(request):
	return render(request,"aboutus.html" ,{})
def contactus(request):
    return render(request,'contactus.html',{})
def services(request):
	sr=Service.objects.all()
	return render(request,'services.html',{"ser":sr})
def services1(request,sid):
	stg=repair_centre.objects.get(id=sid)
	sr=Service.objects.filter(rep=stg)
	return render(request,"services.html",{"ser":sr})
def repaircentre(request):
	rr=repair_centre.objects.all()
	return render(request,'repaircentre.html',{"rer":rr})
def repaircentre1(request,rid):
	rtg=Category.objects.get(id=rid)
	rr=repair_centre.objects.filter(cate=rtg)
	return render(request,"repaircentre.html",{"rer":rr})
def Cart(request):
	dic={}
	item=cart.objects.filter(usr_id=request.user.id,status=False)
	dic["item"]=item
	if request.user.is_authenticated:
		if request.method=="POST":
			sid=request.POST["sid"]
			quantity=request.POST["qty"]
			is_exist=cart.objects.filter(service_id=sid,usr_id=request.user.id,status="False")
			if len(is_exist)>0:
				dic["msg"]="Item already exist in your cart."
			else:
				srvc=get_object_or_404(Service,id=sid)
				usr=get_object_or_404(User,id=request.user.id)
				crt=cart(usr=usr,service=srvc,quantity=quantity)
				crt.save()
				dic["msg"]="{} Added in your cart.".format(srvc.name_ser)
				dic["cls"]="alert alert success"
		else:
				dic["status"]="Please login first to view your cart."
	return render(request,"cart.html",dic)
def remove_ser(request):
	if "delete_cart" in request.GET:
		id=request.GET["delete_cart"]
		cartobj=get_object_or_404(cart,id=id)
		cartobj.delete()
	return HttpResponse(1)
def get_cart_data(request):
	item=cart.objects.filter(usr_id=request.user.id,status=False)
	sale,quantity=0,0
	for i in item:
		sale+=float(i.service.price_ser)*i.quantity
		quantity=quantity+int(i.quantity)
	resp={"quan":quantity,"tot":sale}
	return JsonResponse(resp)
def checkout(request):
	return render(request,"checkout.html",{})
def cash_on_delivery(request):
    items = cart.objects.filter(usr_id=request.user.id,status=False)
    products=""
    amt=0
    inv = "INV10001-"
    cart_ids = ""
    p_ids =""
    for j in items:
        products += str(j.service.name_ser)+"\n"
        p_ids += str(j.service.id)+","
        amt += float(j.service.price_ser)/75
        inv +=  str(j.id)
        cart_ids += str(j.id)+","
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id
    return redirect('viewbookings')
    # return render(request,'viewbookings.html')
def viewbook(request):
    obj=Order.objects.filter(cust_id=request.user.id)
    bkngs=bookingdetails.objects.filter(usr_id=request.user.id)
    blngs=billingdetails.objects.filter(usr_id=request.user.id)
    return render(request,"viewbookings.html",{"orderview":obj,"bkn":bkngs,"bill":blngs})

def process_payment(request):
    items = cart.objects.filter(cust_id=request.user.id,status=False)
    products=""
    amt=0
    inv = "INV10001-"
    cart_ids = ""
    p_ids =""
    for j in items:
        products += str(j.service.name_ser)+"\n"
        p_ids += str(j.service.id)+","
        amt += float(j.service.price_ser)/75
        inv +=  str(j.id)
        cart_ids += str(j.id)+","
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
    }
    usr = User.objects.get(username=request.user.username)
    ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})

def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()      
        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    return render(request,"payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_failed.html")
def search(request):
    dic={}
    if request.method=='GET':
        sr=request.GET['search']
        xyz=Category.objects.filter(name_cat__icontains=sr)
        if len(xyz)>0:
            dic['cro']=xyz
        else:
            Service.objects.filter(name_ser__icontains=sr)
            dic['cro']=xyz 
    return render (request,"home.html",dic)
def Contact(request):
    usr=contact.objects.filter(usr_id=request.user.id)
    if request.method=="POST":
        phone=request.POST['phone']
        content=request.POST['content']
        print(phone, content)
        if len(phone)<10 or len(content)<4:
            messages.info(request, "Field Error")
        else:
            usr=get_object_or_404(User,id=request.user.id)
            con=contact(usr=usr,phone=phone,msg=content)
            con.save()
            messages.info(request, "Message send successfully...")
    return render(request, "contactus.html")
def repairaj(request):
    rep=repair_centre.objects.filter(usr_id=request.user.id)
    if len(rep)>0:
        rep=repair_centre.objects.filter(usr_id=request.user.id)
    return render (request,"repairhome.html",{"rep":rep})
def add_ser(request):
    if request.method=="POST":
        namesr=request.POST['ser1']
        desser=request.POST['descser1']
        pricesr=request.POST['priceser1']
        ra=repair_centre.objects.get(usr_id=request.user.id)
        addser=Service(rep=ra,name_ser=namesr,desc_ser=desser,price_ser=pricesr)
        addser.save()
        if "imgs" in request.FILES:
            img=request.FILES["imgs"]
            addser.img_ser=img
            addser.save()
            messages.info(request, "Service Added Successfully...")
            return redirect("addser")
    return render(request,'addcatser.html')
def bookingdet(request):
    usr=bookingdetails.objects.filter(usr_id=request.user.id)
    if request.method=="POST":
        sn=request.POST['sname']
        sm=request.POST['smod']
        sp=request.POST['sproblem']
        sd=request.POST['sdat']
        usr=get_object_or_404(User,id=request.user.id)
        bookdetails=bookingdetails(usr=usr,servicename=sn,modelname=sm,prob_desc=sp,date_desc=sd)
        bookdetails.save()
        messages.info(request,"Details added successfully!")
    return render(request,'bookingdetails.html',{})
def billingdet(request):
    usr=billingdetails.objects.filter(usr_id=request.user.id)
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        em=request.POST['email']
        ph_pro=request.POST['ph_pro']
        state=request.POST['state']
        city=request.POST['city']
        street=request.POST['street']
        od=request.POST['details']
        usr=get_object_or_404(User,id=request.user.id)
        billdetails=billingdetails(usr=usr,fname=fname,lname=lname,email=em,ph_pro=ph_pro,state=state,city=city,street=street,det=od)
        billdetails.save()
        messages.info(request,"Billing Details have been added")
    return render(request,"checkout.html")
def tracking(request):
    return render(request,"track.html")
def shopdesc(request):
    rr=repair_centre.objects.filter(usr_id=request.user.id)
    return render(request,"shopdesc.html",{"rer":rr})
def postreview(request, prid):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    customer = User.objects.get(user_id=current_user.id)
    if request.method == "POST":
        subject = request.POST['subject']
        review = request.POST['review']
        rating = request.POST['rating']
        product_review = Review(
            product_id = prid,
            customer_id = customer.id,
            subject = subject,
            review = review,
            rating = rating,
        )
        product_review.save()
        messages.success(request, "Review Posted")
        return HttpResponseRedirect(url)
# def cancelProduct(request):

#     if "delete_order" in request.GET:
#         id=request.GET["delete_order"]
# 	    orderobj=get_object_or_404(Order,id=id)
# 		orderobj.delete()
#     return HttpResponse(1)
def cancelProduct(request):
	if "delete_cart" in request.GET:
		id=request.GET["delete_cart"]
		cartobj=get_object_or_404(Order,id=id)
		cartobj.delete()
	return redirect('viewbookings')    
def feed(request):
    usr=contact.objects.filter(usr_id=request.user.id)
    if request.method=="POST":
        title=request.POST['title']
        revbody=request.POST['revbody']
        print(title, revbody)
        usr=get_object_or_404(User,id=request.user.id)
        con=feedback(usr=usr,title=title,revbody=revbody)
        con.save()
        messages.info(request, "Feedback send successfully...")
    return redirect('viewbookings')