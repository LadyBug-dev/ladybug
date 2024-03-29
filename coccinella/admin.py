from django.contrib import admin
from coccinella.models import *
from unfold.admin import ModelAdmin

@admin.register(StockItem)
class StockItemAdmin(ModelAdmin):
    pass

@admin.register(SourceItem)
class SourceItemAdmin(ModelAdmin):
    pass

@admin.register(SalesChannel)
class SalesChannelAdmin(ModelAdmin):
    pass

@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    pass

@admin.register(StockSale)
class StockSaleAdmin(ModelAdmin):
    pass
# Register your models here.
