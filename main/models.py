from django.db import models

class Products(models.Model):
    article = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    min_quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def discounted_price(self):
        return self.price * (100 - self.discount) / 100
        
    class Meta:
        managed = False
        db_table = 'products'

class Users(models.Model):
    role = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    login = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=50)
    роль_сотрудника = models.CharField(db_column='Роль сотрудника', max_length=50, blank=True, null=True)
    фио = models.CharField(max_length=50, blank=True, null=True)
    логин = models.CharField(max_length=50, blank=True, null=True)
    пароль = models.CharField(max_length=50, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'users'