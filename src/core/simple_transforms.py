"""
Transformations financières simplifiées sans pandas pour compatibilité Python 3.14.
"""

from typing import Dict, Any, List
from .simple_models import JeuDonnees, BilanFonctionnel, BilanFinancier, PatrimoineEntreprise, Sens


class SimpleReportCalculator:
    """Calculateur de rapports financiers simplifié."""
    
    def __init__(self):
        pass
    
    def calculer_bilan_fonctionnel(self, donnees: JeuDonnees) -> BilanFonctionnel:
        """
        Calculer le bilan fonctionnel à partir des données comptables.
        
        Args:
            donnees: Jeu de données comptables
            
        Returns:
            BilanFonctionnel calculé
        """
        # Calcul des emplois stables (classe 2)
        emplois_stables = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 2 and l.sens == Sens.DEBIT
        )
        
        # Calcul des ressources stables (classes 1 et 5)
        ressources_stables = 0
        for ligne in donnees.lignes:
            if ligne.classe in [1, 5] and ligne.sens == Sens.CREDIT:
                ressources_stables += ligne.montant
        
        # FRNG = Ressources stables - Emplois stables
        frng = ressources_stables - emplois_stables
        
        # Actifs circulants (classes 3, 4)
        actifs_circulants = sum(
            l.montant for l in donnees.lignes 
            if l.classe in [3, 4] and l.sens == Sens.DEBIT
        )
        
        # Passifs circulants (classes 3, 4)
        passifs_circulants = sum(
            l.montant for l in donnees.lignes 
            if l.classe in [3, 4] and l.sens == Sens.CREDIT
        )
        
        # BFR = Actifs circulants - Passifs circulants
        bfr = actifs_circulants - passifs_circulants
        
        # Trésorerie
        tresorerie_active = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 5 and l.sens == Sens.DEBIT
        )
        
        tresorerie_passive = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 5 and l.sens == Sens.CREDIT
        )
        
        tresorerie_nette = tresorerie_active - tresorerie_passive
        
        return BilanFonctionnel(
            emplois_stables=emplois_stables,
            ressources_stables=ressources_stables,
            frng=frng,
            actifs_circulants=actifs_circulants,
            passifs_circulants=passifs_circulants,
            bfr=bfr,
            tresorerie_active=tresorerie_active,
            tresorerie_passive=tresorerie_passive,
            tresorerie_nette=tresorerie_nette,
            periode=donnees.periode
        )
    
    def calculer_bilan_financier(self, donnees: JeuDonnees) -> BilanFinancier:
        """
        Calculer le bilan financier à partir des données comptables.
        
        Args:
            donnees: Jeu de données comptables
            
        Returns:
            BilanFinancier calculé
        """
        # Actif
        immobilisations_nettes = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 2 and l.sens == Sens.DEBIT
        )
        
        stocks = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 3 and l.sens == Sens.DEBIT
        )
        
        creances_clients = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 4 and l.sens == Sens.DEBIT and l.code_compte.startswith('342')
        )
        
        autres_creances = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 4 and l.sens == Sens.DEBIT and not l.code_compte.startswith('342')
        )
        
        tresorerie_active = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 5 and l.sens == Sens.DEBIT
        )
        
        total_actif = immobilisations_nettes + stocks + creances_clients + autres_creances + tresorerie_active
        
        # Passif
        capital_social = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 1 and l.sens == Sens.CREDIT and l.code_compte.startswith('111')
        )
        
        reserves = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 1 and l.sens == Sens.CREDIT and l.code_compte.startswith('11') and not l.code_compte.startswith('111')
        )
        
        resultat_net = sum(
            l.montant for l in donnees.lignes 
            if l.classe in [6, 7] and l.sens == Sens.CREDIT
        ) - sum(
            l.montant for l in donnees.lignes 
            if l.classe in [6, 7] and l.sens == Sens.DEBIT
        )
        
        capitaux_propres = capital_social + reserves + max(0, resultat_net)
        
        dettes_financieres_lt = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 1 and l.sens == Sens.CREDIT and l.code_compte.startswith('14')
        )
        
        dettes_fournisseurs = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 4 and l.sens == Sens.CREDIT and l.code_compte.startswith('441')
        )
        
        autres_dettes_ct = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 4 and l.sens == Sens.CREDIT and not l.code_compte.startswith('441')
        )
        
        tresorerie_passive = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 5 and l.sens == Sens.CREDIT
        )
        
        total_passif = capitaux_propres + dettes_financieres_lt + dettes_fournisseurs + autres_dettes_ct + tresorerie_passive
        
        return BilanFinancier(
            immobilisations_nettes=immobilisations_nettes,
            stocks=stocks,
            creances_clients=creances_clients,
            autres_creances=autres_creances,
            tresorerie_active=tresorerie_active,
            total_actif=total_actif,
            capital_social=capital_social,
            reserves=reserves,
            resultat_net=resultat_net,
            capitaux_propres=capitaux_propres,
            dettes_financieres_lt=dettes_financieres_lt,
            dettes_fournisseurs=dettes_fournisseurs,
            autres_dettes_ct=autres_dettes_ct,
            tresorerie_passive=tresorerie_passive,
            total_passif=total_passif,
            periode=donnees.periode
        )
    
    def calculer_patrimoine(self, donnees: JeuDonnees) -> PatrimoineEntreprise:
        """
        Calculer le patrimoine de l'entreprise.
        
        Args:
            donnees: Jeu de données comptables
            
        Returns:
            PatrimoineEntreprise calculé
        """
        # Actifs économiques (classes 2, 3, 4, 5)
        actifs_economiques = sum(
            l.montant for l in donnees.lignes 
            if l.classe in [2, 3, 4, 5] and l.sens == Sens.DEBIT
        )
        
        # Dettes financières (classe 1 sauf capitaux propres)
        dettes_financieres = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 1 and l.sens == Sens.CREDIT and not l.code_compte.startswith('11')
        )
        
        # Actif net comptable
        actif_net_comptable = actifs_economiques - dettes_financieres
        
        # Capitaux propres retraités
        capitaux_propres_retraites = sum(
            l.montant for l in donnees.lignes 
            if l.classe == 1 and l.sens == Sens.CREDIT and l.code_compte.startswith('11')
        )
        
        # Patrimoine net
        patrimoine_net = actif_net_comptable
        
        # Ratios
        ratio_endettement = dettes_financieres / actifs_economiques if actifs_economiques > 0 else 0
        ratio_solvabilite = capitaux_propres_retraites / dettes_financieres if dettes_financieres > 0 else 0
        ratio_liquidite = 1.0  # Simplifié
        
        return PatrimoineEntreprise(
            actifs_economiques=actifs_economiques,
            dettes_financieres=dettes_financieres,
            actif_net_comptable=actif_net_comptable,
            capitaux_propres_retraites=capitaux_propres_retraites,
            patrimoine_net=patrimoine_net,
            ratio_endettement=ratio_endettement,
            ratio_solvabilite=ratio_solvabilite,
            ratio_liquidite=ratio_liquidite,
            periode=donnees.periode
        )
    
    def analyser_rapport(self, rapport: Any) -> Dict[str, Any]:
        """
        Analyser un rapport et générer des recommandations.
        
        Args:
            rapport: Rapport à analyser
            
        Returns:
            Dictionnaire d'analyse et recommandations
        """
        analyse = {
            'points_cles': [],
            'recommandations': [],
            'alertes': []
        }
        
        if isinstance(rapport, BilanFonctionnel):
            # Analyse du FRNG
            if rapport.frng > 0:
                analyse['points_cles'].append("FRNG positif : bonne couverture des emplois stables")
            else:
                analyse['alertes'].append("FRNG négatif : dépendance aux financements court terme")
                analyse['recommandations'].append("Renforcer les ressources stables")
            
            # Analyse du BFR
            if rapport.bfr > 0:
                analyse['points_cles'].append(f"BFR positif de {rapport.bfr:,.2f}")
                analyse['recommandations'].append("Optimiser le cycle d'exploitation")
            
            # Analyse de la trésorerie
            if rapport.tresorerie_nette < 0:
                analyse['alertes'].append("Trésorerie négative")
                analyse['recommandations'].append("Améliorer la gestion de trésorerie")
        
        elif isinstance(rapport, BilanFinancier):
            # Analyse de l'endettement
            if rapport.total_actif > 0:
                ratio_endettement = (rapport.total_passif - rapport.capitaux_propres) / rapport.total_actif
                if ratio_endettement > 0.7:
                    analyse['alertes'].append("Taux d'endettement élevé")
                    analyse['recommandations'].append("Réduire l'endettement")
                
                ratio_autonomie = rapport.capitaux_propres / rapport.total_passif
                if ratio_autonomie < 0.3:
                    analyse['alertes'].append("Faible autonomie financière")
        
        elif isinstance(rapport, PatrimoineEntreprise):
            # Analyse des ratios patrimoniaux
            if rapport.ratio_endettement and rapport.ratio_endettement > 0.5:
                analyse['alertes'].append("Endettement patrimonial élevé")
            
            if rapport.ratio_solvabilite and rapport.ratio_solvabilite < 1:
                analyse['alertes'].append("Solvabilité compromise")
        
        return analyse
