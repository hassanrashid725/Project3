from django.contrib import admin
from .models import ItemCategory, Menu, Toppings, Users, Orders, OrderDetails, SubsExtra, Extras
# Register your models here.

class OrderInline(admin.StackedInline):
    model = OrderDetails.toppingsId.through
    extra = 1

class ToppingAdmin(admin.ModelAdmin):
    inlines = [OrderInline]

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ("toppingsId", "subsExtraId",)



admin.site.register(ItemCategory)
admin.site.register(Menu)
admin.site.register(Toppings, ToppingAdmin)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(OrderDetails, OrderAdmin)
admin.site.register(SubsExtra)
admin.site.register(Extras)
