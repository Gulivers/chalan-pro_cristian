from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ctrctsapp.utils import geocode_address

# Modelo de Builder.
class Builder(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name='Name')
    trim_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Trim Price SqFt', default=0)
    rough_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rough Price SqFt', default=0)
    travel_price_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Travel Amount', default=0) 
    # Otros campos relevantes del builder

    class Meta:
        verbose_name = 'Builder'
        verbose_name_plural = 'Builders'
        ordering = ['name']

    def __str__(self):
        return self.name

# Modelo de Job.
class Job(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    builder = models.ForeignKey(Builder, null=True, on_delete=models.CASCADE, related_name='jobs')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Address')  # Nueva dirección
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='Longitude')
    # Otros campos relevantes del job


    def save(self, *args, **kwargs):
        # Si hay dirección y no hay coordenadas, calcularlas
        if self.address and (not self.latitude or not self.longitude):
            self.latitude, self.longitude = geocode_address(self.address)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities (Job)'
        ordering = ['name']

    def __str__(self):
        return self.name

# Modelo de House Model.
class HouseModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    jobs = models.ManyToManyField(Job, related_name='house_models')
    # Otros campos relevantes del house model

    class Meta:
        verbose_name = 'House Model'
        verbose_name_plural = 'House Models'
        ordering = ['name']

    def __str__(self):
        return self.name

# Modelo de Work Price.
class WorkPrice(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    trim = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Trim', default=0)
    rough = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rough', default=0)
    unit_price = models.CharField(max_length=255, verbose_name='Unit Price Type')
    builders = models.ManyToManyField(Builder, related_name='work_prices', verbose_name='Builders')

    class Meta:
        verbose_name = 'Work Price'
        verbose_name_plural = 'Work Prices'
        ordering = ['id']

    def __str__(self):
        return self.name

# Modelo de Work this.contract.
class Contract(models.Model):
    TYPE_CHOICES = [
        ('Rough', 'Rough'),
        ('Trim', 'Trim'),
    ]

    DOC_TYPE_CHOICES = [
    ('Contract', 'Contract'),
    ('Bid', 'Bid'),
    ]
    
    date_created = models.DateTimeField(auto_now_add=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES, default='Contract')
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE, verbose_name='Builder')
    house_model = models.ForeignKey(HouseModel, on_delete=models.CASCADE, verbose_name='House Model')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Job')
    lot = models.CharField(null=True, max_length=10, verbose_name='Lot')
    sqft = models.IntegerField(verbose_name='SqFt')
    address = models.CharField(max_length=255, verbose_name='Address')
    job_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Job Price', default=0)
    travel_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Travel Price', default=0)
    total_options = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name='Total Options', default=0)
    total = models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name='Total', default=0)
    comment = models.TextField(null=True, verbose_name='Comment', default='Required to finish at 100%')
    file = models.FileField(null=True, upload_to='contract', default=None, blank=True, verbose_name='File')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_contracts', verbose_name='Created By')
    needs_reprint = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        ordering = ['-date_created']

    def __str__(self):
        return f"Contract {self.id} - {self.created_by}"
    
# Modelo de Work Details this.contract.
class ContractDetails(models.Model):
    cdname = models.CharField(max_length=255, verbose_name='Nombre')
    cdtrim = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Trim Qty', default=0)
    cdtrim_qty = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Trim', default=0)
    cdrough = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rough', default=0)
    cdrough_qty = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rough Qty', default=0)
    cdunit_price = models.CharField(max_length=255, verbose_name='Unit Price Type')
    cdwork_price = models.ForeignKey(WorkPrice, on_delete=models.CASCADE, related_name='priceDetails', verbose_name='Price Details', null=True)
    contract_details = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_details', verbose_name='Work Price Details', null=True)

    class Meta:
        verbose_name = 'Contract Detail'
        verbose_name_plural = 'Contract Details'
        ordering = ['-id']

    def __str__(self):
        return self.cdname
