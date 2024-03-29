from django.core.management.base import BaseCommand, CommandError
from coccinella.models import *
from faker import Faker
from django.db import transaction, DatabaseError

class Command(BaseCommand):
    help = "Generate random data"

    def add_arguments(self, parser):
        pass
    
    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker(locale='pt_BR')
        try:
            with transaction.atomic():
                sourceItems = []
                fabrics = []
                for i in range(5):
                    fabric = StockItem(
                        name=f'Tecido {fake.color()}',
                        quantity=fake.random_int(min=0, max=100),
                        measure=StockItem.MeasureUnit.SQMETER,
                        sellable=False,
                    )
                    fabric.save()
                    fabrics.append(fabric)
                bodies = []
                for i in range(5):
                    body = StockItem(
                        name=f'Body {fake.color()}',
                        quantity=fake.random_int(min=0, max=100),
                        measure=StockItem.MeasureUnit.PIECE,
                        sellable=False,
                    )
                    body.save()
                    bodies.append(body)
                props = []
                for i in range(5):
                    prop = StockItem(
                        name=f'{fake.random_element(['Sianinha', 'Fita'])} {fake.color()}',
                        quantity=fake.random_int(min=0, max=100),
                        measure=StockItem.MeasureUnit.CENTIMETER,
                        sellable=False,
                    )
                    prop.save()
                    props.append(prop)
                bows = []
                for i in range(5):
                    bow = StockItem(
                        name=f'Laço {fake.word()}',
                        quantity=fake.random_int(min=0, max=100),
                        measure=StockItem.MeasureUnit.PIECE,
                        sellable=True,
                        comments=fake.sentence(),
                    )
                    sourceItem = SourceItem(
                        resource=fake.random_element(props),
                        quantity=fake.random_int(min=2, max=20),
                        comments=fake.sentence()
                    )
                    sourceItem.save()
                    sourceItems.append(sourceItem)
                    bow.resources.add(sourceItem)
                    bow.save()
                    bows.append(bow)
                prods = []
                for i in range(5):
                    prod = StockItem(
                        name=f'Body {fake.word()}',
                        quantity=fake.random_int(min=0, max=100),
                        measure=StockItem.MeasureUnit.PIECE,
                        sellable=True,
                        comments=fake.sentences(),
                    )
                    for source in [fabrics, bodies, props]:
                        sourceItem = SourceItem(
                            resource=fake.random_element(source),
                            quantity=fake.random_int(min=2, max=20),
                            comments=fake.sentence()
                        )
                        sourceItem.save()
                        sourceItems.append(sourceItem)
                        prod.resources.add(sourceItem)
                    prod.save()
                    prods.append(prod)
                salesChannels = []
                for name in ['Shopee', 'Elo7', 'Instagram', 'Mercado Livre', 'Nuvem Shop']:
                    salesC = SalesChannel(
                        name=name,
                        link=fake.url(),
                        comments=fake.sentence(),
                    )
                    salesC.save()
                    salesChannels.append(salesC)
                sales = []
                stockSales = []
                for i in range(20):
                    sale = Sale(
                        channel=fake.random_element(salesChannels),
                        referenceCode=fake.ssn(),
                        referenceLink=fake.url(),
                        destName=fake.name(),
                        destCity=fake.city(),
                        comments=fake.sentence(),
                    )
                    for j in range(fake.random_int(min=1, max=5)):
                        stockSale = StockSale(
                            product=fake.random_element(bows+prods),
                            sale=sale,
                            quantity=fake.random_int(min=1, max=10)
                        )
                        sale.products.add(stockSale)
                        stockSale.save()
                        stockSales.append(stockSale)
                    sale.save()
                    sales.append(sale)
        except DatabaseError as e:
            raise CommandError from e
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated random data')
        )