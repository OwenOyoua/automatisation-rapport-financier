"""
Exporteur de rapports au format PDF.
Génère des documents PDF professionnels avec mise en page complète.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import Color, black, white, grey, lightgrey
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, KeepTogether, Frame, PageTemplate
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from core.models import BilanFonctionnel, BilanFinancier, PatrimoineEntreprise


class PDFExporter:
    """
    Exporteur pour générer des rapports PDF professionnels.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Configurer les styles personnalisés."""
        # Style pour les titres
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=Color(0.2, 0.2, 0.2),
            alignment=TA_CENTER
        ))
        
        # Style pour les sous-titres
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=Color(0.3, 0.3, 0.3)
        ))
        
        # Style pour les paragraphes
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leading=14
        ))
        
        # Style pour les tableaux
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=white
        ))

    def export(self, report_data, filename: str, options: Dict[str, Any]) -> str:
        """
        Exporter un rapport au format PDF.
        
        Args:
            report_data: Données du rapport (BilanFonctionnel, BilanFinancier, etc.)
            filename: Nom du fichier de sortie
            options: Options d'exportation
            
        Returns:
            Chemin du fichier généré
        """
        # Créer le répertoire d'export si nécessaire
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        
        file_path = export_dir / filename
        
        # Créer le document PDF
        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Contenu du document
        story = []
        
        # Page de titre
        story.extend(self.create_title_page(report_data, options))
        
        # Sommaire
        story.append(PageBreak())
        story.extend(self.create_table_of_contents())
        
        # Contenu principal selon le type de rapport
        if isinstance(report_data, BilanFonctionnel):
            story.append(PageBreak())
            story.extend(self.create_bilan_fonctionnel_content(report_data, options))
        elif isinstance(report_data, BilanFinancier):
            story.append(PageBreak())
            story.extend(self.create_bilan_financier_content(report_data, options))
        elif isinstance(report_data, PatrimoineEntreprise):
            story.append(PageBreak())
            story.extend(self.create_patrimoine_content(report_data, options))
        
        # Annexes
        if options.get('include_notes', True):
            story.append(PageBreak())
            story.extend(self.create_annexes(report_data, options))
        
        # Générer le PDF
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return str(file_path)

    def create_title_page(self, report_data, options: Dict[str, Any]) -> list:
        """Créer la page de titre."""
        content = []
        
        # Espacement
        content.append(Spacer(1, 3*cm))
        
        # Titre principal
        if isinstance(report_data, BilanFonctionnel):
            title = "BILAN FONCTIONNEL"
        elif isinstance(report_data, BilanFinancier):
            title = "BILAN FINANCIER"
        elif isinstance(report_data, PatrimoineEntreprise):
            title = "PATRIMOINE DE L'ENTREPRISE"
        else:
            title = "RAPPORT FINANCIER"
        
        content.append(Paragraph(title, self.styles['CustomTitle']))
        content.append(Spacer(1, 1*cm))
        
        # Informations sur l'entreprise
        entreprise = options.get('entreprise', 'Entreprise')
        periode = options.get('periode', '2024')
        devise = options.get('devise', 'MAD')
        
        info_text = f"""
        <b>Entreprise:</b> {entreprise}<br/>
        <b>Période:</b> {periode}<br/>
        <b>Devise:</b> {devise}<br/>
        <b>Date d'édition:</b> {datetime.now().strftime('%d/%m/%Y')}
        """
        
        content.append(Paragraph(info_text, self.styles['CustomBody']))
        content.append(Spacer(1, 2*cm))
        
        # Logo si disponible
        if options.get('include_logo', True):
            # TODO: Ajouter le logo
            content.append(Paragraph("[Logo de l'entreprise]", self.styles['CustomBody']))
            content.append(Spacer(1, 1*cm))
        
        # Footer
        footer_text = "Rapport généré par l'application de comptabilité professionnelle"
        content.append(Paragraph(footer_text, self.styles['CustomBody']))
        
        return content

    def create_table_of_contents(self) -> list:
        """Créer le sommaire."""
        content = []
        
        content.append(Paragraph("SOMMAIRE", self.styles['CustomTitle']))
        content.append(Spacer(1, 1*cm))
        
        toc_data = [
            ["1. Introduction", "3"],
            ["2. Analyse financière", "4"],
            ["3. Tableaux détaillés", "6"],
            ["4. Ratios et indicateurs", "8"],
            ["5. Recommandations", "10"],
            ["6. Annexes", "12"]
        ]
        
        toc_table = Table(toc_data, colWidths=[12*cm, 2*cm])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), grey),
            ('TEXTCOLOR', (0, 0), (0, -1), white),
        ]))
        
        content.append(toc_table)
        content.append(Spacer(1, 1*cm))
        
        return content

    def create_bilan_fonctionnel_content(self, bilan: BilanFonctionnel, options: Dict[str, Any]) -> list:
        """Créer le contenu du bilan fonctionnel."""
        content = []
        
        # Titre
        content.append(Paragraph("BILAN FONCTIONNEL", self.styles['CustomHeading2']))
        
        # Introduction
        intro_text = """
        Le bilan fonctionnel présente l'analyse de la structure financière de l'entreprise 
        selon l'approche fonctionnelle. Il met en évidence les équilibres fondamentaux : 
        Fonds de Roulement Net Global (FRNG), Besoin en Fonds de Roulement (BFR) et Trésorerie.
        """
        content.append(Paragraph(intro_text, self.styles['CustomBody']))
        content.append(Spacer(1, 1*cm))
        
        # Tableau principal
        tableau_data = [
            ["EMPLOIS ET RESSOURCES", "Montant", "Pourcentage"],
            ["EMPLOIS STABLES", f"{float(bilan.emplois_stables):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Ressources stables", f"{float(bilan.ressources_stables):,.2f} {options.get('devise', 'MAD')}", ""],
            ["FRNG", f"{float(bilan.frng):,.2f} {options.get('devise', 'MAD')}", "100%"],
            ["", "", ""],
            ["ACTIFS CIRCULANTS", f"{float(bilan.actifs_circulants):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Passifs circulants", f"{float(bilan.passifs_circulants):,.2f} {options.get('devise', 'MAD')}", ""],
            ["BFR", f"{float(bilan.bfr):,.2f} {options.get('devise', 'MAD')}", ""],
            ["", "", ""],
            ["TRÉSORERIE ACTIVE", f"{float(bilan.tresorerie_active):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Trésorerie passive", f"{float(bilan.tresorerie_passive):,.2f} {options.get('devise', 'MAD')}", ""],
            ["TRÉSORERIE NETTE", f"{float(bilan.tresorerie_nette):,.2f} {options.get('devise', 'MAD')}", ""],
        ]
        
        tableau = Table(tableau_data, colWidths=[6*cm, 4*cm, 2*cm])
        tableau.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.2, 0.2, 0.2)),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 3), (-1, 3), lightgrey),
            ('BACKGROUND', (0, 7), (-1, 7), lightgrey),
            ('BACKGROUND', (0, 10), (-1, 10), lightgrey),
            ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
            ('FONTNAME', (0, 7), (0, 7), 'Helvetica-Bold'),
            ('FONTNAME', (0, 10), (0, 10), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 6), (0, 6), 'Helvetica-Bold'),
            ('FONTNAME', (0, 9), (0, 9), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ]))
        
        content.append(tableau)
        content.append(Spacer(1, 1.5*cm))
        
        # Analyse
        content.append(Paragraph("ANALyse FONCTIONNELLE", self.styles['CustomHeading2']))
        
        analyse_text = self._analyze_bilan_fonctionnel(bilan)
        content.append(Paragraph(analyse_text, self.styles['CustomBody']))
        content.append(Spacer(1, 1*cm))
        
        # Recommandations
        if options.get('include_ratios', True):
            content.append(Paragraph("RECOMMANDATIONS", self.styles['CustomHeading2']))
            
            recommandations = self._get_bilan_fonctionnel_recommendations(bilan)
            for rec in recommandations:
                content.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        return content

    def create_bilan_financier_content(self, bilan: BilanFinancier, options: Dict[str, Any]) -> list:
        """Créer le contenu du bilan financier."""
        content = []
        
        # Titre
        content.append(Paragraph("BILAN FINANCIER", self.styles['CustomHeading2']))
        
        # Introduction
        intro_text = """
        Le bilan financier présente la situation patrimoniale de l'entreprise selon 
        la présentation comptable classique. Il distingue clairement les actifs 
        et les passifs pour évaluer la structure financière et la solvabilité.
        """
        content.append(Paragraph(intro_text, self.styles['CustomBody']))
        content.append(Spacer(1, 1*cm))
        
        # Tableau de l'actif
        content.append(Paragraph("ACTIF", self.styles['CustomHeading2']))
        
        actif_data = [
            ["Rubriques", "Montant", "Pourcentage"],
            ["Immobilisations nettes", f"{float(bilan.immobilisations_nettes):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Stocks", f"{float(bilan.stocks):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Créances clients", f"{float(bilan.creances_clients):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Autres créances", f"{float(bilan.autres_creances):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Trésorerie active", f"{float(bilan.tresorerie_active):,.2f} {options.get('devise', 'MAD')}", ""],
            ["TOTAL ACTIF", f"{float(bilan.total_actif):,.2f} {options.get('devise', 'MAD')}", "100%"],
        ]
        
        actif_table = Table(actif_data, colWidths=[6*cm, 4*cm, 2*cm])
        actif_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.2, 0.2, 0.2)),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, -1), (-1, -1), Color(0.3, 0.3, 0.3)),
            ('TEXTCOLOR', (0, -1), (-1, -1), white),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ]))
        
        content.append(actif_table)
        content.append(Spacer(1, 1*cm))
        
        # Tableau du passif
        content.append(Paragraph("PASSIF", self.styles['CustomHeading2']))
        
        passif_data = [
            ["Rubriques", "Montant", "Pourcentage"],
            ["Capital social", f"{float(bilan.capital_social):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Réserves", f"{float(bilan.reserves):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Résultat net", f"{float(bilan.resultat_net):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Capitaux propres", f"{float(bilan.capitaux_propres):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Dettes financières LT", f"{float(bilan.dettes_financieres_lt):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Dettes fournisseurs", f"{float(bilan.dettes_fournisseurs):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Autres dettes CT", f"{float(bilan.autres_dettes_ct):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Trésorerie passive", f"{float(bilan.tresorerie_passive):,.2f} {options.get('devise', 'MAD')}", ""],
            ["TOTAL PASSIF", f"{float(bilan.total_passif):,.2f} {options.get('devise', 'MAD')}", "100%"],
        ]
        
        passif_table = Table(passif_data, colWidths=[6*cm, 4*cm, 2*cm])
        passif_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.2, 0.2, 0.2)),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, -1), (-1, -1), Color(0.3, 0.3, 0.3)),
            ('TEXTCOLOR', (0, -1), (-1, -1), white),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('BACKGROUND', (0, 3), (0, 3), lightgrey),
            ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ]))
        
        content.append(passif_table)
        content.append(Spacer(1, 1.5*cm))
        
        # Analyse
        content.append(Paragraph("ANALYSE FINANCIÈRE", self.styles['CustomHeading2']))
        
        analyse_text = self._analyze_bilan_financier(bilan)
        content.append(Paragraph(analyse_text, self.styles['CustomBody']))
        
        return content

    def create_patrimoine_content(self, patrimoine: PatrimoineEntreprise, options: Dict[str, Any]) -> list:
        """Créer le contenu du patrimoine."""
        content = []
        
        # Titre
        content.append(Paragraph("PATRIMOINE DE L'ENTREPRISE", self.styles['CustomHeading2']))
        
        # Introduction
        intro_text = """
        L'analyse patrimoniale évalue la valeur réelle de l'entreprise en tenant compte 
        de ses actifs économiques et de ses dettes. Elle permet d'apprécier la solidité 
        financière et la capacité de l'entreprise à faire face à ses engagements.
        """
        content.append(Paragraph(intro_text, self.styles['CustomBody']))
        content.append(Spacer(1, 1*cm))
        
        # Tableau patrimonial
        patrimoine_data = [
            ["ÉLÉMENTS PATRIMONIAUX", "Montant", "Pourcentage"],
            ["Actifs économiques", f"{float(patrimoine.actifs_economiques):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Dettes financières", f"{float(patrimoine.dettes_financieres):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Actif net comptable", f"{float(patrimoine.actif_net_comptable):,.2f} {options.get('devise', 'MAD')}", ""],
            ["Capitaux propres retraités", f"{float(patrimoine.capitaux_propres_retraites):,.2f} {options.get('devise', 'MAD')}", ""],
            ["PATRIMOINE NET", f"{float(patrimoine.patrimoine_net):,.2f} {options.get('devise', 'MAD')}", "100%"],
        ]
        
        patrimoine_table = Table(patrimoine_data, colWidths=[6*cm, 4*cm, 2*cm])
        patrimoine_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.2, 0.2, 0.2)),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, -1), (-1, -1), Color(0.3, 0.3, 0.3)),
            ('TEXTCOLOR', (0, -1), (-1, -1), white),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ]))
        
        content.append(patrimoine_table)
        content.append(Spacer(1, 1.5*cm))
        
        # Ratios patrimoniaux
        if options.get('include_ratios', True):
            content.append(Paragraph("RATIOS PATRIMONIAUX", self.styles['CustomHeading2']))
            
            ratios_data = [
                ["Ratio", "Valeur", "Interprétation"],
                ["Ratio d'endettement", f"{patrimoine.ratio_endettement or 0:.2%}", self._interpret_ratio(patrimoine.ratio_endettement, 0.5, 0.8)],
                ["Ratio de solvabilité", f"{patrimoine.ratio_solvabilite or 0:.2f}", self._interpret_solvability(patrimoine.ratio_solvabilite)],
                ["Ratio de liquidité", f"{patrimoine.ratio_liquidite or 0:.2f}", self._interpret_ratio(patrimoine.ratio_liquidite, 1.0, 0.8)],
            ]
            
            ratios_table = Table(ratios_data, colWidths=[4*cm, 3*cm, 5*cm])
            ratios_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), Color(0.2, 0.2, 0.2)),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            content.append(ratios_table)
            content.append(Spacer(1, 1*cm))
        
        # Analyse
        content.append(Paragraph("ANALYSE PATRIMONIALE", self.styles['CustomHeading2']))
        
        analyse_text = self._analyze_patrimoine(patrimoine)
        content.append(Paragraph(analyse_text, self.styles['CustomBody']))
        
        return content

    def create_annexes(self, report_data, options: Dict[str, Any]) -> list:
        """Créer les annexes du rapport."""
        content = []
        
        content.append(Paragraph("ANNEXES", self.styles['CustomTitle']))
        
        # Méthodologie
        content.append(Paragraph("MÉTHODOLOGIE", self.styles['CustomHeading2']))
        
        methode_text = """
        <b>Source des données:</b> Données comptables fournies par l'entreprise.<br/>
        <b>Période de référence:</b> {periode}<br/>
        <b>Devise:</b> {devise}<br/>
        <b>Normes comptables:</b> Plan Comptable Marocain<br/>
        <b>Date d'édition:</b> {date}<br/><br/>
        
        <b>Méthodes de calcul:</b><br/>
        • FRNG = Ressources stables - Emplois stables<br/>
        • BFR = Actifs circulants - Passifs circulants<br/>
        • Trésorerie nette = Trésorerie active - Trésorerie passive<br/>
        • Ratio d'endettement = Dettes / Actifs économiques<br/>
        • Ratio de solvabilité = Capitaux propres / Dettes<br/>
        • Ratio de liquidité = Actifs liquides / Passifs exigibles
        """.format(
            periode=options.get('periode', '2024'),
            devise=options.get('devise', 'MAD'),
            date=datetime.now().strftime('%d/%m/%Y')
        )
        
        content.append(Paragraph(methode_text, self.styles['CustomBody']))
        content.append(Spacer(1, 1*cm))
        
        # Notes techniques
        content.append(Paragraph("NOTES TECHNIQUES", self.styles['CustomHeading2']))
        
        notes_text = """
        <b>Arrondis:</b> Les montants sont arrondis à deux décimales.<br/>
        <b>Convention de signe:</b> Les soldes positifs indiquent un excédent, les soldes négatifs un déficit.<br/>
        <b>Pourcentages:</b> Calculés par rapport au total de la rubrique principale.<br/><br/>
        
        <b>Avertissement:</b> Ce rapport est basé sur les informations fournies et ne constitue 
        pas un conseil en investissement. Une analyse complémentaire peut être nécessaire 
        pour une prise de décision éclairée.
        """
        
        content.append(Paragraph(notes_text, self.styles['CustomBody']))
        
        return content

    def create_header_footer(self, canvas, doc):
        """Créer l'en-tête et le pied de page."""
        # En-tête
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(grey)
        
        # Ligne supérieure
        canvas.line(2*cm, A4[1] - 2*cm, A4[0] - 2*cm, A4[1] - 2*cm)
        
        # Titre du document
        canvas.drawString(2*cm, A4[1] - 1.5*cm, "Rapport Financier")
        
        # Numéro de page
        canvas.drawRightString(A4[0] - 2*cm, A4[1] - 1.5*cm, f"Page {doc.page}")
        
        # Pied de page
        canvas.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)
        canvas.drawString(2*cm, 1.5*cm, f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        canvas.drawCentredString(A4[0]/2, 1.5*cm, "Application de Comptabilité Professionnelle")
        canvas.drawRightString(A4[0] - 2*cm, 1.5*cm, "Confidentiel")
        
        canvas.restoreState()

    # Méthodes d'analyse
    def _analyze_bilan_fonctionnel(self, bilan: BilanFonctionnel) -> str:
        """Analyser le bilan fonctionnel."""
        analyses = []
        
        if float(bilan.frng) > 0:
            analyses.append("Le Fonds de Roulement Net Global est positif, ce qui indique que les ressources stables financent correctement les emplois stables.")
        else:
            analyses.append("Le FRNG est négatif, ce qui révèle une dépendance aux financements à court terme pour couvrir les investissements.")
        
        if float(bilan.bfr) > 0:
            analyses.append("Le Besoin en Fonds de Roulement est positif, ce qui signifie que le cycle d'exploitation nécessite un financement.")
        else:
            analyses.append("Le BFR est négatif, ce qui constitue une ressource de financement issue de l'exploitation.")
        
        if float(bilan.tresorerie_nette) > 0:
            analyses.append("La trésorerie nette est positive, offrant une marge de sécurité financière.")
        elif float(bilan.tresorerie_nette) < 0:
            analyses.append("La trésorerie nette est négative, ce qui peut créer des tensions de liquidité.")
        
        return " ".join(analyses)

    def _analyze_bilan_financier(self, bilan: BilanFinancier) -> str:
        """Analyser le bilan financier."""
        analyses = []
        
        total_actif = float(bilan.total_actif)
        if total_actif > 0:
            ratio_immobilisations = float(bilan.immobilisations_nettes) / total_actif
            ratio_capitaux_propres = float(bilan.capitaux_propres) / total_actif
            
            if ratio_immobilisations > 0.5:
                analyses.append("L'entreprise présente une structure capitalistique marquée avec des immobilisations importantes.")
            
            if ratio_capitaux_propres > 0.5:
                analyses.append("Les capitaux propres constituent la principale source de financement, assurant une bonne autonomie financière.")
            elif ratio_capitaux_propres < 0.2:
                analyses.append("L'entreprise dépend fortement de l'endettement pour son financement.")
        
        return " ".join(analyses)

    def _analyze_patrimoine(self, patrimoine: PatrimoineEntreprise) -> str:
        """Analyser le patrimoine."""
        analyses = []
        
        if patrimoine.ratio_endettement and patrimoine.ratio_endettement < 0.5:
            analyses.append("L'endettement est maîtrisé, offrant une bonne sécurité financière.")
        elif patrimoine.ratio_endettement and patrimoine.ratio_endettement > 0.8:
            analyses.append("L'endettement est élevé et peut compromettre la solvabilité à long terme.")
        
        if patrimoine.ratio_solvabilite and patrimoine.ratio_solvabilite > 1:
            analyses.append("La solvabilité est assurée avec des capitaux propres supérieurs aux dettes.")
        
        return " ".join(analyses)

    def _get_bilan_fonctionnel_recommendations(self, bilan: BilanFonctionnel) -> list:
        """Obtenir les recommandations pour le bilan fonctionnel."""
        recommendations = []
        
        if float(bilan.frng) < 0:
            recommendations.append("Renforcer les ressources stables (augmentation de capital, dettes à long terme)")
        
        if float(bilan.bfr) > float(bilan.frng):
            recommendations.append("Optimiser le cycle d'exploitation pour réduire le BFR")
        
        if float(bilan.tresorerie_nette) < 0:
            recommendations.append("Améliorer la gestion de trésorerie (negociation des délais, cession d'actifs)")
        
        if not recommendations:
            recommendations.append("La structure financière est équilibrée, maintenir la politique actuelle")
        
        return recommendations

    def _interpret_ratio(self, ratio: Optional[float], good_threshold: float, bad_threshold: float) -> str:
        """Interpréter un ratio."""
        if ratio is None:
            return "Non calculable"
        
        if ratio <= good_threshold:
            return "✅ Bon"
        elif ratio >= bad_threshold:
            return "⚠️ À surveiller"
        else:
            return "🟡 Moyen"

    def _interpret_solvability(self, ratio: Optional[float]) -> str:
        """Interpréter le ratio de solvabilité."""
        if ratio is None:
            return "Non calculable"
        
        if ratio > 1:
            return "✅ Solvable"
        elif ratio > 0.5:
            return "🟡 Solvabilité moyenne"
        else:
            return "⚠️ Solvabilité faible"
