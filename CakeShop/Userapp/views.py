from django.shortcuts import render,redirect
from Adminapp.models import Category,Cake
from Userapp.models import UserInfo,Cart,Payments
from django.http import HttpResponse

# Create your views here.
def Homepage(request):
    cats=Category.objects.all()
    cakes=Cake.objects.all()
    return render(request,'Master.html',{'cats':cats ,'cakes':cakes})

def Showcake(request,cid):
    cats=Category.objects.all()
    cate=Category.objects.get(id=cid) #here we first we find that which category is selected.
    cakes=Cake.objects.filter(category=cate) #here we find how many cakes are present having category same as selected one.
    #here we used filter because filter will provide one more objects that have value but when we use get it provide only single object at a time and if thier are one more than it give error.
    return render(request,'Master.html',{'cats':cats , 'cakes':cakes})

def Viewdetails(request,id):
    cats=Category.objects.all()
    cake=Cake.objects.get(id=id)
    return render(request,'Viewdetails.html',{'cake':cake , 'cats':cats})

def Login(request):
    cats=Category.objects.all()
    if(request.method=='GET'):
        return render(request,'Login.html',{'cats':cats})
    
    else:
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        try:
            user=UserInfo.objects.get(username=uname,password=pwd)
        except:
            return redirect(Login)
        else:
            request.session['uname']=uname
            return redirect(Homepage)

def Signup(request):
    cats=Category.objects.all()
    if(request.method=='GET'):
        return render(request,'Signup.html',{'cats':cats})
    
    else:
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        email=request.POST['email']

        user=UserInfo(uname,pwd,email)
        user.save()
        return redirect(Homepage)

def Logout(request):
    request.session.clear()
    return redirect(Homepage)

def addTocart(request):
    if(request.method=='POST'):
        
        if('uname' in request.session):

            user=UserInfo.objects.get(username=request.session['uname'])
            cake=Cake.objects.get(id=request.POST['cake_id'])
            qty=request.POST['qty']

            try:
             cart_item=Cart.objects.get(user= user ,cake=cake)
          
            except:
             cart_item=Cart()
             cart_item.user=user
             cart_item.cake= cake
             cart_item.qty= qty
             cart_item.save()
             return redirect(Homepage)

            else:
             return HttpResponse('you have allready added this ...')

        else:
          return redirect(Login)       
    else:
        return redirect(Login)


def ShowAllCartItems(request):
    uname=request.session['uname']
    user=UserInfo.objects.get(username=uname)
    if(request.method=='GET'):
        cats=Category.objects.all()
        items=Cart.objects.filter(user=user)
        total=0
        for p in items:
          total+=float(p.cake.price) * int(p.qty)
        request.session['total']=total
        return render(request,'ShowAllCartItems.html',{'items':items,'cats':cats})
    
    else:
        action=request.POST['action']
        cakeid=request.POST['cakeid']
        cake=Cake.objects.get(id=cakeid)
        item=Cart.objects.get(user=user,cake=cake)
        qty=request.POST['qty']
        if(action =='update'):
            item.qty=qty
            item.save()
            return redirect(ShowAllCartItems)

        else: 
            item.delete()
            return redirect(ShowAllCartItems)

def Makepayment(request):
    cats=Category.objects.all()
    if(request.method=='GET'):
       return render(request,'Makepayment.html',{'cats':cats})
    
    else: 
        card_no=request.POST['card_no']
        expiry=request.POST['expiry']
        cvv=request.POST['cvv']
        total=request.session['total']
        uname=request.session['uname']
        user=UserInfo.objects.get(username=uname)
        admin=Payments.objects.get(card_no='111',expiry='6/2025',cvv='111')
        cart_item=Cart.objects.filter(user=user)
        try:
            user=Payments.objects.get(card_no=card_no,expiry=expiry,cvv=cvv)
        
        except:
            return render(request,'Makepayment.html',{'msg':'Please Enter Correct Payment details...'})
        
        else:
            user.balance-=total
            user.save()
            admin.balance+=total
            admin.save()
            cart_item.delete()
            return HttpResponse('Your Order Is Placed Successfully...')



            
        
              




