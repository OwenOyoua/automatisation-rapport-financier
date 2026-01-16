# 📖 Guide Complet d'Utilisation de l'Application de Comptabilité

##python src/simple_main.py
## 🎯 Table des Matières

1. [Présentation de l'Application](#présentation)
2. [Installation et Lancement](#installation)
3. [Plan Comptable Marocain - Classes Détaillées](#plan-comptable)
4. [Interface Utilisateur](#interface)
5. [Guide de Saisie des Données](#saisie)
6. [Génération des Rapports](#rapports)
7. [Export des Données](#export)
8. [Exemples Pratiques](#exemples)
9. [Dépannage et FAQ](#depannage)

---

## 🚀 Présentation de l'Application

### Objectif
Application de comptabilité professionnelle pour la génération de rapports financiers selon le **Plan Comptable Marocain (PCM)**.

### Fonctionnalités Principales
- ✅ **Saisie des données comptables** avec validation automatique
- ✅ **Calculs financiers** : Bilan fonctionnel, bilan financier, patrimoine
- ✅ **Analyse automatique** avec alertes et recommandations
- ✅ **Export multi-formats** : JSON, Texte, CSV
- ✅ **Interface PySide6** moderne et intuitive
- ✅ **Compatible Python 3.14** sans dépendances complexes

---

## ⚙️ Installation et Lancement

### Prérequis
```bash
# Python 3.14 requis
python --version

# Installation des dépendances
pip install -r requirements.txt
```

### Lancement
```bash
# Depuis le répertoire racine
python src/simple_main.py
```

---

## 📚 Plan Comptable Marocain - Classes Détaillées

### 🏗️ Structure des Classes

#### **Classe 1 : Comptes de Financement Permanent**
**Postes principaux :**
- `1111` - Capital social
- `1117` - Capital personnel
- `1140` - Réserves
- `1151` - Réserves légales
- `1152` - Réserves statutaires
- `1161` - Report à nouveau (solde créditeur)
- `1162` - Report à nouveau (solde débiteur)
- `1191` - Résultat net de l'exercice
- `131` - Subventions d'investissement
- `141` - Emprunts obligataires
- `148` - Autres dettes financières

**Règles :**
- Toujours au **CREDIT** pour les capitaux propres
- Représentent les ressources durables de l'entreprise

#### **Classe 2 : Comptes d'Actif Immobilisé**
**Postes principaux :**
- `2111` - Frais de constitution
- `2113` - Frais d'augmentation de capital
- `2121` - Frais de prospection
- `2131` - Frais de recherche et développement
- `2210` - Immobilisations en recherche et développement
- `2230` - Immobilisations en cours
- `231` - Terrains
- `232` - Constructions
- `233` - Installations techniques
- `2340` - Matériel de transport
- `235` - Mobilier, matériel de bureau
- `239` - Autres immobilisations corporelles

**Règles :**
- Toujours au **DEBIT**
- Représentent les investissements durables

#### **Classe 3 : Comptes d'Actif Circulant (Hors Trésorerie)**
**Postes principaux :**
- `3111` - Stocks de marchandises
- `3112` - Stocks de matières premières
- `3113` - Stocks de produits en cours
- `3114` - Stocks de produits finis
- `3121` - Matières premières
- `315` - Produits finis
- `341` - Fournisseurs débiteurs
- `3421` - Clients
- `3424` - Clients douteux
- `345` - État, débiteur
- `348` - Autres débiteurs

**Règles :**
- Toujours au **DEBIT**
- Représentent les actifs d'exploitation

#### **Classe 4 : Comptes de Passif Circulant (Hors Trésorerie)**
**Postes principaux :**
- `4411` - Fournisseurs
- `4415` - Fournisseurs effets à payer
- `442` - Clients créditeurs
- `443` - Personnel créditeur
- `445` - État, créditeur
- `448` - Autres créanciers
- `449` - Comptes de régularisation

**Règles :**
- Toujours au **CREDIT**
- Représentent les dettes d'exploitation

#### **Classe 5 : Comptes de Trésorerie**
**Postes principaux :**
- `5111` - Chèques à encaisser
- `5113` - Effets à encaisser
- `5141` - Banques
- `5143` - Banques, chèques postaux
- `5161` - Caisses
- `5514` - Caisse

**Règles :**
- **DEBIT** pour les disponibilités
- **CREDIT** pour les découverts bancaires

#### **Classe 6 : Comptes de Charges**
**Postes principaux :**
- `611` - Achats de marchandises
- `612` - Achats de matières premières
- `613` - Autres charges externes
- `614` - Impôts et taxes
- `617` - Charges de personnel
- `619` - Dotations d'exploitation

**Règles :**
- Toujours au **DEBIT**
- Utilisées pour le compte de résultat

#### **Classe 7 : Comptes de Produits**
**Postes principaux :**
- `711` - Ventes de marchandises
- `712` - Ventes de biens produits
- `713` - Ventes de services
- `716` - Subventions d'exploitation
- `718` - Autres produits d'exploitation

**Règles :**
- Toujours au **CREDIT**
- Utilisées pour le compte de résultat

#### **Classes 8 et 9 : Comptes Spéciaux**
- **Classe 8** : Comptes des autres charges et produits
- **Classe 9** : Comptes des engagements hors bilan

---

## 🖥️ Interface Utilisateur

### Structure de l'Interface

L'application comporte **3 onglets principaux** :

#### 📝 **Onglet 1 : Saisie des Données**
```
┌─────────────────────────────────────────────────────────┐
│ Informations Générales                                 │
│ ┌─────────────┐ ┌─────────────┐                      │
│ │ Entreprise   │ │ Période     │                      │
│ └─────────────┘ └─────────────┘                      │
│                                                      │
│ Tableau de Saisie                                     │
│ ┌──────┬─────────────┬───────┬────────┬─────────┐    │
│ │ Code │ Libellé     │ Classe│ Sens   │ Montant  │    │
│ └──────┴─────────────┴───────┴────────┴─────────┘    │
│                                                      │
│ [➕ Ajouter ligne] [✅ Valider]                        │
│                                                      │
│ Zone de Messages                                       │
└─────────────────────────────────────────────────────────┘
```

#### 📊 **Onglet 2 : Rapports**
```
┌─────────────────────────────────────────────────────────┐
│ Type de Rapport                                       │
│ ┌─────────────────────────────────────────────────────┐  │
│ │ ○ Bilan Fonctionnel                               │  │
│ │ ○ Bilan Financier                                │  │
│ │ ○ Patrimoine Entreprise                           │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                      │
│ [📊 Générer]                                         │
│                                                      │
│ Zone d'Affichage des Rapports                          │
└─────────────────────────────────────────────────────────┘
```

#### 💾 **Onglet 3 : Export**
```
┌─────────────────────────────────────────────────────────┐
│ Format d'Export                                       │
│ ┌─────────────────────────────────────────────────────┐  │
│ │ ○ JSON                                           │  │
│ │ ○ Texte                                          │  │
│ │ ○ CSV                                            │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                      │
│ [💾 Exporter]                                        │
│                                                      │
│ Zone de Confirmation                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Guide de Saisie des Données

### Étape 1 : Informations Générales
1. **Entreprise** : Nom de la société
2. **Période** : Année fiscale (ex: 2024)

### Étape 2 : Saisie des Écritures

#### Ajout d'une Ligne
1. Cliquez sur **"➕ Ajouter ligne"**
2. Remplissez les champs :

**Code Compte**
- Format : 4 chiffres (ex: 1111, 2340, 5141)
- Doit correspondre au PCM

**Libellé**
- Description claire de l'opération
- Ex: "Capital social", "Matériel transport"

**Classe**
- S'auto-complète selon le code
- 1 à 9 selon la nature du compte

**Sens**
- Choix dans liste déroulante : `DEBIT` ou `CREDIT`
- Déterminé par la nature du compte

**Montant**
- Format numérique avec point décimal
- Ex: 10000.50

### Étape 3 : Validation

#### Règles de Validation
- ✅ **Équilibre obligatoire** : Total Débit = Total Crédit
- ✅ **Codes valides** : Doivent exister dans le PCM
- ✅ **Montants positifs** : Pas de valeurs négatives
- ✅ **Données complètes** : Tous les champs remplis

#### Messages de Validation
- ✅ **"Données validées avec succès"**
- ❌ **"Déséquilibre: Débit=X, Crédit=Y"**
- ❌ **"Code de compte invalide"**

---

## 📈 Génération des Rapports

### 1. Bilan Fonctionnel

**Objectif** : Analyser l'équilibre financier à court terme

**Indicateurs calculés :**
- **FRNG** (Fonds de Roulement Net Global) = Ressources stables - Emplois stables
- **BFR** (Besoin en Fonds de Roulement) = Actifs circulants - Passifs circulants
- **Trésorerie nette** = FRNG - BFR

**Analyse automatique :**
- ✅ FRNG positif : Bon équilibre financier
- ❌ FRNG négatif : Risque de trésorerie
- ✅ Trésorerie positive : Situation confortable
- ❌ Trésorerie négative : Difficultés de paiement

### 2. Bilan Financier

**Objectif** : Présenter le patrimoine selon les normes financières

**Structure :**
- **Actif** : Immobilisations + Stocks + Créances + Trésorerie
- **Passif** : Capitaux propres + Dettes à long terme + Dettes à court terme

**Vérifications :**
- ✅ Équilibre Actif = Passif
- ✅ Ratios de solvabilité
- ✅ Structure financière

### 3. Patrimoine Entreprise

**Objectif** : Évaluer la valeur patrimoniale

**Indicateurs :**
- **Actifs économiques** : Total des investissements
- **Capitaux propres retraités** : Valeur réelle des capitaux
- **Ratio d'endettement** : Niveau d'endettement
- **Ratio de solvabilité** : Capacité à rembourser les dettes

---

## 💾 Export des Données

### Formats Disponibles

#### 1. **JSON**
- **Usage** : Intégration informatique
- **Structure** : Données structurées
- **Extension** : `.json`

#### 2. **Texte**
- **Usage** : Lecture humaine, impression
- **Structure** : Tableaux formatés
- **Extension** : `.txt`

#### 3. **CSV**
- **Usage** : Import dans Excel/Calc
- **Structure** : Valeurs séparées par virgules
- **Extension** : `.csv`

### Processus d'Export
1. **Choisir le format** dans l'onglet Export
2. **Cliquez sur "💾 Exporter"**
3. **Fichier généré** dans le dossier `exports/`
4. **Nom du fichier** : `type_rapport_periode.format`

---

## 📚 Exemples Pratiques

### Exemple 1 : Entreprise de Services

**Données :**
```
Code    | Libellé                    | Classe | Sens   | Montant
-----------------------------------------------------------------
1111    | Capital social              | 1      | CREDIT | 50000
2111    | Frais constitution         | 2      | DEBIT  | 2000
2332    | Matériel informatique      | 2      | DEBIT  | 15000
3421    | Clients                   | 4      | DEBIT  | 8000
4411    | Fournisseurs              | 4      | CREDIT | 3000
5141    | Banque                   | 5      | DEBIT  | 28000
1191    | Résultat exercice         | 1      | CREDIT | 0
```

**Résultats attendus :**
- FRNG : 33000
- BFR : 5000
- Trésorerie nette : 28000

### Exemple 2 : Entreprise Commerciale

**Données :**
```
Code    | Libellé                    | Classe | Sens   | Montant
-----------------------------------------------------------------
1111    | Capital social              | 1      | CREDIT | 100000
2340    | Matériel transport        | 2      | DEBIT  | 30000
3111    | Stocks marchandises        | 3      | DEBIT  | 25000
3421    | Clients                   | 4      | DEBIT  | 40000
4411    | Fournisseurs              | 4      | CREDIT | 35000
5141    | Banque                   | 5      | DEBIT  | 40000
1191    | Résultat exercice         | 1      | CREDIT | 0
```

**Résultats attendus :**
- FRNG : 70000
- BFR : 30000
- Trésorerie nette : 40000

---

## 🔧 Dépannage et FAQ

### Questions Fréquentes

#### Q1 : Pourquoi ai-je une erreur de déséquilibre ?
**R** : Vérifiez que Total Débit = Total Crédit. C'est la règle fondamentale de la comptabilité.

#### Q2 : Quel code utiliser pour un nouveau poste ?
**R** : Référez-vous au tableau des classes ci-dessus ou utilisez les codes standards du PCM.

#### Q3 : Comment corriger une erreur de saisie ?
**R** : Supprimez la ligne erronée et ajoutez une nouvelle ligne correcte.

#### Q4 : Pourquoi mon rapport ne se génère-t-il pas ?
**R** : Assurez-vous d'abord de valider les données dans l'onglet "Saisie".

#### Q5 : Où sont sauvegardés les exports ?
**R** : Dans le dossier `exports/` à la racine du projet.

### Messages d'Erreur Courants

#### "Déséquilibre: Débit=X, Crédit=Y"
- **Cause** : Les totaux ne sont pas égaux
- **Solution** : Ajoutez une ligne d'équilibrage

#### "Code de compte invalide"
- **Cause** : Le code n'existe pas dans le PCM
- **Solution** : Vérifiez le code dans le tableau des classes

#### "Montant invalide"
- **Cause** : Format incorrect du montant
- **Solution** : Utilisez le point comme séparateur décimal

### Performance

#### Volume de données optimal
- **Recommandé** : < 500 lignes
- **Maximum** : 1000 lignes (performance dégradée)

#### Temps de calcul
- **Petit volume** : < 1 seconde
- **Grand volume** : 1-3 secondes

---

## 📞 Support et Contact

### Documentation Complémentaire
- `README_SIMPLIFIE.md` : Vue d'ensemble technique
- `RAPPORT_TESTS.md` : Résultats des tests
- `requirements.txt` : Dépendances

### Signalement de Bugs
Si vous rencontrez un problème :
1. Notez le message d'erreur exact
2. Décrivez les étapes reproduites
3. Indiquez les données utilisées

---

## 🎯 Conclusion

Cette application professionnelle vous permet de :
- ✅ **Gérer votre comptabilité** selon les normes marocaines
- ✅ **Analyser votre situation financière** en temps réel
- ✅ **Générer des rapports professionnels** pour les décideurs
- ✅ **Exporter vos données** dans plusieurs formats

**L'application est prête à l'emploi pour votre gestion comptable quotidienne !**

---

*© 2024 - Application de Comptabilité Professionnelle*
