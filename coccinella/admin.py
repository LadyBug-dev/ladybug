from django.contrib import admin

from . import models

admin.site.register(models.StockItem)
admin.site.register(models.SourceItem)
admin.site.register(models.SalesChannel)
admin.site.register(models.Sale)
admin.site.register(models.StockSale)

# Register your models here.
