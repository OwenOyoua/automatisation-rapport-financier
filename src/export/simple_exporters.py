"""
Exporteurs simplifiés sans dépendances complexes pour compatibilité Python 3.14.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json

from core.simple_models import BilanFonctionnel, BilanFinancier, PatrimoineEntreprise


class SimpleExporter:
    """Exporteur de base pour les rapports financiers."""
    
    def __init__(self):
        pass
    
    def export_to_json(self, rapport: Any, filename: str, options: Dict[str, Any]) -> str:
        """
        Exporter un rapport au format JSON.
        
        Args:
            rapport: Données du rapport
            filename: Nom du fichier de sortie
            options: Options d'exportation
            
        Returns:
            Chemin du fichier généré
        """
        # Créer le répertoire d'export
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        file_path = export_dir / filename
        
        # Préparer les données
        export_data = {
            'type': self._get_rapport_type(rapport),
            'date_generation': datetime.now().isoformat(),
            'entreprise': options.get('entreprise', 'Entreprise'),
            'periode': options.get('periode', '2024'),
            'devise': options.get('devise', 'MAD'),
            'donnees': rapport.to_dict(),
            'analyse': self._generer_analyse(rapport, options)
        }
        
        # Écrire le fichier JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        return str(file_path)
    
    def export_to_text(self, rapport: Any, filename: str, options: Dict[str, Any]) -> str:
        """
        Exporter un rapport au format texte.
        
        Args:
            rapport: Données du rapport
            filename: Nom du fichier de sortie
            options: Options d'exportation
            
        Returns:
            Chemin du fichier généré
        """
        # Créer le répertoire d'export
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        file_path = export_dir / filename
        
        # Générer le contenu texte
        content = self._generer_rapport_texte(rapport, options)
        
        # Écrire le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path)
    
    def export_to_csv(self, rapport: Any, filename: str, options: Dict[str, Any]) -> str:
        """
        Exporter un rapport au format CSV.
        
        Args:
            rapport: Données du rapport
            filename: Nom du fichier de sortie
            options: Options d'exportation
            
        Returns:
            Chemin du fichier généré
        """
        # Créer le répertoire d'export
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        file_path = export_dir / filename
        
        # Générer le contenu CSV
        content = self._generer_rapport_csv(rapport, options)
        
        # Écrire le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path)
    
    def _get_rapport_type(self, rapport: Any) -> str:
        """Déterminer le type de rapport."""
        if isinstance(rapport, BilanFonctionnel):
            return "Bilan Fonctionnel"
        elif isinstance(rapport, BilanFinancier):
            return "Bilan Financier"
        elif isinstance(rapport, PatrimoineEntreprise):
            return "Patrimoine Entreprise"
        else:
            return "Rapport Inconnu"
    
    def _generer_analyse(self, rapport: Any, options: Dict[str, Any]) -> Dict[str, Any]:
        """Générer une analyse simple du rapport."""
        analyse = {
            'points_cles': [],
            'recommandations': [],
            'alertes': []
        }
        
        if isinstance(rapport, BilanFonctionnel):
            if rapport.frng > 0:
                analyse['points_cles'].append("FRNG positif")
            else:
                analyse['alertes'].append("FRNG négatif")
                analyse['recommandations'].append("Renforcer les ressources stables")
            
            if rapport.tresorerie_nette < 0:
                analyse['alertes'].append("Trésorerie négative")
                analyse['recommandations'].append("Améliorer la gestion de trésorerie")
        
        elif isinstance(rapport, BilanFinancier):
            if rapport.total_actif > 0:
                ratio_endettement = (rapport.total_passif - rapport.capitaux_propres) / rapport.total_actif
                if ratio_endettement > 0.7:
                    analyse['alertes'].append("Endettement élevé")
                    analyse['recommandations'].append("Réduire l'endettement")
        
        elif isinstance(rapport, PatrimoineEntreprise):
            if rapport.ratio_endettement and rapport.ratio_endettement > 0.5:
                analyse['alertes'].append("Endettement patrimonial élevé")
        
        return analyse
    
    def _generer_rapport_texte(self, rapport: Any, options: Dict[str, Any]) -> str:
        """Générer le rapport au format texte."""
        lines = []
        
        # En-tête
        lines.append("=" * 60)
        lines.append(f"RAPPORT FINANCIER - {self._get_rapport_type(rapport)}")
        lines.append("=" * 60)
        lines.append("")
        
        # Informations générales
        lines.append(f"Entreprise: {options.get('entreprise', 'Entreprise')}")
        lines.append(f"Période: {options.get('periode', '2024')}")
        lines.append(f"Devise: {options.get('devise', 'MAD')}")
        lines.append(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lines.append("")
        
        # Contenu spécifique selon le type
        if isinstance(rapport, BilanFonctionnel):
            lines.extend(self._format_bilan_fonctionnel_texte(rapport, options))
        elif isinstance(rapport, BilanFinancier):
            lines.extend(self._format_bilan_financier_texte(rapport, options))
        elif isinstance(rapport, PatrimoineEntreprise):
            lines.extend(self._format_patrimoine_texte(rapport, options))
        
        # Analyse
        analyse = self._generer_analyse(rapport, options)
        if analyse['points_cles'] or analyse['alertes']:
            lines.append("")
            lines.append("ANALYSE ET RECOMMANDATIONS")
            lines.append("-" * 40)
            
            if analyse['points_cles']:
                lines.append("Points clés:")
                for point in analyse['points_cles']:
                    lines.append(f"  ✓ {point}")
                lines.append("")
            
            if analyse['alertes']:
                lines.append("Alertes:")
                for alerte in analyse['alertes']:
                    lines.append(f"  ⚠ {alerte}")
                lines.append("")
            
            if analyse['recommandations']:
                lines.append("Recommandations:")
                for rec in analyse['recommandations']:
                    lines.append(f"  → {rec}")
        
        return "\n".join(lines)
    
    def _format_bilan_fonctionnel_texte(self, bilan: BilanFonctionnel, options: Dict[str, Any]) -> List[str]:
        """Formater le bilan fonctionnel en texte."""
        devise = options.get('devise', 'MAD')
        lines = []
        
        lines.append("BILAN FONCTIONNEL")
        lines.append("-" * 30)
        lines.append(f"Emplois stables:    {bilan.emplois_stables:,.2f} {devise}")
        lines.append(f"Ressources stables:  {bilan.ressources_stables:,.2f} {devise}")
        lines.append(f"FRNG:               {bilan.frng:,.2f} {devise}")
        lines.append("")
        lines.append(f"Actifs circulants:   {bilan.actifs_circulants:,.2f} {devise}")
        lines.append(f"Passifs circulants:  {bilan.passifs_circulants:,.2f} {devise}")
        lines.append(f"BFR:                {bilan.bfr:,.2f} {devise}")
        lines.append("")
        lines.append(f"Trésorerie active:   {bilan.tresorerie_active:,.2f} {devise}")
        lines.append(f"Trésorerie passive:  {bilan.tresorerie_passive:,.2f} {devise}")
        lines.append(f"Trésorerie nette:    {bilan.tresorerie_nette:,.2f} {devise}")
        
        return lines
    
    def _format_bilan_financier_texte(self, bilan: BilanFinancier, options: Dict[str, Any]) -> List[str]:
        """Formater le bilan financier en texte."""
        devise = options.get('devise', 'MAD')
        lines = []
        
        lines.append("ACTIF")
        lines.append("-" * 30)
        lines.append(f"Immobilisations nettes: {bilan.immobilisations_nettes:,.2f} {devise}")
        lines.append(f"Stocks:                {bilan.stocks:,.2f} {devise}")
        lines.append(f"Créances clients:       {bilan.creances_clients:,.2f} {devise}")
        lines.append(f"Autres créances:       {bilan.autres_creances:,.2f} {devise}")
        lines.append(f"Trésorerie active:      {bilan.tresorerie_active:,.2f} {devise}")
        lines.append(f"TOTAL ACTIF:           {bilan.total_actif:,.2f} {devise}")
        lines.append("")
        
        lines.append("PASSIF")
        lines.append("-" * 30)
        lines.append(f"Capital social:         {bilan.capital_social:,.2f} {devise}")
        lines.append(f"Réserves:              {bilan.reserves:,.2f} {devise}")
        lines.append(f"Résultat net:          {bilan.resultat_net:,.2f} {devise}")
        lines.append(f"Capitaux propres:       {bilan.capitaux_propres:,.2f} {devise}")
        lines.append(f"Dettes financières LT:   {bilan.dettes_financieres_lt:,.2f} {devise}")
        lines.append(f"Dettes fournisseurs:     {bilan.dettes_fournisseurs:,.2f} {devise}")
        lines.append(f"Autres dettes CT:       {bilan.autres_dettes_ct:,.2f} {devise}")
        lines.append(f"Trésorerie passive:     {bilan.tresorerie_passive:,.2f} {devise}")
        lines.append(f"TOTAL PASSIF:           {bilan.total_passif:,.2f} {devise}")
        
        return lines
    
    def _format_patrimoine_texte(self, patrimoine: PatrimoineEntreprise, options: Dict[str, Any]) -> List[str]:
        """Formater le patrimoine en texte."""
        devise = options.get('devise', 'MAD')
        lines = []
        
        lines.append("PATRIMOINE DE L'ENTREPRISE")
        lines.append("-" * 30)
        lines.append(f"Actifs économiques:        {patrimoine.actifs_economiques:,.2f} {devise}")
        lines.append(f"Dettes financières:        {patrimoine.dettes_financieres:,.2f} {devise}")
        lines.append(f"Actif net comptable:       {patrimoine.actif_net_comptable:,.2f} {devise}")
        lines.append(f"Capitaux propres retraités: {patrimoine.capitaux_propres_retraites:,.2f} {devise}")
        lines.append(f"PATRIMOINE NET:           {patrimoine.patrimoine_net:,.2f} {devise}")
        lines.append("")
        
        if patrimoine.ratio_endettement is not None:
            lines.append("RATIOS PATRIMONIAUX")
            lines.append("-" * 30)
            lines.append(f"Ratio d'endettement: {patrimoine.ratio_endettement:.2%}")
            lines.append(f"Ratio de solvabilité: {patrimoine.ratio_solvabilite:.2f}")
            lines.append(f"Ratio de liquidité:  {patrimoine.ratio_liquidite:.2f}")
        
        return lines
    
    def _generer_rapport_csv(self, rapport: Any, options: Dict[str, Any]) -> str:
        """Générer le rapport au format CSV."""
        lines = []
        
        # En-tête CSV
        lines.append("Rubrique,Montant,Type")
        
        # Contenu selon le type
        if isinstance(rapport, BilanFonctionnel):
            lines.extend([
                f"Emplois stables,{rapport.emplois_stables},Emploi",
                f"Ressources stables,{rapport.ressources_stables},Ressource",
                f"FRNG,{rapport.frng},Solde",
                f"Actifs circulants,{rapport.actifs_circulants},Actif",
                f"Passifs circulants,{rapport.passifs_circulants},Passif",
                f"BFR,{rapport.bfr},Solde",
                f"Trésorerie active,{rapport.tresorerie_active},Actif",
                f"Trésorerie passive,{rapport.tresorerie_passive},Passif",
                f"Trésorerie nette,{rapport.tresorerie_nette},Solde"
            ])
        
        elif isinstance(rapport, BilanFinancier):
            lines.extend([
                f"Immobilisations nettes,{rapport.immobilisations_nettes},Actif",
                f"Stocks,{rapport.stocks},Actif",
                f"Créances clients,{rapport.creances_clients},Actif",
                f"Autres créances,{rapport.autres_creances},Actif",
                f"Trésorerie active,{rapport.tresorerie_active},Actif",
                f"TOTAL ACTIF,{rapport.total_actif},Total",
                f"Capital social,{rapport.capital_social},Passif",
                f"Réserves,{rapport.reserves},Passif",
                f"Résultat net,{rapport.resultat_net},Passif",
                f"Capitaux propres,{rapport.capitaux_propres},Passif",
                f"Dettes financières LT,{rapport.dettes_financieres_lt},Passif",
                f"Dettes fournisseurs,{rapport.dettes_fournisseurs},Passif",
                f"Autres dettes CT,{rapport.autres_dettes_ct},Passif",
                f"Trésorerie passive,{rapport.tresorerie_passive},Passif",
                f"TOTAL PASSIF,{rapport.total_passif},Total"
            ])
        
        elif isinstance(rapport, PatrimoineEntreprise):
            lines.extend([
                f"Actifs économiques,{rapport.actifs_economiques},Actif",
                f"Dettes financières,{rapport.dettes_financieres},Passif",
                f"Actif net comptable,{rapport.actif_net_comptable},Solde",
                f"Capitaux propres retraités,{rapport.capitaux_propres_retraites},Capitaux",
                f"PATRIMOINE NET,{rapport.patrimoine_net},Total"
            ])
        
        return "\n".join(lines)
