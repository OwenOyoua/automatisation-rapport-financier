"""
Tests d'intégration simplifiés pour l'application complète.
"""

import unittest
import tempfile
import os
from pathlib import Path

from src.core.simple_models import LigneCompte, JeuDonnees, Sens
from src.core.simple_transforms import SimpleReportCalculator
from src.export.simple_exporters import SimpleExporter


class TestIntegrationSimple(unittest.TestCase):
    """Tests d'intégration de bout en bout."""
    
    def setUp(self):
        """Configuration des tests."""
        self.calculator = SimpleReportCalculator()
        self.exporter = SimpleExporter()
        
        # Données de test simples et équilibrées
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
    
    def test_flux_complet_bilan_fonctionnel(self):
        """Test flux complet pour le bilan fonctionnel."""
        # 1. Calcul du bilan fonctionnel
        bilan_fonctionnel = self.calculator.calculer_bilan_fonctionnel(self.donnees_test)
        
        # Vérifications de base
        self.assertIsNotNone(bilan_fonctionnel)
        self.assertEqual(bilan_fonctionnel.periode, "2024")
        
        # 2. Génération de l'analyse
        analyse = self.calculator.analyser_rapport(bilan_fonctionnel)
        self.assertIn('points_cles', analyse)
        self.assertIn('recommandations', analyse)
        self.assertIn('alertes', analyse)
        
        # 3. Export dans tous les formats
        options = {
            'entreprise': 'Test Entreprise',
            'periode': '2024',
            'devise': 'MAD'
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Export JSON
            json_file = self.exporter.export_to_json(
                bilan_fonctionnel, "test_bilan_fonctionnel.json", options
            )
            self.assertTrue(os.path.exists(json_file))
            
            # Export Texte
            text_file = self.exporter.export_to_text(
                bilan_fonctionnel, "test_bilan_fonctionnel.txt", options
            )
            self.assertTrue(os.path.exists(text_file))
            
            # Export CSV
            csv_file = self.exporter.export_to_csv(
                bilan_fonctionnel, "test_bilan_fonctionnel.csv", options
            )
            self.assertTrue(os.path.exists(csv_file))
    
    def test_flux_complet_bilan_financier(self):
        """Test flux complet pour le bilan financier."""
        # 1. Calcul du bilan financier
        bilan_financier = self.calculator.calculer_bilan_financier(self.donnees_test)
        
        self.assertIsNotNone(bilan_financier)
        self.assertEqual(bilan_financier.periode, "2024")
        
        # 2. Vérification de l'équilibre actif/passif
        self.assertAlmostEqual(bilan_financier.total_actif, bilan_financier.total_passif, places=2)
        
        # 3. Export
        options = {
            'entreprise': 'Test Entreprise',
            'periode': '2024',
            'devise': 'MAD'
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = self.exporter.export_to_json(
                bilan_financier, "test_bilan_financier.json", options
            )
            self.assertTrue(os.path.exists(json_file))
    
    def test_flux_complet_patrimoine(self):
        """Test flux complet pour le patrimoine."""
        # 1. Calcul du patrimoine
        patrimoine = self.calculator.calculer_patrimoine(self.donnees_test)
        
        self.assertIsNotNone(patrimoine)
        self.assertEqual(patrimoine.periode, "2024")
        
        # 2. Vérification des ratios
        if patrimoine.actifs_economiques > 0:
            self.assertIsNotNone(patrimoine.ratio_endettement)
            self.assertGreaterEqual(patrimoine.ratio_endettement, 0)
            self.assertLessEqual(patrimoine.ratio_endettement, 1)
        
        # 3. Export
        options = {
            'entreprise': 'Test Entreprise',
            'periode': '2024',
            'devise': 'MAD'
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = self.exporter.export_to_json(
                patrimoine, "test_patrimoine.json", options
            )
            self.assertTrue(os.path.exists(json_file))
    
    def test_coherence_entre_rapports(self):
        """Test cohérence entre les différents rapports."""
        # Calculer tous les rapports
        bilan_fonctionnel = self.calculator.calculer_bilan_fonctionnel(self.donnees_test)
        bilan_financier = self.calculator.calculer_bilan_financier(self.donnees_test)
        patrimoine = self.calculator.calculer_patrimoine(self.donnees_test)
        
        # Vérifier que les totaux sont cohérents
        # Actif total du bilan financier doit correspondre aux actifs économiques
        self.assertAlmostEqual(
            bilan_financier.total_actif,
            patrimoine.actifs_economiques,
            places=2,
            msg="Actif total du bilan financier doit correspondre aux actifs économiques"
        )
        
        # Capitaux propres doivent être cohérents
        self.assertAlmostEqual(
            bilan_financier.capitaux_propres,
            patrimoine.capitaux_propres_retraites,
            places=2,
            msg="Capitaux propres doivent être cohérents entre rapports"
        )
    
    def test_gestion_erreurs(self):
        """Test gestion des erreurs."""
        # Test avec données déséquilibrées
        lignes_desequilibrees = self.lignes_test[:-1]  # Retire la dernière ligne
        
        with self.assertRaises(ValueError):
            JeuDonnees(
                lignes=lignes_desequilibrees,
                periode="2024",
                entreprise="Test"
            )
        
        # Test avec données vides
        with self.assertRaises(ValueError):
            JeuDonnees(
                lignes=[],
                periode="2024",
                entreprise="Test"
            )
    
    def test_performance_grand_volume(self):
        """Test performance avec grand volume de données."""
        # Créer un grand jeu de données
        lignes_grand_volume = []
        
        # Ajouter 100 lignes de test (réduit pour la performance)
        for i in range(100):
            ligne = LigneCompte(
                code_compte=f"3421",
                libelle=f"Client test {i}",
                classe=4,
                sens=Sens.DEBIT if i % 2 == 0 else Sens.CREDIT,
                montant=1000.0,
                periode="2024"
            )
            lignes_grand_volume.append(ligne)
        
        # Ajouter une ligne d'équilibrage
        total_debit = sum(l.montant for l in lignes_grand_volume if l.sens == Sens.DEBIT)
        total_credit = sum(l.montant for l in lignes_grand_volume if l.sens == Sens.CREDIT)
        
        if total_debit > total_credit:
            ligne_equilibrage = LigneCompte(
                code_compte="4411",
                libelle="Équilibrage",
                classe=4,
                sens=Sens.CREDIT,
                montant=total_debit - total_credit,
                periode="2024"
            )
        else:
            ligne_equilibrage = LigneCompte(
                code_compte="5141",
                libelle="Équilibrage",
                classe=5,
                sens=Sens.DEBIT,
                montant=total_credit - total_debit,
                periode="2024"
            )
        
        lignes_grand_volume.append(ligne_equilibrage)
        
        # Créer le jeu de données
        donnees_grand_volume = JeuDonnees(
            lignes=lignes_grand_volume,
            periode="2024",
            entreprise="Test Volume"
        )
        
        # Calculer les rapports (doit fonctionner rapidement)
        import time
        
        start_time = time.time()
        bilan_fonctionnel = self.calculator.calculer_bilan_fonctionnel(donnees_grand_volume)
        bilan_financier = self.calculator.calculer_bilan_financier(donnees_grand_volume)
        patrimoine = self.calculator.calculer_patrimoine(donnees_grand_volume)
        end_time = time.time()
        
        # Vérifier que le calcul est rapide (< 1 seconde)
        self.assertLess(end_time - start_time, 1.0, "Le calcul doit être rapide")
        
        # Vérifier que les résultats sont cohérents
        self.assertIsNotNone(bilan_fonctionnel)
        self.assertIsNotNone(bilan_financier)
        self.assertIsNotNone(patrimoine)


if __name__ == '__main__':
    unittest.main()
