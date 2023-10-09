import csv

from django.db import transaction
from django.forms import modelformset_factory
from django.shortcuts import render,get_object_or_404,redirect
from easyaudit.models import CRUDEvent

from products.forms import CategoryForm, CategoryFormSet, SubCategoryForm, SubCategoryFormSet
from products.models import (Products, Category, Stocks,
                             AttributeName, AttributeValue, Payment,
                             ProductChangePriceAttributes, Orders, Subcategory, Vouchers, Warehouse, Delivery)
from users.forms import EmployeeSalaryForm
from users.models import User, EmployeeSalary
from datetime import date
import datetime
from django.db.models import Q
from users.models import Employee
from .forms import (ProductForm, ProductChangePriceAttributesForm,
                    ProductAttributesForm, StocksForm, AttributeNameForm, AttributeNameFormSet, AttributeValueFormSet,
                    ProductChangePriceAttributesFormSet, VouchersForm, WarehouseForm, EmployeeForm, UserForm,
                    DeliveryForm, LedgerForm, LedgerLineForm)
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from geopy.geocoders import Nominatim
from django.contrib.admin.views.decorators import staff_member_required
from utils.helper_functions import get_attribute_full_name, get_warehouse_dict, get_orders_count_by_date, \
    get_pagination_records
from itertools import chain
from django.contrib.admin.models import LogEntry

from .models import OrderPrepare, Ledger

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
    categories = get_pagination_records(request,categories)
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
    subcategories = get_pagination_records(request,subcategories)
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
    attribute_names = get_pagination_records(request,attribute_names)
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
    product_attributes = get_pagination_records(request,product_attributes)
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
    products = get_pagination_records(request,products)
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
    vouchers=Vouchers.objects.filter(is_deleted=False)
    vouchers = get_pagination_records(request,vouchers)
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
    if request.method=="POST":
        forms = VouchersForm(request.POST, instance=voucher_instance)

        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Voucher is Updated")
            return redirect('list_vouchers')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    forms = VouchersForm(instance=voucher_instance)
    return render(request,'staffs/pages/voucher.html',{'forms':forms})

@staff_member_required(login_url='/')
def delete_voucher(request, id):
    voucher_instance = Vouchers.objects.get(id=id)
    voucher_instance.is_deleted =True
    voucher_instance.save()
    messages.success(request, f"Your Voucher has been removed")
    return redirect('list_vouchers')


########## Stock ######################
@staff_member_required(login_url='/')
def stock_list(request):
    # stocks=Stocks.objects.filter(stock_day__year=today.year, stock_day__month=today.month, stock_day__day=today.day)
    stocks=Stocks.objects.all()
    stocks = get_pagination_records(request,stocks)
    return render(request,'staffs/pages/stock_list.html',{'stocks':stocks})

def get_differenced_ids(list1,list2):
    set1 = set(list1)
    set2 = set(list2)
    difference = list(set2 - set1)
    return difference

def get_product_by_warehouse(request):
    warehouse_id = request.GET.get('warehouse_id')
    if warehouse_id:
        stocks = Stocks.objects.filter(warehouse_id=warehouse_id,finished=False)
        product_ids = stocks.values('product_id').distinct()
        ### product objects
        warehouse_products = Products.objects.filter(id__in=product_ids)
        ## product with its attribute available
        total_product_attribute_ids = warehouse_products.values_list('productchangepriceattributes__id', flat=True)
        product_availble_from_stocks = [stock.product_id.productchangepriceattributes_set.filter(~Q(id=stock.product_attributes_id)) for stock in stocks]
        product_availble_from_stocks_ids = get_differenced_ids([i.id for i in list(chain(*product_availble_from_stocks))], list(total_product_attribute_ids))
        product_ids_from_warehouse = ProductChangePriceAttributes.objects.filter(id__in=product_availble_from_stocks_ids).values_list('p_id',
                                                                                                         flat=True)
        products = Products.objects.filter(Q(id__in=product_ids_from_warehouse)).union(
            Products.objects.filter(~Q(id__in=[i.p_id.id for i in list(chain(*product_availble_from_stocks))])))
        # warehouse_products sent for div
        return JsonResponse({'products':list(products.values('p_name','id')),'warehouse_products':[]})

    else:
        return JsonResponse({'products':[],'warehouse_products':[]})


def get_product_attrs_by_product_warehouse(request):
    warehouse_id = request.GET.get('warehouse_id')
    product_id = request.GET.get('product_id')
    if warehouse_id and product_id:
        selected_product = Products.objects.get(id=product_id)
        product_attributes = selected_product.productchangepriceattributes_set.all()

        stocks = Stocks.objects.filter(warehouse_id=warehouse_id,product_id=product_id, finished=False)
        if stocks:
            product_attributes_ids = stocks.values_list('product_attributes', flat=True)
            product_attributes = selected_product.productchangepriceattributes_set.filter(~Q(id__in=[product_attributes_ids]))
        print((">>>>>>>>>>>>>\n\n\n"))
        return JsonResponse({'product_attributes': [(product_attribute.id,str(product_attribute)) for product_attribute in product_attributes]})
    else:
        return JsonResponse({'product_attributes':[]})

@staff_member_required(login_url='/')
def stock_create(request):
    if request.method=="POST":
        forms=StocksForm(request.POST)
        if forms.is_valid():
            stock = forms.save()
            messages.success(request, f"Your Stocks is Created")
            return redirect('stock_list')
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/stock.html',{"forms":forms})
    else:
        forms=StocksForm()
        return render(request,'staffs/pages/stock.html',{"forms":forms})
    return render(request,'staffs/pages/stock.html',{'forms':forms})


@staff_member_required(login_url='/')
def stock_update(request,id):
    stock_instance=get_object_or_404(Stocks,id=id)
    if request.method=="POST":
        forms=StocksForm(request.POST,instance=stock_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Stocks is Updated")
            return redirect('stock_list')
        else:
            messages.warning(request, f"Please Check Again.Invalid Data")
            return render(request,'staffs/pages/stock.html',{"forms":forms,'stock_instance':stock_instance})
    else:
        forms=StocksForm(instance=stock_instance)
        return render(request,'staffs/pages/stock.html',{"forms":forms,'stock_instance':stock_instance})
    return render(request,'staffs/pages/stock.html',{'forms':forms,'stock_instance':stock_instance})


@staff_member_required(login_url='/')
def stock_finish(request, id):
    stock_instance = Stocks.objects.get(id=id)
    stock_instance.finished=True
    stock_instance.save()
    messages.success(request, f"Your Stock has been finished successfully")
    return redirect('stock_list')


 #########################################################

@staff_member_required(login_url='/')
def orderlists(request,status='order_confirm'):
    orders=Orders.objects.filter(order_status=status)
    orders = get_pagination_records(request,orders)
    return render(request,'staffs/pages/orderlists.html',{'orderlist':orders,'Status':status})

@staff_member_required(login_url='/')
def single_order(request,order_id):
    order=Orders.objects.get(orderid=order_id)
    return render(request,'staffs/pages/single_order.html',{'order':order})

@staff_member_required(login_url='/')
def paymentlists(request,status='SUCCESS'):
    payments=Payment.objects.filter(status=status)
    payments = get_pagination_records(request,payments)
    return render(request,'staffs/pages/paymentlists.html',{'paymentlist':payments,'Status':status})


######## Employee ###########

def create_employee(request):
    user_forms = UserForm(request.POST or None)
    employee_forms = EmployeeForm(request.POST or None)
    if request.method=="POST":
        if user_forms.is_valid() and employee_forms.is_valid():
            user = user_forms.save()
            employee = employee_forms.save(commit=False)
            employee.user = user
            employee.save()

            messages.success(request, f"Your Employee is Created")
            return redirect('list_employees')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/employee.html',{'user_forms':user_forms,'employee_forms':employee_forms})

@staff_member_required(login_url='/')
def list_employees(request):
    employees=Employee.objects.all()
    employees = get_pagination_records(request,employees)

    return render(request,'staffs/pages/employee_list.html',{'employees':employees})

@staff_member_required(login_url='/')
def update_employee(request,id):
    employee_instance=get_object_or_404(Employee,id=id)
    user_instance=get_object_or_404(User,id=employee_instance.user.id)
    user_form = UserForm(instance=user_instance)
    employee_form = EmployeeForm(instance=employee_instance)
    if request.method=="POST":
        user_form = UserForm(request.POST,instance=user_instance)
        employee_form = EmployeeForm(request.POST,instance=employee_instance)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            messages.success(request, f"Your Employee is Updated")
            return redirect('list_employees')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/employee.html',{'user_forms':user_form,'employee_forms':employee_form})

@staff_member_required(login_url='/')
def delete_employee(request, id):
    employee_instance = Employee.objects.filter(id=id)
    employee_instance.delete()
    messages.success(request, f"Your Employee has been removed")
    return redirect('list_employees')

######### Employee Salary ##########

@staff_member_required(login_url='/')
def create_employee_salary(request,id):
    employee = Employee.objects.get(id=id)
    forms = EmployeeSalaryForm(request.POST or None)
    forms.instance.employee_id = employee.id

    if request.method == "POST":
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Salary for Employee is Created")
            return redirect('employee_salary_list',id=id)
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/employee_salary.html',{'forms':forms,'employee':employee})

@staff_member_required(login_url='/')
def employee_salary_list(request,id):
    employee_salary = EmployeeSalary.objects.filter(employee_id=id)
    employee_salary = get_pagination_records(request,employee_salary)
    return render(request,'staffs/pages/employee_salary_list.html',{'employee_salary':employee_salary,'employee_id':id})
@staff_member_required(login_url='/')
def update_employee_salary(request,id):
    employee_salary = get_object_or_404(EmployeeSalary,id=id)
    employee = Employee.objects.get(id=employee_salary.employee_id)
    forms = EmployeeSalaryForm(instance=employee_salary)

    forms.instance.employee_id = employee.id

    if request.method == "POST":
        forms = EmployeeSalaryForm(request.POST or None,instance=employee_salary)
        forms.instance.employee_id = employee.id

        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Salary for Employee is Created")
            return redirect('employee_salary_list',id=employee_salary.employee_id)
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/employee_salary.html',{'forms':forms,'employee':employee})

@staff_member_required(login_url='/')
def delete_employee_salary(request,id):
    employee_instance = EmployeeSalary.objects.filter(id=id)
    employee_id = employee_instance.first().employee_id

    employee_instance.delete()
    messages.success(request, f"Your Employee has been removed")
    return redirect('employee_salary_list',id=employee_id)


######3 warehouse #########

@staff_member_required(login_url='/')
def create_warehouse(request):
    forms = WarehouseForm(request.POST or None)
    if request.method=="POST":
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Warehouse is Created")
            return redirect('list_warehouses')
        else:

            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/warehouse.html',{'forms':forms})

@staff_member_required(login_url='/')
def list_warehouses(request):
    warehouses=Warehouse.objects.all()
    warehouses = get_pagination_records(request,warehouses)
    return render(request,'staffs/pages/warehouse_list.html',{'warehouses':warehouses})

@staff_member_required(login_url='/')
def update_warehouse(request,id):
    warehouse_instance=get_object_or_404(Warehouse,id=id)
    forms = WarehouseForm(instance=warehouse_instance)
    if request.method=="POST":
        forms = WarehouseForm(request.POST, instance=warehouse_instance)
        if forms.is_valid():
            forms.save()
            messages.success(request, f"Your Warehouse is Updated")
            return redirect('list_warehouses')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/warehouse.html',{'forms':forms})

@staff_member_required(login_url='/')
def delete_warehouse(request, id):
    warehouse_instance = Employee.objects.filter(id=id)
    warehouse_instance.delete()
    messages.success(request, f"Your Warehouse has been removed")
    return redirect('list_warehouses')

@staff_member_required(login_url='/')
def prepare_order_dynamic_content(request):
    if request.method == "GET":
        order_id = request.GET.get("order_id", None)
        order = Orders.objects.get(id = order_id)
        return render(request,'staffs/pages/prepare_order_temp.html',{'order':order})

def prepare_order(request):
    orders = Orders.objects.all().order_by('-created_at')
    if request.method == "POST":
        try:
            with transaction.atomic():
                data_dict = dict(request.POST)
                warehouses = [value[0] for key, value in data_dict.items() if key.startswith('warehouse_')]
                stock_available = len(warehouses) > 0
                for id_idx in range(0, len(warehouses)):
                    product, product_attribute = data_dict.get(f'product_id_{id_idx + 1}')[0].split("_")
                    # find stock by product and warehouse and reduce quantity
                    stock = Stocks.objects.filter(warehouse_id=warehouses[id_idx], product_id=product,
                                                  product_attributes=product_attribute, finished=False)
                    if stock.count() != 1:
                        stock_available = False

                order_id = data_dict.get('order_id',None)[0]
                # get warehouse and reduce quantity from Stock.
                if stock_available:
                    for id_idx in range(0,len(warehouses)):
                        product,product_attribute = data_dict.get(f'product_id_{id_idx + 1}')[0].split("_")
                        # find stock by product and warehouse and reduce quantity
                        stock = Stocks.objects.filter(warehouse_id=warehouses[id_idx],product_id=product,product_attributes=product_attribute,finished=False)
                        qty = data_dict.get(f'qty_{id_idx + 1}')[0]

                        stock_obj = stock.first()
                        stock_obj.left_qty = stock_obj.left_qty - int(qty)
                        stock_obj.save()
                        # create OrderPrepare for admin so that he/she can send products to user.
                        order_prepare = OrderPrepare(order_id_id=order_id,warehouse_id_id=warehouses[id_idx],stock_id_id=stock_obj.id,purchase_qty=qty,status='preparing')
                        order_prepare.save()
                    current_order = Orders.objects.get(id=order_id)
                    current_order.order_status = 'order_prepared'
                    current_order.save()
                    messages.success(request,"You have successfully Started Prepared Order")
                else:
                    messages.warning(request, f"Please check if stock for the current data is available")
        except Exception as e:
            # Rollback the transaction explicitly in case of an exception
            transaction.rollback()

    return render(request,'staffs/pages/prepare_order.html',{'orders':orders})


def update_prepare_order(request,orderid):
    data_dict = dict(request.POST)
    order = Orders.objects.get(orderid=orderid)
    if request.method == 'POST':
        for idx,single_order_prepare in enumerate(order.orderprepare_set.all()):
            warehouse_id = data_dict.get(f'warehouse_{idx+1}',None)
            if warehouse_id:
                single_order_prepare.warehouse_id_id = warehouse_id[0]
                single_order_prepare.save()
                messages.success(request, "You have successfully Updated Prepared Order")
            else:
                messages.warning(request, f"Please Check Again,Invalid Data")
                break
    return render(request,'staffs/pages/update_prepare_order.html',{'order':order})



def list_prepare_orders(request):
    orders = Orders.objects.all().order_by('-created_at')
    orders = get_pagination_records(request,orders)

    return render(request,'staffs/pages/prepare_orders_list.html',{'orders':orders})

def create_delivery(request,orderid):
    order = Orders.objects.get(orderid=orderid)
    forms = DeliveryForm(request.POST or None)
    forms.instance.order_id = order.id

    if request.method=="POST":
        if forms.is_valid():
            if not order.delivery_set.exists():
                order.orderprepare_set.update(status='prepared')
                forms.save()
                messages.success(request, f"Your Delivery is Started")
            else:
                messages.warning(request, f"Already Your Delivery for the order is created")
            return redirect('delivery_list_with_status',status='Confirm')
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")
    return render(request,'staffs/pages/delivery.html',{'forms':forms,'order':order})


def list_of_ledgers(request,type=None):
    ledgers = Ledger.objects.all()

    if type is not None:
        ledgers=ledgers.filter(ledger_type=type)
    ledgers = get_pagination_records(request,ledgers)

    return render(request,'staffs/pages/list_of_ledgers.html',{'ledgers':ledgers,'type':type})

def create_other_ledgers(request):
    ledger_form = LedgerForm(request.POST or None)
    ledger_line_form = LedgerLineForm(request.POST or None)
    if request.method == "POST":
        if ledger_form.is_valid() and ledger_line_form.is_valid():
            ledger = ledger_form.save()
            ledger_line = ledger_line_form.save(commit=False)
            ledger_line.ledger = ledger
            ledger_line.save()
            messages.success(request, f"Your Ledger is Created")
            return redirect('list_of_ledgers',type=ledger.ledger_type)
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")

    return render(request,'staffs/pages/create_other_ledger.html',{'ledger_form':ledger_form,'ledger_line_form':ledger_line_form})


def update_other_ledgers(request,id):
    ledger = Ledger.objects.get(id=id)
    ledger_form = LedgerForm(request.POST or None,instance=ledger)
    ledger_line_form = LedgerLineForm(request.POST or None,instance=ledger.ledger_line.first())
    if request.method == "POST":
        if ledger_form.is_valid() and ledger_line_form.is_valid():
            ledger = ledger_form.save()
            ledger_line = ledger_line_form.save(commit=False)
            ledger_line.ledger = ledger
            ledger_line.save()
            messages.success(request, f"Your Ledger has been Updated")
            return redirect('list_of_ledgers',type=ledger.ledger_type)
        else:
            messages.warning(request, f"Please Check Again,Invalid Data")

    return render(request,'staffs/pages/create_other_ledger.html',{'ledger_form':ledger_form,'ledger_line_form':ledger_line_form})


def custom_log_view(request):
    logs = CRUDEvent.objects.all()  # Retrieve all audit log entries
    logs = get_pagination_records(request,logs)

    return render(request, 'staffs/pages/custom_log_view.html', {'logs': logs,'CUD':[1,2,3]})

def dashboard(request):
    print(">>>>>>>>>",request.POST)
    stocks = Stocks.objects.count()
    warehouses = Warehouse.objects.count()
    employees = Employee.objects.count()
    user_orders = Orders.objects.count()
    prepare_orders = OrderPrepare.objects.count()
    vouchers = Vouchers.objects.filter(is_deleted=False).count()
    other_expenses = Ledger.objects.filter(ledger_type__in=['product_making_expense','raw_material_expense','other_expense']).count()
    payments = Payment.objects.count()
    deliveries = Delivery.objects.count()
    product_attribute_names = AttributeName.objects.count()
    product_attributes = AttributeValue.objects.count()
    product_categories = Category.objects.count()
    product_sub_categories = Subcategory.objects.count()
    products = Products.objects.count()

    # order chart
    now = datetime.datetime.now()
    start_date = datetime.datetime(now.year, now.month, 1)  # Replace with your desired start date
    end_date = datetime.datetime.now()  # Replace with your desired end date

    data_dict = dict(request.POST)
    if data_dict.get('start_date',None) and data_dict.get('end_date',None):
        start_date = datetime.datetime.strptime(data_dict.get('start_date')[0], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(data_dict.get('end_date')[0], '%Y-%m-%d')

    order_chart,orderprepare_chart,expenses_credit_count_by_date,expenses_debit_count_by_date,payment_by_date,delivery_confirm_by_date,delivery_delivering_by_date,delivery_shipped_by_date= get_orders_count_by_date([Orders,OrderPrepare,Ledger,Payment,Delivery],start_date,end_date)

    return render(request, 'staffs/pages/dashboard.html',{
        'stocks':stocks,
        'warehouses':warehouses,
        'employees':employees,
        'user_orders':user_orders,
        'prepare_orders':prepare_orders,
        'vouchers':vouchers,
        'other_expenses':other_expenses,
        'payments':payments,
        'deliveries':deliveries,
        'product_attribute_names':product_attribute_names,
        'product_attributes':product_attributes,
        'product_categories':product_categories,
        'product_sub_categories':product_sub_categories,
        'products':products,
        'order_chart':order_chart,
        'orderprepare_chart':orderprepare_chart,
        'expenses_credit_count_by_date':expenses_credit_count_by_date,
        'expenses_debit_count_by_date':expenses_debit_count_by_date,
        'payment_by_date':payment_by_date,
        'delivery_confirm_by_date':delivery_confirm_by_date,
        'delivery_delivering_by_date':delivery_delivering_by_date,
        'delivery_shipped_by_date':delivery_shipped_by_date,
    })

def get_employees_download(request,type=None):
    queryset = Employee.objects.all()
    if type is not None:
        queryset = queryset.filter(type=type)
        # Assuming you have filtered out the records you want

    # Create the response object with appropriate CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'''attachment; filename="employee_{type if type else 'all'}.csv"'''

    # Create a CSV writer
    csv_writer = csv.writer(response)

    # Write header row
    header_row = [field.name for field in Employee._meta.fields]  # Replace with actual field names
    csv_writer.writerow(header_row)

    # Write data rows
    for record in queryset:
        data_row = [getattr(record, field) if field != 'user' else getattr(record, field).username for field in
                    header_row]
        csv_writer.writerow(data_row)

    return response


