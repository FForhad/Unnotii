from django.db import models

class Code(models.Model):
    key = models.CharField(max_length=100)
    value = models.PositiveIntegerField()

class CodePDF(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='pdfs/')
