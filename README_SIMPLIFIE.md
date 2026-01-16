# 🏢 Application de Comptabilité Professionnelle (Version Simplifiée)

## 📋 Vue d'ensemble

Cette version simplifiée de l'application de comptabilité professionnelle est conçue pour fonctionner avec **Python 3.14** et des dépendances minimales, évitant les problèmes de compatibilité rencontrés avec les packages plus complexes.

## 🚀 Installation et Lancement

### Prérequis
- Python 3.14 (installé)
- Accès internet pour l'installation des dépendances

### Installation
```bash
# Naviguer vers le répertoire du projet
cd C:\Users\HP\Desktop\projet-management

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python src/simple_main.py
```

## 📊 Fonctionnalités

### ✅ Fonctionnalités Implémentées

1. **Interface Utilisateur Moderne**
   - Design PySide6 avec onglets intuitifs
   - Saisie manuelle des écritures comptables
   - Validation en temps réel des données

2. **Gestion des Données Comptables**
   - Saisie des lignes comptables (code, libellé, classe, sens, montant)
   - Validation automatique (équilibre débit/crédit)
   - Support du Plan Comptable Marocain (classes 1-9)

3. **Génération de Rapports**
   - **Bilan Fonctionnel** : FRNG, BFR, Trésorerie
   - **Bilan Financier** : Actif/Passif détaillé
   - **Patrimoine Entreprise** : Analyse patrimoniale complète

4. **Export Multi-Formats**
   - **JSON** : Format structuré pour intégration
   - **Texte** : Format lisible pour impression
   - **CSV** : Format tabulaire pour Excel

5. **Analyse Automatique**
   - Détection des déséquilibres financiers
   - Recommandations personnalisées
   - Alertes sur les ratios critiques

## 🎯 Utilisation

### 1. Saisie des Données
1. Renseignez le nom de l'entreprise et la période
2. Ajoutez les lignes comptables avec le bouton "➕ Ajouter ligne"
3. Utilisez les codes du Plan Comptable Marocain :
   - Classe 1 : Comptes de capitaux
   - Classe 2 : Comptes d'immobilisations
   - Classe 3 : Comptes de stocks
   - Classe 4 : Comptes de tiers
   - Classe 5 : Comptes de trésorerie
4. Cliquez sur "✅ Valider" pour vérifier l'équilibre

### 2. Génération des Rapports
1. Allez dans l'onglet "Rapports"
2. Sélectionnez le type de rapport souhaité
3. Cliquez sur "📊 Générer"
4. Le rapport s'affiche avec l'analyse automatique

### 3. Export des Rapports
1. Après génération, allez dans l'onglet "Export"
2. Choisissez le format (JSON, Texte, CSV)
3. Cliquez sur "💾 Exporter"
4. Les fichiers sont sauvegardés dans le dossier `exports/`

## 📁 Structure du Projet

```
projet-management/
├── src/
│   ├── simple_main.py              # Point d'entrée de l'application
│   ├── core/
│   │   ├── simple_models.py      # Modèles de données (sans Pydantic)
│   │   └── simple_transforms.py # Calculs financiers
│   └── export/
│       ├── __init__.py
│       └── simple_exporters.py   # Export multi-formats
├── exports/                     # Fichiers générés (créé automatiquement)
├── requirements.txt              # Dépendances minimales
└── README_SIMPLIFIE.md         # Ce fichier
```

## 🔧 Dépendances

La version simplifiée utilise uniquement :
- **PySide6** : Interface utilisateur
- **openpyxl** : Support Excel (optionnel)
- **python-docx** : Support Word (optionnel)

**Note** : Les packages suivants nécessitent Python < 3.14 :
- `pandas` : Remplacé par des calculs natifs
- `pydantic` : Remplacé par des dataclasses
- `reportlab` : Remplacé par export texte/JSON

## 📈 Exemple d'Utilisation

### Données de Test
Vous pouvez tester l'application avec ces écritures :

| Code Compte | Libellé | Classe | Sens | Montant |
|-------------|----------|---------|-------|---------|
| 1111 | Capital social | 1 | CREDIT | 100000 |
| 2111 | Frais de constitution | 2 | DEBIT | 5000 |
| 2340 | Matériel de transport | 2 | DEBIT | 25000 |
| 3111 | Stocks de marchandises | 3 | DEBIT | 15000 |
| 3421 | Clients | 4 | DEBIT | 20000 |
| 4411 | Fournisseurs | 4 | CREDIT | 12000 |
| 5141 | Banque | 5 | DEBIT | 50000 |
| 5514 | Caisse | 5 | DEBIT | 7000 |

### Résultats Attendus
- **FRNG** positif : Bon équilibre financier
- **BFR** calculé selon le cycle d'exploitation
- **Trésorerie** nette positive

## 🚨 Limitations

### Version Simplifiée
- Pas d'import de fichiers (PDF, Excel, CSV)
- Pas de génération PDF/Word natifs
- Interface de base sans thème avancé

### Version Complète (Recommandée)
Pour une version complète avec toutes les fonctionnalités :
1. Installer Python 3.9-3.11
2. Utiliser `src/main.py` au lieu de `src/simple_main.py`
3. Installer toutes les dépendances avec `requirements.txt`

## 🔄 Migration vers la Version Complète

Quand vous aurez accès à Python 3.9-3.11 :

```bash
# Installer la version complète
pip install pandas==2.2.3 pydantic==2.5.3 reportlab==4.0.9

# Lancer l'application complète
python src/main.py
```

## 📞 Support

Pour toute question ou problème :
1. Vérifiez que Python 3.14 est bien installé
2. Assurez-vous que les dépendances sont installées
3. Consultez les messages d'erreur dans la console

## 🎯 Prochaines Étapes

1. **Tests Unitaires** : Ajouter des tests pour valider les calculs
2. **Import de Fichiers** : Support CSV/Excel basique
3. **Améliorations UI** : Thème et graphiques
4. **Base de Données** : Sauvegarde des historiques

---

**Version** : 1.0-Simplifiée  
**Compatibilité** : Python 3.14+  
**Licence** : MIT
