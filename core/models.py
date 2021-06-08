from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    """
    Transaction model

    FK: ``User``

    BackReference: None

    """
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=11, decimal_places=2)

    owner = models.ForeignKey(
        User, verbose_name='Owner', related_name= "transactions", on_delete=models.CASCADE)

    type = models.CharField(max_length=10, blank=True, editable = False)
    
    def save(self, *args, **kwargs):
        if (self.amount>0):
            self.type =  "income"
        else:
            self.type =  "outcome"
        
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date', 'id']