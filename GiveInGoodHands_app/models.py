from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)


class Institution(models.Model):
    TYPE_STATUS = (
        (1, 'Fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_STATUS, default=1)
    categories = models.ManyToManyField(Category)

class Donation(models.Model):
    quantity = models.IntegerField()  # (liczba worków)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone_number = PhoneField(null=False, blank=False, unique=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    zip_code = models.CharField(max_length=5, null=False, blank=False)
    # zip_code = models.CharField(_("zip code"), max_length=5, default="43701")
    pick_up_date = models.DateTimeField(auto_now_add=True)  # wybierz datę
    pick_up_time = models.DateTimeField(auto_now_add=True)  # godzina odbioru
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)