from django.db import models

class FactureQuerySet(models.QuerySet):
    def payees(self):
        return self.filter(payee=True)

    def impayees(self):
        return self.filter(payee=False)

    def par_client(self, client):
        return self.filter(client=client)

    def par_categorie(self, categorie):
        return self.filter(categorie=categorie)


class FactureManager(models.Manager):
    def get_queryset(self):
        return FactureQuerySet(self.model, using=self._db)

    def payees(self):
        return self.get_queryset().payees()

    def impayees(self):
        return self.get_queryset().impayees()

    def par_client(self, client):
        return self.get_queryset().par_client(client)
