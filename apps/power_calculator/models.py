from django.db import models


class GpuBrandsModel(models.Model):
    title = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class GpuSeriesModel(models.Model):
    brand = models.ForeignKey(GpuBrandsModel, on_delete=models.DO_NOTHING, related_name='gpu_series')
    title = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class GpuModel(models.Model):
    series = models.ForeignKey(GpuSeriesModel, on_delete=models.DO_NOTHING, related_name='series_gpu')
    title = models.CharField(max_length=1000)
    power = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class MainBoardModel(models.Model):
    title = models.CharField(max_length=500)
    power = models.IntegerField()


class SSDModel(models.Model):
    type = models.CharField(max_length=500)
    power = models.IntegerField()


class HardModel(models.Model):
    type = models.CharField(max_length=500)
    power = models.IntegerField()


class RamModel(models.Model):
    type = models.CharField(max_length=500)
    power = models.IntegerField()


class DriveModel(models.Model):
    type = models.CharField(max_length=1000)
    power = models.IntegerField()


class FanModel(models.Model):
    size = models.CharField(max_length=500)
    power = models.IntegerField()


class LiquidFanModel(models.Model):
    type = models.CharField(max_length=500)
    power = models.IntegerField()

