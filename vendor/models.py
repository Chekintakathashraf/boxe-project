from django.db import models

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.vendor_name

class Sequence(models.Model):
    TYPE_CHOICES = [
        ('purchase order', 'Purchase Order'),
        ('sales order', 'Sales Order'),
        ('payment', 'Payment')
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    alpha = models.CharField(max_length=10) 
    numeric = models.PositiveIntegerField()  
    padding = models.PositiveIntegerField()  
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='sequences')

    def __str__(self):
        numeric_formatted = str(self.numeric).zfill(self.padding)
        return f"{self.vendor.vendor_name }-{self.type}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['type', 'vendor'], name='unique_type_vendor')
        ]
        
        # unique_together = ('type', 'vendor')
        