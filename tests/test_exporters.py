"""
Tests pour les exporteurs simplifiés.
"""

import unittest
import json
import os
import tempfile
from pathlib import Path

from src.core.simple_models import BilanFonctionnel
from src.export.simple_exporters import SimpleExporter


class TestSimpleExporter(unittest.TestCase):
    """Tests pour la classe SimpleExporter."""
    
    def setUp(self):
        """Configuration des tests."""
        self.exporter = SimpleExporter()
        
        # Bilan fonctionnel de test
        self.bilan_test = BilanFonctionnel(
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
        
        self.options_test = {
            'entreprise': 'Test Entreprise',
            'periode': '2024',
            'devise': 'MAD'
        }
    
    def test_get_rapport_type(self):
        """Test identification du type de rapport."""
        rapport_type = self.exporter._get_rapport_type(self.bilan_test)
        self.assertEqual(rapport_type, "Bilan Fonctionnel")
    
    def test_export_to_json(self):
        """Test export au format JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Modifier le répertoire d'export pour le test
            original_export_dir = Path("exports")
            test_export_dir = Path(temp_dir) / "exports"
            test_export_dir.mkdir()
            
            filename = "test_bilan.json"
            filepath = self.exporter.export_to_json(self.bilan_test, filename, self.options_test)
            
            # Vérifier que le fichier existe
            self.assertTrue(os.path.exists(filepath))
            
            # Vérifier le contenu JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertEqual(data['type'], "Bilan Fonctionnel")
            self.assertEqual(data['entreprise'], "Test Entreprise")
            self.assertEqual(data['periode'], "2024")
            self.assertEqual(data['devise'], "MAD")
            self.assertIn('donnees', data)
            self.assertIn('analyse', data)
            self.assertEqual(data['donnees']['frng'], 77000.0)
    
    def test_export_to_text(self):
        """Test export au format texte."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_export_dir = Path(temp_dir) / "exports"
            test_export_dir.mkdir()
            
            filename = "test_bilan.txt"
            filepath = self.exporter.export_to_text(self.bilan_test, filename, self.options_test)
            
            # Vérifier que le fichier existe
            self.assertTrue(os.path.exists(filepath))
            
            # Vérifier le contenu texte
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn("BILAN FONCTIONNEL", content)
            self.assertIn("Test Entreprise", content)
            self.assertIn("2024", content)
            self.assertIn("77000.00 MAD", content)
            self.assertIn("FRNG", content)
    
    def test_export_to_csv(self):
        """Test export au format CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_export_dir = Path(temp_dir) / "exports"
            test_export_dir.mkdir()
            
            filename = "test_bilan.csv"
            filepath = self.exporter.export_to_csv(self.bilan_test, filename, self.options_test)
            
            # Vérifier que le fichier existe
            self.assertTrue(os.path.exists(filepath))
            
            # Vérifier le contenu CSV
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn("Rubrique,Montant,Type", content)
            self.assertIn("Emplois stables,30000.0,Emploi", content)
            self.assertIn("FRNG,77000.0,Solde", content)
    
    def test_generer_analyse(self):
        """Test génération de l'analyse."""
        analyse = self.exporter._generer_analyse(self.bilan_test, self.options_test)
        
        self.assertIn('points_cles', analyse)
        self.assertIn('recommandations', analyse)
        self.assertIn('alertes', analyse)
        
        # FRNG positif doit être dans les points clés
        self.assertTrue(any("FRNG positif" in point for point in analyse['points_cles']))
    
    def test_format_bilan_fonctionnel_texte(self):
        """Test formatage du bilan fonctionnel en texte."""
        lignes = self.exporter._format_bilan_fonctionnel_texte(self.bilan_test, self.options_test)
        
        # Convertir en chaîne pour vérification
        texte = '\n'.join(lignes)
        
        self.assertIn("BILAN FONCTIONNEL", texte)
        self.assertIn("Emplois stables:", texte)
        self.assertIn("30,000.00 MAD", texte)
        self.assertIn("FRNG:", texte)
        self.assertIn("77,000.00 MAD", texte)
    
    def test_format_bilan_financier_texte(self):
        """Test formatage du bilan financier en texte."""
        from src.core.simple_models import BilanFinancier
        
        bilan_financier = BilanFinancier(
            immobilisations_nettes=30000.0,
            stocks=15000.0,
            creances_clients=20000.0,
            autres_creances=0.0,
            tresorerie_active=57000.0,
            total_actif=122000.0,
            capital_social=100000.0,
            reserves=0.0,
            resultat_net=7000.0,
            capitaux_propres=107000.0,
            dettes_financieres_lt=0.0,
            dettes_fournisseurs=12000.0,
            autres_dettes_ct=0.0,
            tresorerie_passive=0.0,
            total_passif=119000.0,
            periode="2024"
        )
        
        lignes = self.exporter._format_bilan_financier_texte(bilan_financier, self.options_test)
        texte = '\n'.join(lignes)
        
        self.assertIn("ACTIF", texte)
        self.assertIn("PASSIF", texte)
        self.assertIn("Immobilisations nettes:", texte)
        self.assertIn("Capital social:", texte)
        self.assertIn("TOTAL ACTIF:", texte)
        self.assertIn("TOTAL PASSIF:", texte)
    
    def test_format_patrimoine_texte(self):
        """Test formatage du patrimoine en texte."""
        from src.core.simple_models import PatrimoineEntreprise
        
        patrimoine = PatrimoineEntreprise(
            actifs_economiques=122000.0,
            dettes_financieres=0.0,
            actif_net_comptable=122000.0,
            capitaux_propres_retraites=107000.0,
            patrimoine_net=122000.0,
            periode="2024",
            ratio_endettement=0.0,
            ratio_solvabilite=None,
            ratio_liquidite=1.0
        )
        
        lignes = self.exporter._format_patrimoine_texte(patrimoine, self.options_test)
        texte = '\n'.join(lignes)
        
        self.assertIn("PATRIMOINE DE L'ENTREPRISE", texte)
        self.assertIn("Actifs économiques:", texte)
        self.assertIn("PATRIMOINE NET:", texte)
        self.assertIn("RATIOS PATRIMONIAUX", texte)
        self.assertIn("Ratio d'endettement:", texte)


if __name__ == '__main__':
    unittest.main()
