from django.db import models
from django.shortcuts import reverse
from django_jalali.db import models as jmodels
from apps.user.models import UserModel
from apps.product.models import ProductModel


class BuketModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='user_buckets')
    is_paid = models.BooleanField(default=False)
    transaction_code = models.CharField(max_length=100, blank=True, null=True)
    paid_date = jmodels.jDateTimeField(null=True, blank=True)
    price_paid = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1000, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bailee_name = models.CharField(max_length=1000, null=True, blank=True)
    bailee_phone = models.CharField(max_length=11, null=True, blank=True)
    transaction_mode = models.CharField(max_length=1000, null=True, blank=True)
    post_price = models.PositiveIntegerField(default=0)
    delivery_date = jmodels.jDateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('user:order_detail', args=[self.id])


class BucketProductsModel(models.Model):
    bucket = models.ForeignKey(BuketModel, on_delete=models.CASCADE, related_name='user_bucket_products')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, related_name='bucket_products')
    final_price = models.PositiveIntegerField(null=True, blank=True)
    number = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.number * self.product.price_after_off


class WalletModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.DO_NOTHING, related_name='user_wallet')
    amount = models.PositiveIntegerField(default=0)
    last_charge = jmodels.jDateTimeField(null=True, blank=True)


TransactionChoices = (('deposit', 'deposit'), ('endurance', 'endurance'))


class WalletTransactionModel(models.Model):
    wallet = models.ForeignKey(WalletModel, on_delete=models.CASCADE, related_name='wallet_transactions')
    type = models.CharField(max_length=500, choices=TransactionChoices)
    description = models.TextField()
    date = jmodels.jDateTimeField(auto_now_add=True)
