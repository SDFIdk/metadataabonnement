from django.db import models

class Dataset(models.Model):
    OBJECTID = models.IntegerField(unique=True)
    ID_LOKALID = models.CharField(max_length=255, unique=True)
    TITEL = models.CharField(max_length=255)

    def __str__(self):
        return self.TITEL


class CustomUser(models.Model):
    USERID = models.AutoField(primary_key=True)
    EMAIL = models.EmailField(unique=True)
    datasets = models.ManyToManyField(Dataset, related_name='users')

    