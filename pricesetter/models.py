from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    overlap_day_before = models.IntegerField(validators=[MaxValueValidator(31), MinValueValidator(0)])
    overlap_day_after = models.IntegerField(validators=[MaxValueValidator(31), MinValueValidator(0)])

    def __str__(self):
        return self.name

class SKU(models.Model):
    # setting sku_number in string instead of integer to cater use case when sku_number starts with "0", e.g. "001209"
    sku_number = models.CharField(max_length=20, primary_key=True)
    # setting name as unique to raise error when user accidentally input two skus with same name. theoretically it does not matter as sku_number (p key) should be ultimate source of validation
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.sku_number) + " " + str(self.name)

class Pricing(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    # wsp = wholesale price = list price per case
    # setting wsp's max_digits=6 to expand versatility of the app. in most cases fmcg companies in hk have wsp below $1,000/cs. minority of them could be selling at over $1,000 e.g. high-end wine or pharmaceutical companies
    # wsp sits in Pricing because even perhaps there is no selling price for a wsp pricing entry, a wsp requires start and end date which will be specified in Promotion model
    wsp = models.DecimalField(max_digits=6, decimal_places=2)
    # selling_price = price to shopper in selling unit, e.g. RSP, EDLP, PSP
    selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    multi_buy = models.IntegerField()
    # net_price = price to customer per case
    # allowing users to set pricing in terms of net_price instead of discount to enable more direct, easier approach when using this app
    net_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    @property
    def discount(self):
        return self.wsp - self.net_price

    def __str__(self):
        return str(self.customer) + " " + str(self.sku) + " " + str(self.selling_price) + "/" + str(self.multi_buy)

# Promotion here means a commitment on price with customer
class Promotion(models.Model):
    promo_start = models.DateField()
    promo_end = models.DateField()
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.promo_start) + " to " + str(self.promo_end) + ": " + str(self.pricing)

    @property
    def pricing_start(self):
        return self.promo_start - timedelta(days=self.pricing.customer.overlap_day_before)

    @property
    def pricing_end(self):
        return self.promo_end + timedelta(days=self.pricing.customer.overlap_day_after)

# actual net price to be set after taking in all concerned period(s)
class Result(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return str(self.customer) + " " + str(self.sku) + "'s data"

    def calculate(self):
        pricings = Pricing.objects.filter(customer=self.customer, sku=self.sku)
        pricings_list = list(pricings)
        promotions = Promotion.objects.filter(pricing__in=pricings_list)
        promotions_list = list(promotions)

        for promotion in promotions_list:
            current_date = promotion.pricing_start
            print(current_date)
            #period is a datetime.delta object type
            period = promotion.pricing_end - promotion.pricing_start
            period_days = period.days
            for day in range(period_days):
                print(self.data.get(current_date))
                if self.data.get(current_date) is None:
                    self.data[current_date] = promotion.pricing.net_price
                else:
                    self.data[current_date] = min(self.data[current_date], promotion.pricing.net_price)
                current_date += timedelta(days=1)
        return self.data


    