from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import render,get_object_or_404,redirect

from products.forms import CategoryForm, CategoryFormSet, SubCategoryForm, SubCategoryFormSet
from products.models import (Products, Category, Stocks,
                             AttributeName, AttributeValue, Payment,
                             ProductChangePriceAttributes, Orders, Subcategory, Vouchers)
from datetime import date
from .forms import (ProductForm, ProductChangePriceAttributesForm,
                    ProductAttributesForm, StocksForm, AttributeNameForm, AttributeNameFormSet, AttributeValueFormSet,
                    ProductChangePriceAttributesFormSet, VouchersForm)
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


########### Product Category #########

def create_category(request):
    ProductCategoryFormSet = modelformset_factory(Category, form=CategoryForm,formset=CategoryFormSet)
    formset = ProductCategoryFormSet(request.POST or None, queryset=Category.objects.none(), prefix='category')
    if request.method == "POST":
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for category in formset:
                        category.save()
                messages.success(request, f"Your Category is Created")
            except Exception as e:
                print(">>>>e",e)
                messages.warning(request, f"Please Check Again,Invalid Data")
            return redirect('list_category')
        else:
            for error in formset.non_form_errors():
                messages.warning(request, error)
    context = {
        'formset': formset,
    }
    return render(request,'staffs/pages/category.html',context)

def list_category(request):
    categories = Category.objects.all()
    return render(request,'staffs/pages/category_list.html',{'categories':categories})

def update_category(request,id):
    category_instance=get_object_or_404(Category,id=id)
    if request.method=="POST":
        forms=CategoryForm(request.POST,instance=category_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Category is Updated")
            return redirect('list_category')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
            return render(request,'staffs/pages/category.html',{"forms":forms})
    else:
        forms=CategoryForm(instance=category_instance)
        return render(request,'staffs/pages/category.html',{"forms":forms})
    return render(request,'staffs/pages/category.html',{'forms':forms})


@staff_member_required(login_url='/')
def remove_category(request,id):
    category_instance=Category.objects.filter(id=id)
    category_instance.delete()
    messages.success(request, f"Your Category has been removed")
    return redirect('list_category')

############ Sub Category ################3

@staff_member_required(login_url='/')
def create_attribute_name(request):
    if request.is_ajax and request.method == "POST":
        attribute_name=AttributeName(a_name=request.POST.get('a_name',False))
        attribute_name.save()
        return JsonResponse({'attribute_name_id':attribute_name.id,'attribute_name_a_name':attribute_name.a_name})
    else:
        return JsonResponse({"error": "please enter valid"}, status=400)


########### Product Sub Category #########

def create_sub_category(request):
    ProductSubCategoryFormSet = modelformset_factory(Subcategory, form=SubCategoryForm,formset=SubCategoryFormSet)
    formset = ProductSubCategoryFormSet(request.POST or None, queryset=Subcategory.objects.none(), prefix='subcategory')
    if request.method == "POST":
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for subcategory in formset:
                        subcategory.save()
                messages.success(request, f"Your Sub-Category is Created")
            except Exception as e:
                print(">>>>e",e)
                messages.warning(request, f"Please Check Again,Invalid Data")
            return redirect('list_sub_category')
        else:
            for error in formset.non_form_errors():
                messages.warning(request, error)
    context = {
        'formset': formset,
    }
    return render(request,'staffs/pages/sub_category.html',context)

def list_sub_category(request):
    subcategories = Subcategory.objects.all()
    return render(request,'staffs/pages/sub_category_list.html',{'subcategories':subcategories})

def update_sub_category(request,id):
    sub_category_instance=get_object_or_404(Subcategory,id=id)
    if request.method=="POST":
        forms=SubCategoryForm(request.POST,instance=sub_category_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Sub Category is Updated")
            return redirect('list_sub_category')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
            return render(request,'staffs/pages/sub_category.html',{"forms":forms})
    else:
        forms=SubCategoryForm(instance=sub_category_instance)
        return render(request,'staffs/pages/sub_category.html',{"forms":forms})
    return render(request,'staffs/pages/sub_category.html',{'forms':forms})


@staff_member_required(login_url='/')
def remove_sub_category(request,id):
    subcategory_instance=Subcategory.objects.filter(id=id)
    subcategory_instance.delete()
    messages.success(request, f"Your Sub Category has been removed")
    return redirect('list_sub_category')


##################### Attrbiute Names ######3
@staff_member_required(login_url='/')
def create_attribute_names(request):
    AttributeNameFormset = modelformset_factory(AttributeName, form=AttributeNameForm,formset=AttributeNameFormSet)
    formset = AttributeNameFormset(request.POST or None, queryset=AttributeName.objects.none(), prefix='name')
    if request.method == "POST":
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for attribute in formset:
                        attribute.save()
                messages.success(request, f"Your Attribute Name is Created")
            except Exception as e:
                print(">>>>e",e)
                messages.warning(request, f"Please Check Again,Invalid Data")
            return redirect('create_attribute')
        else:
            for error in formset.non_form_errors():
                messages.warning(request, error)
    context = {
        'formset': formset,
    }
    return render(request,'staffs/pages/attribute_name.html',context)


@staff_member_required(login_url='/')
def update_attribute_names(request,id):
    attribute_name_instance=get_object_or_404(AttributeName,id=id)
    if request.method=="POST":
        forms=AttributeNameForm(request.POST,instance=attribute_name_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Attribute Name is Updated")
            return redirect('list_attribute_name')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
            return render(request,'staffs/pages/attribute_name.html',{"forms":forms})
    else:
        forms=AttributeNameForm(instance=attribute_name_instance)
        return render(request,'staffs/pages/attribute_name.html',{"forms":forms})
    return render(request,'staffs/pages/attribute_name.html',{'forms':forms})

@staff_member_required(login_url='/')
def list_attribute_name(request):
    attribute_names=AttributeName.objects.all()
    return render(request,'staffs/pages/attribute_name_list.html',{'attribute_names':attribute_names})

@staff_member_required(login_url='/')
def remove_attribute_names(request,id):
    attribute_name_instance=AttributeName.objects.filter(id=id)
    attribute_name_instance.delete()
    messages.success(request, f"Your Attribute Name has been removed")
    return redirect('list_attribute_name')


##################### AttributeValue ##################3

@staff_member_required(login_url='/')
def create_attribute(request):
    AttributeValueForm = modelformset_factory(AttributeValue, form=ProductAttributesForm,formset=AttributeNameFormSet)
    formset = AttributeValueForm(request.POST or None, queryset=AttributeValue.objects.none(), prefix='name')
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
            for error in formset.non_form_errors():
                messages.warning(request, error)
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
            return redirect('product_attribute_list')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
            return render(request,'staffs/pages/attribute.html',{"forms":forms})
    else:
        forms=ProductAttributesForm(instance=attribute_instance)
        return render(request,'staffs/pages/attribute.html',{"forms":forms})
    return render(request,'staffs/pages/attribute.html',{'forms':forms})

@staff_member_required(login_url='/')
def remove_attribute(request,id):
    attribute_instance=AttributeValue.objects.filter(id=id)
    attribute_instance.delete()
    messages.success(request, f"Your Attribute has been removed")
    return redirect('product_attribute_list')

@staff_member_required(login_url='/')
def product_attribute_list(request):
    product_attributes=AttributeValue.objects.all()
    return render(request,'staffs/pages/product_attribute_list.html',{'product_attributes':product_attributes})


##################### ProductAttribute ################

@staff_member_required(login_url='/')
def create_product_attribute(request,pid):
    product_instance=get_object_or_404(Products,id=pid)
    if request.method=="POST":
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


def get_attribute_values(request):
    if request.method == 'GET':
        a_name_id = request.GET.get('a_name_id')
        attribute_values = AttributeValue.objects.filter(a_name_id=a_name_id)
        values = [{'id': obj.id, 'value': obj.a_value} for obj in attribute_values]
        return JsonResponse({'values': values})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@staff_member_required(login_url='/')
def product_add(request):
    formset = ProductChangePriceAttributesFormSet(request.POST or None)
    forms = ProductForm(request.POST or None, request.FILES or None)

    if request.method=="POST":
        if forms.is_valid() and formset.is_valid():
            product_obj=forms.save()
            formset.instance = product_obj
            formset.save()
            messages.success(request, f"Your Product is Created")
            return redirect('product_list')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
            return render(request,'staffs/pages/product_update.html',{"forms":forms,'formset':formset})
    else:
        return render(request,'staffs/pages/product_update.html',{"forms":forms,'formset':formset})
    return render(request,'staffs/pages/product_update.html',{"forms":forms,'formset':formset})

@staff_member_required(login_url='/')
def product_update(request,id):
    product_instance=get_object_or_404(Products,id=id)
    formset = ProductChangePriceAttributesFormSet(request.POST or None,instance = product_instance,queryset=product_instance.productchangepriceattributes_set.all())
    forms = ProductForm(request.POST or None, request.FILES or None,instance=product_instance)

    if request.method=="POST":
        if forms.is_valid() and formset.is_valid():
            product_obj = forms.save()
            formset.instance = product_obj
            formset.save()
            messages.success(request, f"Your Product is Updated")
            return redirect('product_list')
        else:
            print(">>>",formset.errors)
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/product_update.html',{"forms":forms,'formset':formset,'pid':id})
    return render(request, 'staffs/pages/product_update.html', {"forms": forms, 'formset': formset,'pid':id})

@staff_member_required(login_url='/')
def product_delete(request, id):
    product_instance = Products.objects.filter(id=id)
    product_instance.delete()
    messages.success(request, f"Your Product has been removed")
    return redirect('product_list')


####### Vouchers #####
@staff_member_required(login_url='/')
def create_voucher(request):
    forms = VouchersForm(request.POST or None)
    if request.method=="POST":
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Voucher is Created")
            return redirect('list_vouchers')
        else:

            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/voucher.html',{'forms':forms})

@staff_member_required(login_url='/')
def list_vouchers(request):
    vouchers=Vouchers.objects.all()
    return render(request,'staffs/pages/voucher_list.html',{'vouchers':vouchers})

@staff_member_required(login_url='/')
def update_status_voucher(request,id,type):
    voucher = Vouchers.objects.get(id=id)
    voucher.stop = bool(type)
    voucher.save()
    return redirect('list_vouchers')


@staff_member_required(login_url='/')
def update_voucher(request,id):
    voucher_instance=get_object_or_404(Vouchers,id=id)
    forms = VouchersForm(request.POST, instance=voucher_instance)
    if request.method=="POST":
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Voucher is Updated")
            return redirect('list_vouchers')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/voucher.html',{'forms':forms})

@staff_member_required(login_url='/')
def delete_voucher(request, id):
    voucher_instance = Vouchers.objects.filter(id=id)
    voucher_instance.delete()
    messages.success(request, f"Your Vouhcer has been removed")
    return redirect('list_vouchers')


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

