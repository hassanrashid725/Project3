from django.db.models import Max
from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
import unittest
from django.contrib.auth.signals import user_logged_in

import os
import pathlib
from selenium import webdriver

from .models import Menu, Toppings, Users, Orders, OrderDetails, ItemCategory, SubsExtra, Extras
# Create your tests here.

def file_uri(filename):
    return str(pathlib.Path(os.path.abspath(filename)).as_uri())

driver = webdriver.Chrome('/home/travis/virtualenv/python3.6.7/lib/python3.6/bin/chromedriver')
# options = webdriver.ChromeOptions()
# options.binary_location = '/usr/bin/chromium-browser'
# #All the arguments added for chromium to work on selenium
# options.add_argument("--no-sandbox") #This make Chromium reachable
# options.add_argument("--no-default-browser-check") #Overrides default choices
# options.add_argument("--no-first-run")
# options.add_argument("--disable-default-apps")
# driver = webdriver.Chrome('/home/travis/virtualenv/python3.6/chromedriver',chrome_options=options)

class UserTestCase(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test@gmail.com",first_name="testname", password='top_secret')
        Users.objects.create(user=self.user,address="address",contactNumber=123)
        u2=User.objects.get(username=self.user.username)
        u3=Users.objects.get(user=u2)
        orderTest = Orders.objects.create(user=u3, totalAmount=100)
        c1 = ItemCategory.objects.create(categoryName="test_category")
        e1 = Extras.objects.create(extrasName="test_extra")
        m1 = Menu.objects.create(category=c1, itemName="test_item", priceLarge=10, extras=e1)
        t1 = Toppings.objects.create(name="test_topping1")
        t2 = Toppings.objects.create(name="test_topping2")
        orderDetailsTest = OrderDetails.objects.create(orderId=orderTest, menuId=m1, size="L", price=20)
        self.client = Client()

    def test_order(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.user = self.user
        u1=User.objects.get(username="test@gmail.com")
        u2=User.objects.get(username=u1.username)
        u3=Users.objects.get(user=u2)
        orderTest = Orders.objects.get(user=u3)
        orderDetailsTest = OrderDetails.objects.get(orderId=orderTest)
        t1 = Toppings.objects.get(name="test_topping1")
        t2 = Toppings.objects.get(name="test_topping2")
        orderDetailsTest.toppingsId.add(t1)
        orderDetailsTest.toppingsId.add(t2)
        self.assertEqual(len(orderDetailsTest.toppingsId.in_bulk()),2)

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["menus"].count(), 1)


    def test_login_signout(self):
        response = self.client.login(username='test@gmail.com', password='top_secret')
        self.assertTrue(response)
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.context["user"], "Not Logged In")

class WebpageTests(unittest.TestCase):

    def test_size_toppings(self):
        driver.get(file_uri("seleniumtest/index.html"))
        mushrooms = driver.find_element_by_id("mushrooms")
        olives = driver.find_element_by_id("olives")
        large = driver.find_element_by_id("large")
        AddCartBtn = driver.find_element_by_id("AddCartBtn")
        mushrooms.click()
        olives.click()
        large.click()
        AddCartBtn.click()
        size = driver.execute_script("return window.localStorage.getItem('size');")
        toppings = driver.execute_script("return window.localStorage.getItem('toppings');")
        self.assertEqual(size,"large")
        self.assertEqual(toppings,"Mushrooms,Olives")
