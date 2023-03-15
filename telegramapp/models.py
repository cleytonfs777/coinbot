from django.db import models


class Coin(models.Model):
    
    par = models.CharField(max_length=10)
    preco = models.CharField(max_length=10, null=True, blank=True)
    qtd = models.CharField(max_length=10, null=True, blank=True)
    tipo = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return self.par
