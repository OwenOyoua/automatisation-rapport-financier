"""
Tests pour les transformations financières.
"""

import unittest
from src.core.simple_models import LigneCompte, JeuDonnees, Sens
from src.core.simple_transforms import SimpleReportCalculator


class TestSimpleReportCalculator(unittest.TestCase):
    """Tests pour la classe SimpleReportCalculator."""
    
    def setUp(self):
        """Configuration des tests."""
        self.calculator = SimpleReportCalculator()
        
        # Données de test équilibrées
        self.lignes_test = [
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
        
        self.donnees_test = JeuDonnees(
            lignes=self.lignes_test,
            periode="2024",
            entreprise="Test Entreprise"
        )
    
    def test_calculer_bilan_fonctionnel(self):
        """Test calcul du bilan fonctionnel."""
        bilan = self.calculator.calculer_bilan_fonctionnel(self.donnees_test)
        
        # Vérification des emplois stables (classe 2 débit)
        self.assertEqual(bilan.emplois_stables, 30000.0)
        
        # Vérification des ressources stables (classes 1 et 5 crédit)
        ressources_attendues = 110000.0 + 0.0  # Classe 1 crédit + Classe 5 crédit (aucun)
        self.assertEqual(bilan.ressources_stables, ressources_attendues)
        
        # FRNG = Ressources stables - Emplois stables
        self.assertEqual(bilan.frng, 80000.0)
        
        # Actifs circulants (classes 3, 4 débit)
        self.assertEqual(bilan.actifs_circulants, 35000.0)
        
        # Passifs circulants (classes 3, 4 crédit)
        self.assertEqual(bilan.passifs_circulants, 12000.0)
        
        # BFR = Actifs circulants - Passifs circulants
        self.assertEqual(bilan.bfr, 23000.0)
        
        # Trésorerie
        self.assertEqual(bilan.tresorerie_active, 57000.0)
        self.assertEqual(bilan.tresorerie_passive, 0.0)
        self.assertEqual(bilan.tresorerie_nette, 57000.0)
        
        # Vérification de l'équilibre FRNG = BFR + Trésorerie nette
        self.assertEqual(bilan.frng, bilan.bfr + bilan.tresorerie_nette)
    
    def test_calculer_bilan_financier(self):
        """Test calcul du bilan financier."""
        bilan = self.calculator.calculer_bilan_financier(self.donnees_test)
        
        # Actif
        self.assertEqual(bilan.immobilisations_nettes, 30000.0)
        self.assertEqual(bilan.stocks, 15000.0)
        self.assertEqual(bilan.creances_clients, 20000.0)
        self.assertEqual(bilan.autres_creances, 0.0)
        self.assertEqual(bilan.tresorerie_active, 57000.0)
        self.assertEqual(bilan.total_actif, 122000.0)
        
        # Passif
        self.assertEqual(bilan.capital_social, 100000.0)
        # Réserves (classe 1 crédit sauf capital social et résultat)
        self.assertEqual(bilan.reserves, 10000.0)
        self.assertEqual(bilan.capitaux_propres, 110000.0)
        self.assertEqual(bilan.dettes_financieres_lt, 0.0)
        self.assertEqual(bilan.dettes_fournisseurs, 12000.0)
        self.assertEqual(bilan.autres_dettes_ct, 0.0)
        self.assertEqual(bilan.tresorerie_passive, 0.0)
        self.assertEqual(bilan.total_passif, 122000.0)
        
        # Note: Le résultat est calculé comme différence classes 7-6
        # Dans nos données de test, il n'y a pas de classes 6/7
        # Le résultat net est donc 0 (pas de comptes de gestion)
        self.assertEqual(bilan.resultat_net, 0.0)
    
    def test_calculer_patrimoine(self):
        """Test calcul du patrimoine."""
        patrimoine = self.calculator.calculer_patrimoine(self.donnees_test)
        
        # Actifs économiques (classes 2,3,4,5 débit)
        actifs_attendus = 30000.0 + 15000.0 + 20000.0 + 57000.0
        self.assertEqual(patrimoine.actifs_economiques, actifs_attendus)
        
        # Dettes financières (classe 1 crédit sauf capitaux propres)
        self.assertEqual(patrimoine.dettes_financieres, 0.0)
        
        # Actif net comptable
        self.assertEqual(patrimoine.actif_net_comptable, actifs_attendus)
        
        # Capitaux propres retraités
        self.assertEqual(patrimoine.capitaux_propres_retraites, 110000.0)
        
        # Patrimoine net
        self.assertEqual(patrimoine.patrimoine_net, actifs_attendus)
        
        # Ratios
        self.assertEqual(patrimoine.ratio_endettement, 0.0)
        self.assertIsNotNone(patrimoine.ratio_solvabilite)  # Division par zéro évitée
        self.assertEqual(patrimoine.ratio_liquidite, 1.0)
    
    def test_analyser_rapport_bilan_fonctionnel(self):
        """Test analyse du bilan fonctionnel."""
        from src.core.simple_models import BilanFonctionnel
        
        bilan = BilanFonctionnel(
            emplois_stables=30000.0,
            ressources_stables=107000.0,
            frng=77000.0,
            actifs_circulants=35000.0,
            passifs_circulants=12000.0,
            bfr=23000.0,
            tresorerie_active=57000.0,
            tresorerie_passive=0.0,
            tresorerie_nette=57000.0,
            periode="2024"
        )
        
        analyse = self.calculator.analyser_rapport(bilan)
        
        self.assertIn('points_cles', analyse)
        self.assertIn('recommandations', analyse)
        self.assertIn('alertes', analyse)
        
        # FRNG positif doit être dans les points clés
        self.assertTrue(any("FRNG positif" in point for point in analyse['points_cles']))
        
        # Pas d'alertes car tout est positif
        self.assertEqual(len(analyse['alertes']), 0)
    
    def test_analyser_rapport_avec_alertes(self):
        """Test analyse avec alertes."""
        from src.core.simple_models import BilanFonctionnel
        
        bilan = BilanFonctionnel(
            emplois_stables=50000.0,
            ressources_stables=30000.0,
            frng=-20000.0,  # FRNG négatif
            actifs_circulants=35000.0,
            passifs_circulants=12000.0,
            bfr=23000.0,
            tresorerie_active=5000.0,
            tresorerie_passive=8000.0,
            tresorerie_nette=-3000.0,  # Trésorerie négative
            periode="2024"
        )
        
        analyse = self.calculator.analyser_rapport(bilan)
        
        # Doit contenir des alertes
        self.assertGreater(len(analyse['alertes']), 0)
        self.assertGreater(len(analyse['recommandations']), 0)
        
        # Vérifier les alertes spécifiques
        alertes_text = ' '.join(analyse['alertes'])
        self.assertIn("FRNG négatif", alertes_text)
        self.assertIn("Trésorerie négative", alertes_text)


if __name__ == '__main__':
    unittest.main()
