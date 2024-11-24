from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to='category-images/', default='category-images/default.jpg')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, default=1)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='product-images/', default='product-images/default.jpg')
    old_price = models.DecimalField(decimal_places=2, max_digits=10)
    new_price = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('product_id', 'user_id'),
        )

    def __str__(self):
        return self.product_id.name
