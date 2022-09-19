from pyexpat import model
from tokenize import Ignore
from django.test import TestCase
from Appthing.models import Customer, Category, Fooditem
from django.utils import timezone
from django.contrib.auth.models import User
from model_bakery import baker
from pprint import pprint
from django.urls import reverse
from selenium import webdriver
import unittest
from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse
#from whatever.forms import WhateverForm

# models test
#@Ignore
class CustomerTest(TestCase):

    def create_customer(self, name="some name", email="some email"):
        return Customer.objects.create( name=name, email=email, date_created=timezone.now())

    def test_customer_creation(self):
        w = self.create_customer()
        self.assertTrue(isinstance(w, Customer))
        self.assertEqual(w.__unicode__(), (w.name, w.email, w.date_created))

    def test_customer_creation_view(self):
        m = self.create_customer()
        url = reverse("login")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

class CustomerTestBakery(TestCase):

    def test_customer_creation_bakery(self):
        what = baker.make(Customer)
        self.assertTrue(isinstance(what, Customer))
        self.assertEqual(what.__unicode__(), (what.name, what.email, what.date_created))

    

class CategoryTest(TestCase):

    def create_category(self, name="some name"):
        return Category.objects.create( name=name)

    def test_category_creation(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__unicode__(), w.name)
    
    # def test_customer_creation_view(self):
    #     cust=User.customer
    #     User.groups.clear()
    #     url = reverse("addFooditem")
    #     resp = self.client.get(url)

    #     self.assertEqual(resp.status_code, 200)

class TestSignup(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("C:\py_stuff\chromedriver.exe")
        self.driver.maximize_window() 
        self.driver.implicitly_wait(20) 

    def test_signup_fire(self):
        self.driver.get("http://localhost:8000/login")
        #self.driver.find_element_by_id('id_title').send_keys("test title")
        self.driver.find_element_by_id('id_form').send_keys("test body")
        self.driver.find_element_by_id('submit').click()
        self.assertIn("http://localhost:8000/login", self.driver.current_url)
        #self.assertIn("http://localhost:8000/login", self.driver.current_url)

    def tearDown(self):
        self.driver.quit        


class FooditemTestBakery(TestCase):
    
    def test_fooditem_creation_bakery(self):
        what = baker.make(Fooditem)
        self.assertTrue(isinstance(what, Fooditem))
        self.assertEqual(what.__unicode__(), what.name)     

