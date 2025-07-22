from django.shortcuts import render, get_object_or_404, redirect
from .models import Facture, Client
from .forms import FactureForm, ClientForm

# get_object_or_404 renvoie une 404 sale => Go faire une page 404

def creer_facture(request):
    form = FactureForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_factures')
    return render(request, 'factures/creer_facture.html', {'form': form})

def modifier_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    form = FactureForm(request.POST or None, instance=facture)
    if form.is_valid():
        form.save()
        return redirect('liste_factures')
    return render(request, 'factures/modifier_facture.html', {'form': form})

def supprimer_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        facture.delete()
        return redirect('liste_factures')
    return render(request, 'factures/supprimer_facture.html', {'facture': facture})

def detail_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'factures/detail_facture.html', {'facture': facture})

def liste_factures(request):
    client_id = request.GET.get('client')
    if client_id:
        factures = Facture.objects.filter(client__id=client_id)
    else:
        factures = Facture.objects.all()
    clients = Client.objects.all()
    return render(request, 'factures/liste_factures.html', {
        'factures': factures,
        'clients': clients
    })


########### CLIENT ##########

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste_clients.html', {'clients': clients})

def creer_client(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_clients')
    return render(request, 'clients/form_client.html', {'form': form, 'action': 'Créer'})

def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('liste_clients')
    return render(request, 'clients/form_client.html', {'form': form, 'action': 'Modifier'})

def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'clients/supprimer_client.html', {'client': client})