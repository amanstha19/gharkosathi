from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class Categorie(models.Model):
    model_name = models.CharField(max_length=200)

    def __str__(self):
        return self.model_name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    Filter_Price_Choices = (
        ('100 TO 1000', '1000 TO 2000'),
        ('200 TO 3000', '3000 TO 4000'),
        ('4000 TO 10000', '10000 To 30000'),
    )
    price = models.CharField(choices=Filter_Price_Choices, max_length=90)

class Product(models.Model):
    STOCK_CHOICES = (('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK'))
    STATUS_CHOICES = (('Publish', 'Publish'), ('DRAFT', 'DRAFT'))

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=60)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    stock = models.CharField(choices=STOCK_CHOICES, max_length=200)
    status = models.CharField(choices=STATUS_CHOICES, max_length=200)
    added_date = models.DateTimeField(default=timezone.now)

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.unique_id and self.added_date:
            if not self.id:
                super().save(*args, **kwargs)
            self.unique_id = self.added_date.strftime('75%Y%m%d23') + str(self.id)
            super().save(*args, **kwargs)

class images(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
      return self.name

class CustomUser(models.Model):
    email = models.EmailField(unique=True, validators=[EmailValidator(message="Enter a valid email address.")])

    def clean(self):
        email_exists = CustomUser.objects.exclude(pk=self.pk).filter(email=self.email).exists()
        if email_exists:
            raise ValidationError({'email': 'This email address is already in use.'})
