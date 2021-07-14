from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_STATUS = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_STATUS, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def get_institution_count(self):
        quantity_institutions = Institution.objects.all().count()
        return quantity_institutions


class Donation(models.Model):
    quantity = models.IntegerField()  # (liczba worków)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    # phone_number = PhoneField(null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=200, null=False, blank=False)
    zip_code = models.CharField(max_length=5, null=False, blank=False)
    # zip_code = models.CharField(_("zip code"), max_length=5, default="43701")
    pick_up_date = models.DateField()  # wybierz datę
    pick_up_time = models.TimeField()  # godzina odbioru
    pick_up_comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_quantity_count(self):
        quantity = Donation.objects.all()
        quantity_bags = 0
        for i in quantity:
            quantity_bags += i.quantity
        return quantity_bags

    # class Meta():
    #     abstract = True
    def __str__(self):
        return f'{self.quantity}, {self.institution}'
