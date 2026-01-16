"""
Version simplifiée de l'application de comptabilité professionnelle.
Compatible avec Python 3.14 et dépendances minimales.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox, QFileDialog
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QFont, QIcon
except ImportError:
    print("PySide6 n'est pas installé. Veuillez exécuter: pip install PySide6")
    sys.exit(1)

from core.simple_models import LigneCompte, JeuDonnees, Sens
from core.simple_transforms import SimpleReportCalculator
from export.simple_exporters import SimpleExporter


class SimpleComptabilityApp(QMainWindow):
    """Application simplifiée de comptabilité."""
    
    def __init__(self):
        super().__init__()
        self.calculator = SimpleReportCalculator()
        self.exporter = SimpleExporter()
        self.donnees_actuelles = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialiser l'interface utilisateur."""
        self.setWindowTitle("Application de Comptabilité Professionnelle")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # En-tête
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Onglets
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Onglet de saisie
        input_tab = self.create_input_tab()
        self.tabs.addTab(input_tab, "Saisie des données")
        
        # Onglet de rapports
        report_tab = self.create_report_tab()
        self.tabs.addTab(report_tab, "Rapports")
        
        # Onglet d'export
        export_tab = self.create_export_tab()
        self.tabs.addTab(export_tab, "Export")
        
        # Status bar
        self.statusBar().showMessage("Prêt")
    
    def create_header(self):
        """Créer l'en-tête de l'application."""
        layout = QHBoxLayout()
        
        # Titre
        title = QLabel("🏢 Application de Comptabilité Professionnelle")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Informations
        self.entreprise_label = QLabel("Entreprise: Non définie")
        self.periode_label = QLabel("Période: 2024")
        layout.addWidget(self.entreprise_label)
        layout.addWidget(self.periode_label)
        
        return layout
    
    def create_input_tab(self):
        """Créer l'onglet de saisie des données."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Formulaire d'entreprise
        form_layout = QHBoxLayout()
        
        self.entreprise_input = QLineEdit("Entreprise Test")
        self.entreprise_input.setPlaceholderText("Nom de l'entreprise")
        form_layout.addWidget(QLabel("Entreprise:"))
        form_layout.addWidget(self.entreprise_input)
        
        self.periode_input = QLineEdit("2024")
        self.periode_input.setPlaceholderText("Période (ex: 2024)")
        form_layout.addWidget(QLabel("Période:"))
        form_layout.addWidget(self.periode_input)
        
        form_layout.addStretch()
        layout.addLayout(form_layout)
        
        # Tableau de saisie
        layout.addWidget(QLabel("Saisie des écritures comptables:"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Code Compte", "Libellé", "Classe", "Sens", "Montant"])
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Ajouter ligne")
        add_btn.clicked.connect(self.add_ligne)
        button_layout.addWidget(add_btn)
        
        clear_btn = QPushButton("🗑️ Vider")
        clear_btn.clicked.connect(self.clear_table)
        button_layout.addWidget(clear_btn)
        
        validate_btn = QPushButton("✅ Valider")
        validate_btn.clicked.connect(self.validate_donnees)
        button_layout.addWidget(validate_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Zone de messages
        self.message_area = QTextEdit()
        self.message_area.setMaximumHeight(100)
        self.message_area.setPlaceholderText("Messages...")
        layout.addWidget(self.message_area)
        
        return widget
    
    def create_report_tab(self):
        """Créer l'onglet des rapports."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Sélection du type de rapport
        select_layout = QHBoxLayout()
        
        select_layout.addWidget(QLabel("Type de rapport:"))
        self.report_type = QComboBox()
        self.report_type.addItems(["Bilan Fonctionnel", "Bilan Financier", "Patrimoine"])
        select_layout.addWidget(self.report_type)
        
        generate_btn = QPushButton("📊 Générer")
        generate_btn.clicked.connect(self.generate_report)
        select_layout.addWidget(generate_btn)
        
        select_layout.addStretch()
        layout.addLayout(select_layout)
        
        # Zone d'affichage du rapport
        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        self.report_display.setFont(QFont("Courier", 10))
        layout.addWidget(self.report_display)
        
        return widget
    
    def create_export_tab(self):
        """Créer l'onglet d'export."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Options d'export
        options_layout = QHBoxLayout()
        
        options_layout.addWidget(QLabel("Format:"))
        self.export_format = QComboBox()
        self.export_format.addItems(["JSON", "Texte", "CSV"])
        options_layout.addWidget(self.export_format)
        
        export_btn = QPushButton("💾 Exporter")
        export_btn.clicked.connect(self.export_report)
        options_layout.addWidget(export_btn)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Instructions
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml("""
        <h3>Instructions d'export</h3>
        <p>1. Générez d'abord un rapport dans l'onglet "Rapports"</p>
        <p>2. Choisissez le format d'export souhaité</p>
        <p>3. Cliquez sur "Exporter" pour sauvegarder le rapport</p>
        
        <h4>Formats disponibles:</h4>
        <ul>
        <li><b>JSON</b>: Format structuré pour intégration</li>
        <li><b>Texte</b>: Format lisible pour impression</li>
        <li><b>CSV</b>: Format tabulaire pour Excel</li>
        </ul>
        """)
        layout.addWidget(instructions)
        
        return widget
    
    def add_ligne(self):
        """Ajouter une ligne au tableau."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Valeurs par défaut
        self.table.setItem(row, 0, QTableWidgetItem("1111"))
        self.table.setItem(row, 1, QTableWidgetItem("Capital social"))
        self.table.setItem(row, 2, QTableWidgetItem("1"))
        self.table.setItem(row, 3, QTableWidgetItem("CREDIT"))
        self.table.setItem(row, 4, QTableWidgetItem("100000"))
    
    def clear_table(self):
        """Vider le tableau."""
        self.table.setRowCount(0)
        self.message_area.clear()
        self.donnees_actuelles = None
    
    def validate_donnees(self):
        """Valider les données saisies."""
        try:
            lignes = []
            
            for row in range(self.table.rowCount()):
                code = self.table.item(row, 0).text()
                libelle = self.table.item(row, 1).text()
                classe = int(self.table.item(row, 2).text())
                sens_text = self.table.item(row, 3).text().upper()
                montant = float(self.table.item(row, 4).text())
                
                sens = Sens.DEBIT if sens_text == "DEBIT" else Sens.CREDIT
                
                ligne = LigneCompte(
                    code_compte=code,
                    libelle=libelle,
                    classe=classe,
                    sens=sens,
                    montant=montant,
                    periode=self.periode_input.text()
                )
                lignes.append(ligne)
            
            # Créer le jeu de données
            self.donnees_actuelles = JeuDonnees(
                lignes=lignes,
                periode=self.periode_input.text(),
                entreprise=self.entreprise_input.text()
            )
            
            # Mettre à jour les labels
            self.entreprise_label.setText(f"Entreprise: {self.entreprise_input.text()}")
            self.periode_label.setText(f"Période: {self.periode_input.text()}")
            
            self.message_area.setText(f"✅ {len(lignes)} lignes validées avec succès")
            self.statusBar().showMessage("Données validées")
            
        except Exception as e:
            self.message_area.setText(f"❌ Erreur de validation: {str(e)}")
            self.statusBar().showMessage("Erreur de validation")
    
    def generate_report(self):
        """Générer le rapport sélectionné."""
        if not self.donnees_actuelles:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord valider les données")
            return
        
        try:
            report_type = self.report_type.currentText()
            
            if report_type == "Bilan Fonctionnel":
                rapport = self.calculator.calculer_bilan_fonctionnel(self.donnees_actuelles)
            elif report_type == "Bilan Financier":
                rapport = self.calculator.calculer_bilan_financier(self.donnees_actuelles)
            elif report_type == "Patrimoine":
                rapport = self.calculator.calculer_patrimoine(self.donnees_actuelles)
            else:
                return
            
            # Exporter en texte pour l'affichage
            options = {
                'entreprise': self.entreprise_input.text(),
                'periode': self.periode_input.text(),
                'devise': 'MAD'
            }
            
            rapport_text = self.exporter._generer_rapport_texte(rapport, options)
            self.report_display.setPlainText(rapport_text)
            
            self.current_report = rapport
            self.statusBar().showMessage(f"{report_type} généré")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du rapport: {str(e)}")
    
    def export_report(self):
        """Exporter le rapport généré."""
        if not hasattr(self, 'current_report'):
            QMessageBox.warning(self, "Attention", "Veuillez d'abord générer un rapport")
            return
        
        try:
            format_type = self.export_format.currentText().lower()
            
            # Nom de fichier par défaut
            filename = f"rapport_{self.report_type.currentText().lower().replace(' ', '_')}_{self.periode_input.text()}"
            
            if format_type == "json":
                filename += ".json"
                filepath = self.exporter.export_to_json(self.current_report, filename, {
                    'entreprise': self.entreprise_input.text(),
                    'periode': self.periode_input.text(),
                    'devise': 'MAD'
                })
            elif format_type == "texte":
                filename += ".txt"
                filepath = self.exporter.export_to_text(self.current_report, filename, {
                    'entreprise': self.entreprise_input.text(),
                    'periode': self.periode_input.text(),
                    'devise': 'MAD'
                })
            elif format_type == "csv":
                filename += ".csv"
                filepath = self.exporter.export_to_csv(self.current_report, filename, {
                    'entreprise': self.entreprise_input.text(),
                    'periode': self.periode_input.text(),
                    'devise': 'MAD'
                })
            
            QMessageBox.information(self, "Export réussi", f"Rapport exporté avec succès:\n{filepath}")
            self.statusBar().showMessage(f"Exporté: {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export: {str(e)}")


def main():
    """Fonction principale."""
    app = QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle("Fusion")
    
    # Créer et afficher la fenêtre principale
    window = SimpleComptabilityApp()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
