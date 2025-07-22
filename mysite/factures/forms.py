from django import forms
from .models import Facture, Client

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorie'].required = False
        self.fields['client'].required = False

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'adresse', 'ville', 'codepostal']