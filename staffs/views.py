from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import render,get_object_or_404,redirect
from products.models import (Products,Category,Stocks,
                            AttributeName,AttributeValue,Payment,
                            ProductChangePriceAttributes,Orders)
from datetime import date
from .forms import (ProductForm,ProductChangePriceAttributesForm,
                    ProductAttributesForm,StocksForm,AttributeNameForm)
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from geopy.geocoders import Nominatim
from django.contrib.admin.views.decorators import staff_member_required

geolocator = Nominatim(user_agent="Blink")


today = date.today()

# Create your views here.
@staff_member_required(login_url='/')
def home(request):
    return render(request,'staffs/pages/homepage.html')

@staff_member_required(login_url='/')
def create_attribute_name(request):
    if request.is_ajax and request.method == "POST":
        attribute_name=AttributeName(a_name=request.POST.get('a_name',False))
        attribute_name.save()
        return JsonResponse({'attribute_name_id':attribute_name.id,'attribute_name_a_name':attribute_name.a_name})
    else:
        return JsonResponse({"error": "please enter valid"}, status=400)


##################### Attrbiute Names ######3

def create_attribute_names(request):
    AttributeNameFormset = modelformset_factory(AttributeName, form=AttributeNameForm)
    formset = AttributeNameFormset(request.POST or None, queryset=AttributeName.objects.none(), prefix='name')
    if request.method == "POST":
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for attribute in formset:
                        attribute.save()
                    messages.success(request, f"Your Attribute Name is Created")
            except Exception as e:
                messages.warning(request, f"Please Check Again.Invalid Data")
            return redirect('create_attribute')
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
    context = {
        'formset': formset,
    }

    return render(request,'staffs/pages/attribute_name.html',context)


##################### AttributeValue ##################3

@staff_member_required(login_url='/')
def create_attribute(request):
    AttributeValueFormset = modelformset_factory(AttributeValue, form=ProductAttributesForm)
    formset = AttributeValueFormset(request.POST or None, queryset=AttributeValue.objects.none(), prefix='name')
    if request.method == "POST":
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for attribute in formset:
                        attribute.save()
                    messages.success(request, f"Your Attribute Value is Created")
            except Exception as e:
                messages.warning(request, f"Please Check Again.Invalid Data")
            return redirect('product_attribute_list')
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
    context = {
        'formset': formset,
    }
    return render(request,'staffs/pages/attribute.html',context)

@staff_member_required(login_url='/')
def update_attribute(request,id):
    attribute_instance=get_object_or_404(AttributeValue,id=id)
    if request.method=="POST":
        forms=ProductAttributesForm(request.POST,instance=attribute_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Attribute is Updated")
            return redirect(product_update_attribute,id=attribute_instance.id)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/attribute.html',{"forms":forms})
    else:
        forms=ProductAttributesForm(instance=attribute_instance)
        return render(request,'staffs/pages/attribute.html',{"forms":forms})
    return render(request,'staffs/pages/attribute.html',{'forms':forms})


@staff_member_required(login_url='/')
##################### ProductAttribute ################
def product_attribute_list(request):
    product_attributes=Stocks.objects.all().values('product_id__id','product_id__productchangepriceattributes__id','product_id__p_name','product_id__productchangepriceattributes__price','product_id__productchangepriceattributes__attribute_values__a_value','product_id__productchangepriceattributes__attribute_values__a_name__a_name')
    return render(request,'staffs/pages/product_attribute_list.html',{'product_attributes':product_attributes})


@staff_member_required(login_url='/')
def create_product_attribute(request,pid):
    product_instance=get_object_or_404(Products,id=pid)
    if request.method=="POST":
        # request.POST['pid']=[str(pid)]
        forms=ProductChangePriceAttributesForm(request.POST)
        if forms.is_valid():
            forms.save(commit=False)
            attribute_values=forms.cleaned_data['attribute_values']
            price=forms.cleaned_data['price']
            product_attribute=ProductChangePriceAttributes(price=price,p_id=product_instance)
            product_attribute.save()
            product_attribute.attribute_values.add(*attribute_values)
            product_attribute.save()

            messages.success(request, f"Your Product is Created")
            return redirect(product_update,id=pid)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/product_attribute.html',{"forms":forms})
    else:
        forms=ProductChangePriceAttributesForm()
        return render(request,'staffs/pages/product_attribute.html',{"forms":forms})
    return render(request,'staffs/pages/product_attribute.html',{'forms':forms})

@staff_member_required(login_url='/')
def product_update_attribute(request,pid,id):
    product_instance=get_object_or_404(Products,id=pid)
    product_attribute_instance=get_object_or_404(ProductChangePriceAttributes,id=id)
    if request.method=="POST":
        forms=ProductChangePriceAttributesForm(request.POST,instance=product_attribute_instance)
        if forms.is_valid():
            obj=forms.save()
            obj.p_id_id=pid
            obj.save()
            messages.success(request, f"Your Product's Attribute is Updated")
            return redirect(product_update,id=pid)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/product_attribute.html',{"forms":forms})
    else:
        forms=ProductChangePriceAttributesForm(instance=product_attribute_instance)
        return render(request,'staffs/pages/product_attribute.html',{"forms":forms})
    return render(request,'staffs/pages/product_attribute.html',{'forms':forms})


######################## Product #########################
@staff_member_required(login_url='/')
def product_list(request):
    products=Products.objects.all()
    return render(request,'staffs/pages/product_list.html',{'products':products})

@staff_member_required(login_url='/')
def product_add(request):
    if request.method=="POST":
        forms=ProductForm(request.POST,request.FILES)
        if forms.is_valid():
            obj=forms.save() 
            messages.success(request, f"Your Product is Created")
            return redirect('product_update',id=obj.pk)
        else:
            # print(">>>>>>>>",forms.errors)
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/product_update.html',{"forms":forms})
    else:
        forms=ProductForm()
        return render(request,'staffs/pages/product_update.html',{"forms":forms})
    return render(request,'staffs/pages/product_update.html',{'forms':forms})

@staff_member_required(login_url='/')
def product_update(request,id):
    product_instance=get_object_or_404(Products,id=id)
    p_attrs=product_instance.productchangepriceattributes_set.values('id','attribute_values__a_name__a_name','attribute_values__a_value','price')
    if request.method=="POST":
        forms=ProductForm(request.POST,request.FILES,instance=product_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Product is Updated")
            return redirect(product_update,id=product_instance.id)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/product_update.html',{"forms":forms,'p_attrs':p_attrs,'pid':id})
    else:
        forms=ProductForm(instance=product_instance)
        return render(request,'staffs/pages/product_update.html',{"forms":forms,'p_attrs':p_attrs,'pid':id})
    return render(request,'staffs/pages/product_update.html',{'forms':forms,'p_attrs':p_attrs,'pid':id})

########## Stock ######################
@staff_member_required(login_url='/')
def stock_list(request):
    stocks=Stocks.objects.filter(stock_day__year=today.year, stock_day__month=today.month, stock_day__day=today.day)
    return render(request,'staffs/pages/stock_list.html',{'stocks':stocks})

@staff_member_required(login_url='/')
def stock_create(request):
    if request.method=="POST":
        forms=StocksForm(request.POST)
        if forms.is_valid():
            obj=forms.save(commit=False)
            stock=Stocks.objects.create(shop_id=request.user.store_set.first(),
                            product_id=forms.cleaned_data['product_id'],
                            total_qty=forms.cleaned_data['total_qty'],
                            left_qty=forms.cleaned_data['left_qty'],
                            on_alert_qty=forms.cleaned_data['on_alert_qty'],
                            finished=False)
            stock.save()
            messages.success(request, f"Your Stocks is Created")
            return redirect(stock_update,id=stock.id)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/stock_update.html',{"forms":forms})
    else:
        forms=StocksForm()
        return render(request,'staffs/pages/stock_update.html',{"forms":forms})
    return render(request,'staffs/pages/stock_update.html',{'forms':forms})

@staff_member_required(login_url='/')
def stock_update(request,id):
    stock_instance=get_object_or_404(Stocks,id=id)
    if request.method=="POST":
        forms=StocksForm(request.POST,instance=stock_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Stocks is Updated")
            return redirect(stock_update,id=stock_instance.id)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/stock_update.html',{"forms":forms,'stock_instance':stock_instance})
    else:
        forms=StocksForm(instance=stock_instance)
        return render(request,'staffs/pages/stock_update.html',{"forms":forms,'stock_instance':stock_instance})
    return render(request,'staffs/pages/stock_update.html',{'forms':forms,'stock_instance':stock_instance})


####################Deals Of the day##################

@staff_member_required(login_url='/')
def deals_of_day_list(request):
    deals_of_days=Deals_of_day.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
    return render(request,'staffs/pages/deals_of_day_list.html',{'deals_of_days':deals_of_days})

@staff_member_required(login_url='/')
def update_deals_of_the_day(request,id):
    deals_of_the_day_instance=get_object_or_404(Deals_of_day,id=id)
    if request.method=="POST":
        forms=Deals_of_dayForm(request.POST,instance=deals_of_the_day_instance)
        if forms.is_valid():
            forms.save() 
            messages.success(request, f"Your Deals of the day is Updated")
            return redirect(update_deals_of_the_day,id=deals_of_the_day_instance.id)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/deals_of_day_update.html',{"forms":forms})
    else:
        forms=Deals_of_dayForm(instance=deals_of_the_day_instance)
        return render(request,'staffs/pages/deals_of_day_update.html',{"forms":forms})
    return render(request,'staffs/pages/deals_of_day_update.html',{'forms':forms})
 
@staff_member_required(login_url='/')
def create_deals_of_the_day(request):
    if request.method=="POST":
        forms=Deals_of_dayForm(request.POST)
        if forms.is_valid():
            obj=forms.save() 
            messages.success(request, f"Your Deals of the day is Created")
            return redirect(update_deals_of_the_day,id=obj.id)
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/deals_of_day_update.html',{"forms":forms})
    else:
        forms=Deals_of_dayForm()
        return render(request,'staffs/pages/deals_of_day_update.html',{"forms":forms})
    return render(request,'staffs/pages/deals_of_day_update.html',{'forms':forms})
 
 #########################################################

@staff_member_required(login_url='/')
def orderlists(request,status='order_confirm'):
    orders=Orders.objects.filter(created_at__year=today.year, created_at__month=today.month, created_at__day=today.day,order_status=status)
    # orders=Orders.objects.filter(order_status=status)
    return render(request,'staffs/pages/orderlists.html',{'orderlist':orders,'Status':status})

@staff_member_required(login_url='/')
def single_order(request,order_id):
    order=Orders.objects.get(orderid=order_id)
    return render(request,'staffs/pages/single_order.html',{'order':order})

@staff_member_required(login_url='/')
def paymentlists(request,status='SUCCESS'):
    payments=Payment.objects.filter(created_at__year=today.year, created_at__month=today.month, created_at__day=today.day,status=status)
    # payments=Payment.objects.filter(status=status)
    return render(request,'staffs/pages/paymentlists.html',{'paymentlist':payments,'Status':status})

