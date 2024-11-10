from django.db import models
from datetime import date

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_en_stock = models.IntegerField()
    date_peremption = models.DateField(default=date.today)

class Commande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_commande = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=50)

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    adresse = models.TextField()

class Utilisateur(models.Model):
    nom_utilisateur = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)
    
