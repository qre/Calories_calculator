from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    def __unicode__(self):
        return self.name, self.email, self.date_created
    
    def __str__(self):
        return str(self.name)
class Category(models.Model):
    options=(
        ('bread','bread, cereal'),
        ('meat','meat, fish'),
        ('fruits','fruits, vegetables'),
        ('milk','milk, dairy'),
        ('fats','fats, sugars'),
    )
    name=models.CharField(max_length=50,choices=options)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
class Fooditem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    carbohydrate = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    fats = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    protein = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    calories=models.DecimalField(max_digits=5,decimal_places=2,default=0,blank=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    def __unicode__(self):
        return self.name #, self.category, self.carbohydrate, self.fats, self.protein, self.calories, self.quantity, self.description
    def __str__(self):
        return str(self.name)
#for user page-------------------------------------------------------------
class UserFooditem(models.Model):
    customer = models.ManyToManyField(Customer ,blank=True)
    fooditem=models.ManyToManyField(Fooditem)
