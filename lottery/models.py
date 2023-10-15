from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class GivenToken(models.Model):
    gtoken = models.CharField(max_length=15)
    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.gtoken