from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    overlap_day_before = models.IntegerField()
    overlap_day_after = models.IntegerField()

class SKU(models.Model):
    #setting sku_number in string instead of integer to cater use case when sku_number starts with "0", e.g. "001209"
    sku_number = models.CharField(max_length=20, primary_key=True)
    #setting name as unique to raise error when user accidentally input two skus with same name. theoretically it does not matter as sku_number (p key) should be ultimate source of validation
    name = models.CharField(max_length=50, unique=True)

class Pricing(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    #wsp = wholesale price = list price per case
    #setting wsp's max_digits=6 to expand versatility of the app. in most cases fmcg companies in hk have wsp below $1,000/cs. minority of them could be selling at over $1,000 e.g. high-end wine or pharmaceutical companies
    wsp = models.DecimalField(max_digits=6, decimal_places=2)
    #selling_price = price to shopper in selling unit, e.g. RSP, EDLP, PSP
    selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    multi_buy = models.IntegerField()
    #net_price = price to customer per case
    net_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    @property
    def discount(self):
        return self.wsp - self.net_price

#Period here means price setting period
class Period(models.Model):
    promo_start = models.DateField()
    promo_end = models.DateField()
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE) 
