from django.contrib import admin
from .models import Client, Facture, CategorieFacture, FactureLog

@admin.action(description="Marquer les factures sélectionnées comme payées")
def marquer_comme_payee(modeladmin, request, queryset):
    updated = queryset.update(payee=True)
    modeladmin.message_user(request, f"{updated} facture(s) marquée(s) comme payée(s).")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'ville', 'adresse', 'codepostal')
    search_fields = ('payee', 'nom', 'prenom')
    list_filter = ('nom',)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'categorie', 'montant', 'date_emission', 'payee')
    list_filter = ('payee', 'categorie', 'client')
    search_fields = ('numero', 'client__nom', 'client__prenom')
    date_hierarchy = 'date_emission'
    actions = [marquer_comme_payee]

@admin.register(CategorieFacture)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(FactureLog)
class FactureLogAdmin(admin.ModelAdmin):
    list_display = ('facture', 'timestamp', 'ip_address')
    search_fields = ('facture__numero', 'ip_address')
    list_filter = ('timestamp',)