from django.db import models
from django.utils.translation import gettext_lazy as _

# TODO: discuss all relations' on_delete behaviour

class StockItem(models.Model):
    class MeasureUnit(models.TextChoices): #TBD, maybe promote to a model by itself
        METER = 'm', _('Meter')
        CENTIMETER = 'cm', _('Centimeter')
        SQMETER = 'm²', _('Squared meter')
        PIECE = 'p', _('Piece')

    name = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    measure = models.CharField(max_length=5, choices=MeasureUnit, default=MeasureUnit.PIECE)
    sellable = models.BooleanField()
    resources = models.ManyToManyField(to='self', blank=True, symmetrical=False, through='SourceItem')
    comments = models.TextField(null=True, blank=True)


class SourceItem(models.Model):
    resource = models.ForeignKey(StockItem, on_delete=models.RESTRICT, related_name='resources_set')
    product = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='products_set')
    quantity = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    
    
class SalesChannel(models.Model):
    name = models.CharField(max_length=30)
    link = models.CharField(max_length=1024)
    comments = models.TextField(null=True, blank=True)


class Sale(models.Model):
    channel = models.ForeignKey(SalesChannel, on_delete=models.CASCADE)
    referenceCode = models.CharField(max_length=30)
    referenceLink = models.CharField(max_length=1024, null=True, blank=True)
    destName = models.CharField(max_length=100)
    destCity = models.CharField(max_length=30)
    products = models.ManyToManyField(StockItem, through="StockSale")
    comments = models.TextField(null=True, blank=True)
    
    
class StockSale(models.Model):
    product = models.ForeignKey(StockItem, on_delete=models.RESTRICT)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    quantity = models.IntegerField()