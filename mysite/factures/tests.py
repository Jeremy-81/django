from django.test import TestCase
from django.urls import reverse
from .models import Client, Facture, CategorieFacture
from decimal import Decimal
from datetime import date

class FactureModelTest(TestCase):

    def setUp(self):
        self.client_obj = Client.objects.create(nom="John", prenom="Doe", email="doe@mail.com", adresse="", ville="", codepostal="")
        self.cat = CategorieFacture.objects.create(nom="Services")

    def test_calcul_automatique_tva_ttc(self):
        facture = Facture.objects.create(
            numero="F001",
            montant=Decimal("100.00"),
            tauxTVA=Decimal("20.00"),
            date_emission=date.today(),
            client=self.client_obj,
            categorie=self.cat
        )
        self.assertEqual(facture.montantTVA, Decimal("20.00"))
        self.assertEqual(facture.montantTTC, Decimal("120.00"))

    def test_categorie_autres_automatique(self):
        facture = Facture.objects.create(
            numero="F002",
            montant=Decimal("50.00"),
            tauxTVA=Decimal("10.00"),
            date_emission=date.today(),
            client=self.client_obj,
            categorie=None
        )
        self.assertEqual(facture.categorie.nom, "Autres")


class FactureViewTests(TestCase):

    def setUp(self):
        self.client_obj = Client.objects.create(nom="Doe", prenom="John", email="john@mail.com", adresse="", ville="", codepostal="")
        self.cat = CategorieFacture.objects.create(nom="Informatique")
        self.facture = Facture.objects.create(
            numero="F100",
            montant=Decimal("300.00"),
            tauxTVA=Decimal("20.00"),
            date_emission=date.today(),
            client=self.client_obj,
            categorie=self.cat,
        )

    def test_list_view_status_code(self):
        response = self.client.get(reverse('liste_factures'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_template_used(self):
        response = self.client.get(reverse('liste_factures'))
        self.assertTemplateUsed(response, 'factures/liste_factures.html')

    def test_list_view_contains_facture(self):
        response = self.client.get(reverse('liste_factures'))
        self.assertContains(response, "F100")

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('detail_facture', args=[self.facture.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_invalid_id_404(self):
        response = self.client.get(reverse('detail_facture', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_content(self):
        response = self.client.get(reverse('detail_facture', args=[self.facture.pk]))
        self.assertContains(response, "300.00")

    def test_create_view_post_valid_data(self):
        response = self.client.post(reverse('creer_facture'), {
            'numero': 'F200',
            'montant': '150.00',
            'tauxTVA': '10.00',
            'date_emission': '2024-01-01',
            'client': self.client_obj.pk,
            'categorie': self.cat.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Facture.objects.filter(numero='F200').exists())

    def test_create_view_missing_category(self):
        response = self.client.post(reverse('creer_facture'), {
            'numero': 'F201',
            'montant': '100.00',
            'tauxTVA': '5.50',
            'date_emission': '2024-01-01',
            'client': self.client_obj.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Facture.objects.filter(numero='F201').exists())

    def test_create_view_template_used(self):
        response = self.client.get(reverse('creer_facture'))
        self.assertTemplateUsed(response, 'factures/creer_facture.html')