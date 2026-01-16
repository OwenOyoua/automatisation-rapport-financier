"""
Modèles de données simplifiés sans Pydantic pour compatibilité Python 3.14.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
from decimal import Decimal


class Sens(Enum):
    """Sens des écritures comptables."""
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


@dataclass
class LigneCompte:
    """Ligne d'écriture comptable."""
    code_compte: str
    libelle: str
    classe: int
    sens: Sens
    montant: float
    periode: str
    
    def __post_init__(self):
        """Validation après création."""
        # Validation du code compte
        if not self.code_compte or len(self.code_compte) < 3:
            raise ValueError("Code compte invalide")
        
        # Validation de la classe
        if not 1 <= self.classe <= 9:
            raise ValueError("Classe doit être entre 1 et 9")
        
        # Validation du montant
        if self.montant < 0:
            raise ValueError("Montant doit être positif")


@dataclass
class JeuDonnees:
    """Ensemble de données comptables."""
    lignes: List[LigneCompte]
    periode: str
    entreprise: str = "Entreprise"
    
    def __post_init__(self):
        """Validation après création."""
        if not self.lignes:
            raise ValueError("Le jeu de données doit contenir au moins une ligne")
        
        # Vérifier l'équilibre débit/crédit
        total_debit = sum(l.montant for l in self.lignes if l.sens == Sens.DEBIT)
        total_credit = sum(l.montant for l in self.lignes if l.sens == Sens.CREDIT)
        
        if abs(total_debit - total_credit) > 0.01:
            raise ValueError(f"Déséquilibre: Débit={total_debit}, Crédit={total_credit}")
    
    def get_total_classe(self, classe: int) -> float:
        """Obtenir le total pour une classe de comptes."""
        return sum(l.montant for l in self.lignes if l.classe == classe)
    
    def get_total_sens(self, sens: Sens) -> float:
        """Obtenir le total par sens."""
        return sum(l.montant for l in self.lignes if l.sens == sens)


@dataclass
class BilanFonctionnel:
    """Bilan fonctionnel simplifié."""
    emplois_stables: float
    ressources_stables: float
    frng: float  # Fonds de roulement net global
    actifs_circulants: float
    passifs_circulants: float
    bfr: float  # Besoin en fonds de roulement
    tresorerie_active: float
    tresorerie_passive: float
    tresorerie_nette: float
    periode: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir en dictionnaire."""
        return {
            'emplois_stables': self.emplois_stables,
            'ressources_stables': self.ressources_stables,
            'frng': self.frng,
            'actifs_circulants': self.actifs_circulants,
            'passifs_circulants': self.passifs_circulants,
            'bfr': self.bfr,
            'tresorerie_active': self.tresorerie_active,
            'tresorerie_passive': self.tresorerie_passive,
            'tresorerie_nette': self.tresorerie_nette,
            'periode': self.periode
        }


@dataclass
class BilanFinancier:
    """Bilan financier simplifié."""
    immobilisations_nettes: float
    stocks: float
    creances_clients: float
    autres_creances: float
    tresorerie_active: float
    total_actif: float
    capital_social: float
    reserves: float
    resultat_net: float
    capitaux_propres: float
    dettes_financieres_lt: float
    dettes_fournisseurs: float
    autres_dettes_ct: float
    tresorerie_passive: float
    total_passif: float
    periode: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir en dictionnaire."""
        return {
            'immobilisations_nettes': self.immobilisations_nettes,
            'stocks': self.stocks,
            'creances_clients': self.creances_clients,
            'autres_creances': self.autres_creances,
            'tresorerie_active': self.tresorerie_active,
            'total_actif': self.total_actif,
            'capital_social': self.capital_social,
            'reserves': self.reserves,
            'resultat_net': self.resultat_net,
            'capitaux_propres': self.capitaux_propres,
            'dettes_financieres_lt': self.dettes_financieres_lt,
            'dettes_fournisseurs': self.dettes_fournisseurs,
            'autres_dettes_ct': self.autres_dettes_ct,
            'tresorerie_passive': self.tresorerie_passive,
            'total_passif': self.total_passif,
            'periode': self.periode
        }


@dataclass
class PatrimoineEntreprise:
    """Patrimoine de l'entreprise simplifié."""
    actifs_economiques: float
    dettes_financieres: float
    actif_net_comptable: float
    capitaux_propres_retraites: float
    patrimoine_net: float
    periode: str
    ratio_endettement: Optional[float] = None
    ratio_solvabilite: Optional[float] = None
    ratio_liquidite: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir en dictionnaire."""
        return {
            'actifs_economiques': self.actifs_economiques,
            'dettes_financieres': self.dettes_financieres,
            'actif_net_comptable': self.actif_net_comptable,
            'capitaux_propres_retraites': self.capitaux_propres_retraites,
            'patrimoine_net': self.patrimoine_net,
            'ratio_endettement': self.ratio_endettement,
            'ratio_solvabilite': self.ratio_solvabilite,
            'ratio_liquidite': self.ratio_liquidite,
            'periode': self.periode
        }
