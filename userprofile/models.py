from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    nid = models.CharField(max_length=16)
    address = models.CharField(max_length=200)
    image = models.CharField(max_length=300)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add a point field with an initial value of zero
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Retrieve the points_increment parameter or use a default value (e.g., 10)
        points_increment = kwargs.pop('points_increment', 0)

        # Update the points field based on the provided increment value
        self.points += points_increment

        super().save(*args, **kwargs)


class RechargeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=15)
    value = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.key} - {self.value} - {self.date}"