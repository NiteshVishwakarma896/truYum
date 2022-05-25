from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Menu Item Models
class Menu(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    active = models.BooleanField()
    delivery_free = models.BooleanField()
    date_of_launch = models.DateField()
    category_type = models.CharField(max_length=250)
    date_created = models.DateTimeField()
    
    def __repr__(self) -> str:
        return f"{self.id} - {self.name} - {self.price} - {self.active} - {self.delivery_free} - {self.date_of_launch} - {self.category_type} - {self.date_created}"
    

#Cart Item Models
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    category_type = models.CharField(max_length=250)
    delivery_free = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __repr__(self) -> str:
        return f"{self.id} - {self.user_id} - {self.name} - {self.price} - {self.delivery_free} - {self.category_type} - {self.date_created}"