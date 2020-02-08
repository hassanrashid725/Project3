from django.db import models
from django.contrib.auth.models import User


class ItemCategory(models.Model):
    categoryName = models.CharField("Category Name",max_length=64)

    def __str__(self):
        return f"{self.categoryName}"

class Extras(models.Model):
    extrasName = models.CharField("Extras Name", max_length=64)

    def __str__(self):
        return f"{self.extrasName}"


# Create your models here.
class Menu(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="itemcategory")
    itemName = models.CharField(max_length=64)
    priceSmall = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    priceLarge = models.DecimalField(max_digits=5, decimal_places=2)
    extras = models.ForeignKey(Extras, null=True, blank=True, on_delete=models.CASCADE, related_name="itemextras")
    extrasAllowed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Item Name: {self.itemName} - Category: {self.category} - Small: {self.priceSmall} - Large: {self.priceLarge} - Extras: {self.extras}"

class Toppings(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class SubsExtra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} + ${self.price}"


class Users(models.Model):
    # email = models.CharField(max_length=24)
    # password = models.CharField(max_length=24)
    # name = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    address = models.CharField(max_length=64)
    contactNumber = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user}"

class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="userOrder")
    totalAmount = models.FloatField()

    def __str__(self):
        return f"Username: {self.user} - Total Amount: {self.totalAmount}"

class OrderDetails(models.Model):
    availableSizes = [
        ('S','Small'),
        ('L','Large')
        ]

    orderId = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="orderID")
    menuId = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menuID")
    toppingsId = models.ManyToManyField(Toppings, blank=True, related_name="toppingsID")
    subsExtraId = models.ManyToManyField(SubsExtra, blank=True, related_name="subsExtraID")
    size = models.CharField(max_length=1,choices=availableSizes,default="L")
    # quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True);

    def __str__(self):
        return f"Order ID: {self.orderId.id} - User: {self.orderId.user.user.username} - Menu ID: {self.menuId.category.categoryName} - {self.menuId.itemName} Toppings: {self.toppingsId.in_bulk()} - Price: {self.price}"
