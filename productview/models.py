from django.db import models

# Create your models here.
class ProductItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class ProductPoint(models.Model):
    title = models.CharField(max_length=100)
    point = models.CharField(max_length=10)

    def __str__(self):
        return self.title