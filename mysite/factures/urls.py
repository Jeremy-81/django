from django.urls import path
from . import views

urlpatterns = [
    # Factures
    path('', views.liste_factures, name='liste_factures'),
    path('creer/', views.creer_facture, name='creer_facture'),
    path('modifier/<int:pk>/', views.modifier_facture, name='modifier_facture'),
    path('supprimer/<int:pk>/', views.supprimer_facture, name='supprimer_facture'),
    path('<int:pk>/', views.detail_facture, name='detail_facture'),
    # Clients
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/creer/', views.creer_client, name='creer_client'),
    path('clients/modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),

]
