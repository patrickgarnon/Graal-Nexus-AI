"""Moteur ReportLab — génération en mémoire du PDF 'Protocole Sommeil &
Récupération 2026' (Jouvence du Graal). Aucune écriture disque.
"""
from __future__ import annotations

import io
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

COLOR_BG_DARK = colors.HexColor("#0F172A")
COLOR_ACCENT_NEON = colors.HexColor("#0284C7")
COLOR_TEXT_LIGHT = colors.HexColor("#F8FAFC")
COLOR_TEXT_MUTED = colors.HexColor("#94A3B8")

LEGAL_DISCLAIMER = (
    "Ce document est fourni à titre informatif et éducatif uniquement. Il ne "
    "constitue ni un avis médical, ni un diagnostic, ni une garantie de "
    "résultat. Aucune promesse de guérison n'est faite ou implicite. "
    "Consultez un professionnel de la santé qualifié avant tout changement "
    "significatif à votre sommeil ou votre mode de vie. Conforme aux "
    "exigences de transparence LPRPDE / RGPD applicables au traitement de "
    "vos données personnelles."
)


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "GraalTitle", parent=base["Title"], textColor=COLOR_TEXT_LIGHT,
            backColor=COLOR_BG_DARK, fontSize=24, leading=28, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "GraalSubtitle", parent=base["Normal"], textColor=COLOR_ACCENT_NEON,
            fontSize=12, leading=16, spaceAfter=12,
        ),
        "heading": ParagraphStyle(
            "GraalHeading", parent=base["Heading2"], textColor=COLOR_ACCENT_NEON,
            fontSize=13, spaceBefore=10, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "GraalBody", parent=base["Normal"], fontSize=10, leading=14,
            textColor=colors.HexColor("#1E293B"),
        ),
        "legal": ParagraphStyle(
            "GraalLegal", parent=base["Normal"], fontSize=7.5, leading=10,
            textColor=COLOR_TEXT_MUTED,
        ),
    }


def generate_graal_protocol_pdf(recipient_name: str) -> bytes:
    """Génère le PDF 'Protocole Sommeil & Récupération 2026' en mémoire."""
    styles = _styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=LETTER,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
        title="Protocole Sommeil & Récupération 2026",
        author="Jouvence du Graal",
    )

    header = Table(
        [
            [Paragraph("Protocole Sommeil &amp; Récupération 2026", styles["title"])],
            [Paragraph("Jouvence du Graal — Guide informatif", styles["subtitle"])],
        ],
        colWidths=[170 * mm],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_BG_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, 0), 16),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
    ]))

    story = [
        header,
        Spacer(1, 10 * mm),
        Paragraph(f"Préparé pour&nbsp;: {_escape(recipient_name)}", styles["body"]),
        Paragraph(f"Date&nbsp;: {date.today().isoformat()}", styles["body"]),
        Spacer(1, 6 * mm),
        HRFlowable(width="100%", color=COLOR_ACCENT_NEON, thickness=1),
        Paragraph("Introduction", styles["heading"]),
        Paragraph(
            "Ce guide présente des principes généraux d'hygiène du sommeil et "
            "de récupération, à titre éducatif uniquement.",
            styles["body"],
        ),
        Spacer(1, 3 * mm),
        Paragraph("Prochaine étape", styles["heading"]),
        Paragraph(
            "Un conseiller Jouvence du Graal communiquera avec vous pour "
            "personnaliser ces recommandations selon votre situation.",
            styles["body"],
        ),
        Spacer(1, 8 * mm),
        HRFlowable(width="100%", color=COLOR_TEXT_MUTED, thickness=0.5),
        Spacer(1, 3 * mm),
        Paragraph(LEGAL_DISCLAIMER, styles["legal"]),
    ]

    doc.build(story)
    return buffer.getvalue()
