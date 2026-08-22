"""Tests unitaires du moteur ReportLab — génération en mémoire uniquement."""
from __future__ import annotations

from health_leads import pdf_generator


def test_graal_pdf_generates_valid_pdf_bytes():
    pdf_bytes = pdf_generator.generate_graal_protocol_pdf("Patrick")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 500


def test_pdf_escapes_markup_in_recipient_name():
    pdf_bytes = pdf_generator.generate_graal_protocol_pdf("<script>alert(1)</script>")
    assert pdf_bytes.startswith(b"%PDF")
