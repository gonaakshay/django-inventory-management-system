from django.db import models

class Product(models.Model):

    product_name = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.IntegerField()

    description = models.TextField()

    manufacture_date = models.DateField()

    expiry_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Soft Delete Field
    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.product_name