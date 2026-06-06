"""
Helpers de mise en forme des livrables de données (CSV + Excel).

Chaque axe produit :
  - data/axeN/<serie>.csv          (une série = un CSV, format long propre)
  - data/axeN/axeN_<theme>.xlsx    (classeur multi-feuilles + feuille Métadonnées)
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path
import config as C


def ecrire_csv(df: pd.DataFrame, chemin: Path):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False, encoding="utf-8-sig")  # BOM pour Excel FR


def construire_xlsx(chemin: Path, feuilles: dict, metadonnees: pd.DataFrame,
                    titre_classeur: str):
    """
    feuilles : {nom_feuille: DataFrame}
    metadonnees : DataFrame avec colonnes
        [serie, source, url, unite, periode, date_extraction, notes]
    """
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(chemin, engine="xlsxwriter") as xw:
        wb = xw.book
        # Formats
        f_titre = wb.add_format({"bold": True, "font_size": 14,
                                 "font_color": C.COULEURS["encre"]})
        f_entete = wb.add_format({"bold": True, "bg_color": "#2E5E8C",
                                  "font_color": "white", "border": 1,
                                  "align": "center", "valign": "vcenter",
                                  "text_wrap": True})
        f_cell = wb.add_format({"border": 1})
        f_num = wb.add_format({"border": 1, "num_format": "#,##0.00"})
        f_wrap = wb.add_format({"border": 1, "text_wrap": True, "valign": "top"})

        # --- Feuille Notice / métadonnées en premier ---
        ws = wb.add_worksheet("Métadonnées")
        xw.sheets["Métadonnées"] = ws
        ws.write(0, 0, titre_classeur, f_titre)
        ws.write(1, 0, f"Date de collecte : {C.DATE_EXTRACTION}  |  "
                       f"Commande Tribune PZ-0626")
        meta = metadonnees.copy()
        start = 3
        for j, col in enumerate(meta.columns):
            ws.write(start, j, col, f_entete)
        for i, (_, row) in enumerate(meta.iterrows()):
            for j, col in enumerate(meta.columns):
                ws.write(start + 1 + i, j, str(row[col]), f_wrap)
        widths = {"serie": 34, "source": 30, "url": 46, "unite": 22,
                  "periode": 14, "date_extraction": 14, "notes": 52}
        for j, col in enumerate(meta.columns):
            ws.set_column(j, j, widths.get(col, 18))
        ws.freeze_panes(start + 1, 0)

        # --- Feuilles de données ---
        for nom, df in feuilles.items():
            nom = nom[:31]  # limite Excel
            df.to_excel(xw, sheet_name=nom, index=False, startrow=1)
            ws = xw.sheets[nom]
            ws.write(0, 0, nom, f_titre)
            for j, col in enumerate(df.columns):
                ws.write(1, j, col, f_entete)
                # largeur auto approximative
                w = max(12, min(40, int(df[col].astype(str).str.len().max() if len(df) else 12) + 2))
                ws.set_column(j, j, w)
            ws.freeze_panes(2, 0)
    print(f"  ✓ Excel écrit : {chemin.name}  ({len(feuilles)} feuilles + métadonnées)")


def pivot_large(df: pd.DataFrame, index="annee", colonnes="iso3", valeurs="valeur"):
    """Format large pour lecture humaine (années en lignes, pays en colonnes)."""
    p = df.pivot_table(index=index, columns=colonnes, values=valeurs)
    return p.reset_index()
