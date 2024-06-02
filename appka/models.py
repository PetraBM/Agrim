import datetime
from django.core.validators import MinValueValidator

from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"Profile {self.user.username}"


class Commodity(models.Model):
    commodity_id = models.AutoField(primary_key=True)
    commodity = models.CharField(max_length=255)
    commodity_active = models.IntegerField(default=1)

    def __str__(self):
        return self.commodity


class CNCode(models.Model):
    cncode_id = models.AutoField(primary_key=True)
    cncode = models.CharField(max_length=255)
    commodity = models.ForeignKey("Commodity", on_delete=models.CASCADE)
    cncode_active = models.IntegerField(default=1)

    def __str__(self):
        return self.cncode


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2)
    country_active = models.IntegerField(default=1)

    def __str__(self):
        return self.country


class Licence(models.Model):
    licence_id = models.AutoField(primary_key=True)
    licence_number = models.CharField(max_length=50)
    licence_validity = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    licence_quantity = models.IntegerField(default=0)
    cncode = models.ForeignKey("CNCode", on_delete=models.CASCADE)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)
    quota_number = models.CharField(max_length=10, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    licence_active = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.licence_number}"


class ReqLicence(models.Model):
    request_id = models.AutoField(primary_key=True)
    licence = models.ForeignKey("Licence", on_delete=models.CASCADE)
    request_quantity = models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    request_date = models.DateField()
