from django.contrib import admin
from .models import (Store,Category,Subcategory,AttributeName,AttributeValue,Products,
ProductChangePriceAttributes,
Rates,
Stocks,Cart,Checkout,Discount,Orders,OrderLines,Delivery,
Deals_of_day,PromoCode,OtpModel,Payment)
from import_export.admin import ImportExportActionModelAdmin


class StocksAdmin(ImportExportActionModelAdmin):
    list_display=('product_id','total_qty','left_qty','finished')
    search_fields = ('product_id', 'finished')
    list_per_page = 25
class StocksInline(admin.TabularInline):
    model = Stocks

class StoreAdmin(ImportExportActionModelAdmin):
    list_display=('name_of_shop','owner','mobile_no')
    inlines = [
        StocksInline
    ]

admin.site.register(Stocks, StocksAdmin)
admin.site.register(Store, StoreAdmin)


class ProductChangePriceAttributesAdmin(ImportExportActionModelAdmin):
    list_display = ( 'p_id', 'price')
    # list_display_links = ('id', 'name')
    search_fields = ('p_id', 'attribute_values')
    list_per_page = 25


class ProductChangePriceAttributesInline(admin.TabularInline):
    model = ProductChangePriceAttributes

class Deals_of_dayAdmin(ImportExportActionModelAdmin):
    model = Deals_of_day
    list_display = ('p_id', 'with_product','discount_price')

class Deals_of_dayInline(admin.TabularInline):
    model = Deals_of_day
    fk_name = "p_id"

admin.site.register(Deals_of_day,Deals_of_dayAdmin)

class ProductAdmin(ImportExportActionModelAdmin):
    model = Products
    inlines = [
        ProductChangePriceAttributesInline,
        Deals_of_dayInline,
    ]
    list_display = ('p_name', 'price','p_category')

class ProductsInline(admin.TabularInline):
    model = Products

admin.site.register(Products, ProductAdmin)
admin.site.register(ProductChangePriceAttributes,ProductChangePriceAttributesAdmin)


class CategoryAdmin(ImportExportActionModelAdmin):
    model = Category
    inlines = [
        ProductsInline,
    ]

class SubcategoryAdmin(ImportExportActionModelAdmin):
    model = Subcategory
    inlines = [
        ProductsInline,
    ]

admin.site.register(Category,CategoryAdmin)
admin.site.register(Subcategory,SubcategoryAdmin)


admin.site.register(AttributeName)
admin.site.register(AttributeValue)
admin.site.register(Rates)

class CartAdmin(ImportExportActionModelAdmin):
    model = Cart
    list_display = ('product_id', 'user_id','qty','price')

admin.site.register(Cart,CartAdmin)
admin.site.register(Checkout)

class DiscountAdmin(ImportExportActionModelAdmin):
    model = Discount
    list_display = ('on_above_purchase', 'percent_off')

admin.site.register(Discount,DiscountAdmin)

class PromoCodeAdmin(ImportExportActionModelAdmin):
    model = PromoCode
    list_display = ('name_of_code', 'discount_price','created_at','expirable')

admin.site.register(PromoCode,PromoCodeAdmin)


class OrderLinesAdmin(admin.ModelAdmin):
    list_display = ['product_id','order_id','price','qty']
    fields = ['product_id','order_id','price','qty']

class OrderLinesInline(admin.TabularInline):
    model = OrderLines


class OrdersAdmin(admin.ModelAdmin):
    model = Orders
    readonly_fields=('created_at',)

    inlines = [
        OrderLinesInline,
    ]
    list_display = ('checkout', 'order_status','user','created_at','payment_failed','amount','discount','created_seller')
    fields = ['checkout', 'order_status','user','payment_failed','amount','discount','created_seller']


admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderLines,OrderLinesAdmin)

admin.site.register(OtpModel)

admin.site.register(Payment)

admin.site.register(Delivery)
