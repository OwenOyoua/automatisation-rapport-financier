"""
Tests pour les modèles de données simplifiés.
"""

import unittest
from src.core.simple_models import LigneCompte, JeuDonnees, Sens


class TestLigneCompte(unittest.TestCase):
    """Tests pour la classe LigneCompte."""
    
    def test_ligne_compte_valide(self):
        """Test création d'une ligne de compte valide."""
        ligne = LigneCompte(
            code_compte="1111",
            libelle="Capital social",
            classe=1,
            sens=Sens.CREDIT,
            montant=100000.0,
            periode="2024"
        )
        
        self.assertEqual(ligne.code_compte, "1111")
        self.assertEqual(ligne.libelle, "Capital social")
        self.assertEqual(ligne.classe, 1)
        self.assertEqual(ligne.sens, Sens.CREDIT)
        self.assertEqual(ligne.montant, 100000.0)
        self.assertEqual(ligne.periode, "2024")
    
    def test_code_compte_invalide(self):
        """Test validation du code compte."""
        with self.assertRaises(ValueError):
            LigneCompte(
                code_compte="",
                libelle="Test",
                classe=1,
                sens=Sens.DEBIT,
                montant=1000.0,
                periode="2024"
            )
    
    def test_classe_invalide(self):
        """Test validation de la classe."""
        with self.assertRaises(ValueError):
            LigneCompte(
                code_compte="1111",
                libelle="Test",
                classe=10,
                sens=Sens.DEBIT,
                montant=1000.0,
                periode="2024"
            )
    
    def test_montant_invalide(self):
        """Test validation du montant."""
        with self.assertRaises(ValueError):
            LigneCompte(
                code_compte="1111",
                libelle="Test",
                classe=1,
                sens=Sens.DEBIT,
                montant=-1000.0,
                periode="2024"
            )


class TestJeuDonnees(unittest.TestCase):
    """Tests pour la classe JeuDonnees."""
    
    def setUp(self):
        """Configuration des tests."""
        self.lignes_equilibrees = [
            LigneCompte("1111", "Capital social", 1, Sens.CREDIT, 100000.0, "2024"),
            LigneCompte("2111", "Frais constitution", 2, Sens.DEBIT, 5000.0, "2024"),
            LigneCompte("2340", "Matériel transport", 2, Sens.DEBIT, 25000.0, "2024"),
            LigneCompte("3111", "Stocks marchandises", 3, Sens.DEBIT, 15000.0, "2024"),
            LigneCompte("3421", "Clients", 4, Sens.DEBIT, 20000.0, "2024"),
            LigneCompte("4411", "Fournisseurs", 4, Sens.CREDIT, 12000.0, "2024"),
            LigneCompte("5141", "Banque", 5, Sens.DEBIT, 50000.0, "2024"),
            LigneCompte("5514", "Caisse", 5, Sens.DEBIT, 7000.0, "2024"),
            LigneCompte("1191", "Résultat de l'exercice", 1, Sens.CREDIT, 10000.0, "2024"),
        ]
    
    def test_jeu_donnees_valide(self):
        """Test création d'un jeu de données valide."""
        donnees = JeuDonnees(
            lignes=self.lignes_equilibrees,
            periode="2024",
            entreprise="Test Entreprise"
        )
        
        self.assertEqual(len(donnees.lignes), 9)
        self.assertEqual(donnees.periode, "2024")
        self.assertEqual(donnees.entreprise, "Test Entreprise")
    
    def test_jeu_donnees_vide(self):
        """Test validation d'un jeu de données vide."""
        with self.assertRaises(ValueError):
            JeuDonnees(
                lignes=[],
                periode="2024",
                entreprise="Test Entreprise"
            )
    
    def test_desequilibre_debit_credit(self):
        """Test détection du déséquilibre débit/crédit."""
        lignes_desequilibrees = self.lignes_equilibrees[:-1]  # Retire la dernière ligne
        
        with self.assertRaises(ValueError):
            JeuDonnees(
                lignes=lignes_desequilibrees,
                periode="2024",
                entreprise="Test Entreprise"
            )
    
    def test_get_total_classe(self):
        """Test calcul du total par classe."""
        donnees = JeuDonnees(
            lignes=self.lignes_equilibrees,
            periode="2024"
        )
        
        # Classe 1 (capitaux) : 100000 + 10000 = 110000
        total_classe_1 = donnees.get_total_classe(1)
        self.assertEqual(total_classe_1, 110000.0)
        
        # Classe 2 (immobilisations) : 5000 + 25000 = 30000
        total_classe_2 = donnees.get_total_classe(2)
        self.assertEqual(total_classe_2, 30000.0)
    
    def test_get_total_sens(self):
        """Test calcul du total par sens."""
        donnees = JeuDonnees(
            lignes=self.lignes_equilibrees,
            periode="2024"
        )
        
        total_debit = donnees.get_total_sens(Sens.DEBIT)
        total_credit = donnees.get_total_sens(Sens.CREDIT)
        
        # Vérifier l'équilibre
        self.assertEqual(total_debit, total_credit)
        self.assertEqual(total_debit, 122000.0)


if __name__ == '__main__':
    unittest.main()
