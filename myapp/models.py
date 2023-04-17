from django.db import models

# Create your models here.

# Account 繼承 models.Model
class Account(models.Model):
    name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    passwd = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    


    # 命名資料表為'account'
    class Meta:
        db_table = 'account'

class History(models.Model):
    title = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    image = models.CharField(max_length=50)


    class Meta:
        db_table = 'history'