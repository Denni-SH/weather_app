from django.db import models


class Information(models.Model):
    ID = models.AutoField(primary_key=True)
    city = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    description = models.CharField(max_length=20)

    def __str__(self):
        return self.city


