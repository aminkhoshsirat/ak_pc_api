from django.db import models
from apps.product.models import ProductModel


class AsembleModel(models.Model):
    is_payed = models.BooleanField(default=False)


class AsembleProductsModel(models.Model):
    asemble = models.ForeignKey(AsembleModel, on_delete=models.CASCADE, related_name='asemble_products')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING)
    numbers = models.PositiveIntegerField(default=1)
