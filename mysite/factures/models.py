from django.db import models
from decimal import Decimal
from django.utils.timezone import now
from .manager import FactureManager

class CategorieFacture(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, default='', blank=True)
    email = models.CharField(max_length=100, default='', blank=True)
    adresse = models.CharField(max_length=100, default='', blank=True)
    ville = models.CharField(max_length=100, default='', blank=True)
    codepostal = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Facture(models.Model):
    TAUX_TVA_CHOICES = [
        (Decimal('0.00'), '0 %'),
        (Decimal('5.50'), '5.5 %'),
        (Decimal('10.00'), '10 %'),
        (Decimal('20.00'), '20 %'),
    ]

    numero = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    tauxTVA = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        choices=TAUX_TVA_CHOICES,
        default=Decimal('20.00')
    )
    montantTVA = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    montantTTC = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date_emission = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    categorie = models.ForeignKey(CategorieFacture, on_delete=models.SET_NULL, null=True)
    payee = models.BooleanField(default=False)

    objects = FactureManager()

    def save(self, *args, **kwargs):
        self.montantTVA = (self.montant * self.tauxTVA / Decimal('100.00')).quantize(Decimal('0.01'))
        self.montantTTC = (self.montant + self.montantTVA).quantize(Decimal('0.01'))

        if not self.categorie:
            autres, _ = CategorieFacture.objects.get_or_create(nom='Autres')
            self.categorie = autres
        super().save(*args, **kwargs)

class FactureLog(models.Model):
    facture = models.ForeignKey('Facture', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)