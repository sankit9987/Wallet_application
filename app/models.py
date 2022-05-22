from django.db import models
from django.contrib.auth.models import User
# Create your models here.

status = (
    ('add','add'),
    ('remove','remove'),
)
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=10,choices=status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Total_amount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.FloatField()
