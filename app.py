# app.py
# Wichtig:
# DEBUG_MODE vor echter Erhebung auf False lassen.
# credentials.json nicht auf GitHub hochladen.

import base64
import csv
import os
import random
import uuid
from datetime import datetime
from html import escape
from textwrap import dedent

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials
from swipe_component import swipe_component

st.set_page_config(page_title="Cultural Fit Prototype", layout="centered")

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    

/* =========================================================
   FINAL CONSENT INTEGRATION
   Checkbox + Button in die weiße Hauptkarte integrieren
   ========================================================= */

.st-key-consent_integrated_card,
div[class*="st-key-consent_integrated_card"] {
    width: min(820px, 100%) !important;
    margin: 0 auto 0.95rem auto !important;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.05), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.08), transparent 34%),
        rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 30px !important;
    box-shadow: 0 20px 48px rgba(49,92,99,0.11) !important;
    padding: 1.75rem 1.85rem 1.65rem 1.85rem !important;
    text-align: center !important;
    line-height: 1.62 !important;
}

.st-key-consent_integrated_card .hero-title,
div[class*="st-key-consent_integrated_card"] .hero-title,
.st-key-consent_integrated_card .hero-subtitle,
div[class*="st-key-consent_integrated_card"] .hero-subtitle {
    text-align: center !important;
}

.st-key-consent_integrated_card p,
div[class*="st-key-consent_integrated_card"] p {
    text-align: center !important;
    margin-bottom: 0.85rem !important;
}

.st-key-consent_integrated_card .info-grid,
div[class*="st-key-consent_integrated_card"] .info-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    margin-top: 0.9rem !important;
    margin-bottom: 0.95rem !important;
}

.st-key-consent_inline_box,
div[class*="st-key-consent_inline_box"] {
    width: min(640px, 100%) !important;
    margin: 1.05rem auto 1rem auto !important;
    padding: 0.95rem 1rem 1rem 1rem !important;
    background: rgba(248,244,237,0.72) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 22px !important;
    box-shadow: 0 10px 26px rgba(49,92,99,0.06) !important;
}

.st-key-consent_inline_box div[data-testid="stCheckbox"],
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
    display: flex !important;
    justify-content: center !important;
    margin: 0 0 0.55rem 0 !important;
}

.st-key-consent_inline_box div[data-testid="stCheckbox"] label,
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    width: auto !important;
    max-width: 100% !important;
    text-align: left !important;
}

.st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
    margin: 0 !important;
    font-size: 0.95rem !important;
    line-height: 1.32 !important;
    text-align: left !important;
}

.consent-contact {
    margin-top: 0.2rem !important;
    margin-bottom: 0 !important;
    color: var(--text) !important;
}

@media (max-width: 700px) {
    .st-key-consent_integrated_card,
    div[class*="st-key-consent_integrated_card"] {
        border-radius: 24px !important;
        padding: 1.25rem 1rem 1.15rem 1rem !important;
        margin-bottom: 0.65rem !important;
    }

    .st-key-consent_integrated_card .info-grid,
    div[class*="st-key-consent_integrated_card"] .info-grid {
        gap: 0.5rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.85rem !important;
    }

    .st-key-consent_integrated_card .info-box,
    div[class*="st-key-consent_integrated_card"] .info-box {
        min-height: 74px !important;
        padding: 0.72rem 0.34rem !important;
    }

    .st-key-consent_inline_box,
    div[class*="st-key-consent_inline_box"] {
        width: 100% !important;
        border-radius: 18px !important;
        padding: 0.78rem 0.72rem 0.85rem 0.72rem !important;
        margin: 0.85rem auto 0.85rem auto !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        font-size: 0.88rem !important;
        line-height: 1.28 !important;
    }

    .st-key-consent_inline_box .stButton,
    div[class*="st-key-consent_inline_box"] .stButton {
        margin-top: 0.15rem !important;
        margin-bottom: 0 !important;
    }
}

/* ================================
   MOBILE FIX: Consent Screen Typography
   gezielt nur für Screen 2
   ================================ */

@media (max-width: 640px) {

  .st-key-consent_integrated_card,
  div[class*="st-key-consent_integrated_card"] {
    padding: 1.2rem 1rem 1.05rem 1rem !important;
    border-radius: 24px !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy p,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy p {
    font-size: 0.9rem !important;
    line-height: 1.48 !important;
    letter-spacing: 0.005em !important;
    margin: 0 0 0.78rem 0 !important;
    text-align: center !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy .hero-title,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy .hero-title {
    font-size: 1.55rem !important;
    line-height: 1.12 !important;
    margin-bottom: 0.55rem !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy .hero-subtitle,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy .hero-subtitle {
    font-size: 0.9rem !important;
    line-height: 1.42 !important;
    margin-bottom: 0.85rem !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy .info-grid,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 0.48rem !important;
    margin: 0.8rem 0 0.85rem 0 !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy .info-box,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-box {
    min-height: 72px !important;
    padding: 0.68rem 0.35rem !important;
    border-radius: 16px !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy .info-box strong,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-box strong {
    font-size: 0.88rem !important;
    line-height: 1.15 !important;
    margin-bottom: 0.16rem !important;
  }

  .st-key-consent_integrated_card .consent-screen-copy .info-box span,
  div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-box span {
    font-size: 0.72rem !important;
    line-height: 1.18 !important;
  }

  .st-key-consent_inline_box,
  div[class*="st-key-consent_inline_box"] {
    margin: 0.85rem auto 0.85rem auto !important;
    padding: 0.78rem 0.72rem 0.85rem 0.72rem !important;
    border-radius: 18px !important;
  }

  .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
  div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
    font-size: 0.88rem !important;
    line-height: 1.28 !important;
  }

  .st-key-consent_inline_box .stButton,
  div[class*="st-key-consent_inline_box"] .stButton {
    margin-top: 0.15rem !important;
    margin-bottom: 0 !important;
  }

  .st-key-consent_inline_box .stButton > button,
  div[class*="st-key-consent_inline_box"] .stButton > button {
    max-width: 78% !important;
    min-height: 3.05rem !important;
    font-size: 0.98rem !important;
  }

  .consent-contact {
    font-size: 0.88rem !important;
    line-height: 1.38 !important;
    margin-top: 0.75rem !important;
  }
}

/* =========================================================
   FINAL OVERRIDE: Consent Micro Card
   Kompakte, cleane Einwilligungsbox in Screen 2
   GANZ AM ENDE DES CSS-BLOCKS EINSETZEN
   ========================================================= */

.st-key-consent_inline_box,
div[class*="st-key-consent_inline_box"] {
    width: min(620px, 94%) !important;
    margin: 0.8rem auto 0.75rem auto !important;
    padding: 0.75rem 0.85rem 0.8rem 0.85rem !important;
    background: rgba(248, 244, 237, 0.58) !important;
    border: 1px solid rgba(49, 92, 99, 0.10) !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 22px rgba(49, 92, 99, 0.055) !important;
}

/* Checkbox-Zeile kompakt */
.st-key-consent_inline_box div[data-testid="stCheckbox"],
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
    display: flex !important;
    justify-content: center !important;
    margin: 0 0 0.55rem 0 !important;
    padding: 0 !important;
}

/* Checkbox + Text als ruhige Zeile */
.st-key-consent_inline_box div[data-testid="stCheckbox"] label,
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.55rem !important;
    width: auto !important;
    max-width: 100% !important;
    margin: 0 auto !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    text-align: left !important;
}

/* Text kleiner und eleganter */
.st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
    font-size: 0.82rem !important;
    line-height: 1.25 !important;
    letter-spacing: 0 !important;
    margin: 0 !important;
    color: var(--text) !important;
}

/* Button innerhalb der Consent-Box kompakter */
.st-key-consent_inline_box .stButton,
div[class*="st-key-consent_inline_box"] .stButton {
    display: flex !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
}

.st-key-consent_inline_box .stButton > button,
div[class*="st-key-consent_inline_box"] .stButton > button {
    width: min(280px, 72vw) !important;
    max-width: 280px !important;
    min-height: 44px !important;
    padding: 0.55rem 0.95rem !important;
    font-size: 0.9rem !important;
    border-radius: 999px !important;
    margin: 0 auto !important;
}

/* Kontakt enger an Consent-Bereich anbinden */
.consent-contact {
    margin-top: 0.75rem !important;
    margin-bottom: 0 !important;
    font-size: 0.84rem !important;
    line-height: 1.35 !important;
    text-align: center !important;
}

/* Mobile Feinschliff */
@media (max-width: 700px) {
    .st-key-consent_inline_box,
    div[class*="st-key-consent_inline_box"] {
        width: 94% !important;
        margin: 0.7rem auto 0.65rem auto !important;
        padding: 0.68rem 0.65rem 0.72rem 0.65rem !important;
        border-radius: 17px !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"],
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
        margin-bottom: 0.48rem !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        font-size: 0.8rem !important;
        line-height: 1.23 !important;
    }

    .st-key-consent_inline_box .stButton > button,
    div[class*="st-key-consent_inline_box"] .stButton > button {
        width: min(265px, 70vw) !important;
        max-width: 265px !important;
        min-height: 42px !important;
        font-size: 0.88rem !important;
    }

    .consent-contact {
        margin-top: 0.7rem !important;
        font-size: 0.82rem !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL OVERRIDE: Result Assessment Card
   Kompaktere Abstände + dezenter Hinweistext
   ========================================================= */

/* Gesamte Einschätzungskarte kompakter */
.st-key-result_assessment_card,
div[class*="st-key-result_assessment_card"] {
    padding: 1.15rem 1.15rem 0.9rem 1.15rem !important;
    margin-top: 0.55rem !important;
    margin-bottom: 0.8rem !important;
    border-radius: 26px !important;
}

/* Innerer Textblock: weniger Abstand nach unten */
.result-assessment-inner {
    margin: 0 0 0.25rem 0 !important;
    padding: 0 !important;
}

/* Überschrift kompakter */
.result-assessment-inner h3 {
    font-size: 1.42rem !important;
    line-height: 1.12 !important;
    margin: 0 0 0.38rem 0 !important;
    padding: 0 !important;
}

/* Frage direkt unter der Überschrift */
.result-assessment-inner p {
    font-size: 0.98rem !important;
    line-height: 1.35 !important;
    margin: 0 0 0.25rem 0 !important;
    padding: 0 !important;
}

/* Streamlit-Radio-Block näher an die Frage ziehen */
.st-key-result_assessment_card div[data-testid="stRadio"],
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
    margin-top: 0 !important;
    margin-bottom: 0.25rem !important;
    padding-top: 0 !important;
}

/* Abstand zwischen den Radio-Optionen etwas reduzieren */
.st-key-result_assessment_card div[role="radiogroup"],
div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
    gap: 0.04rem !important;
}

/* Einzelne Antwortzeilen kompakter */
.st-key-result_assessment_card div[data-testid="stRadio"] label,
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label {
    min-height: 30px !important;
    padding-top: 0.08rem !important;
    padding-bottom: 0.08rem !important;
}

/* Text der Antwortoptionen etwas ruhiger */
.st-key-result_assessment_card div[data-testid="stRadio"] label p,
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label p {
    font-size: 0.96rem !important;
    line-height: 1.25 !important;
    margin: 0 !important;
}

/* Button näher an die Antwortliste */
.st-key-result_assessment_card .stButton,
div[class*="st-key-result_assessment_card"] .stButton {
    margin-top: 0.2rem !important;
    margin-bottom: 0.1rem !important;
}

/* Hinweis unten: kleiner, nicht fett, dezenter */
.result-assessment-hint {
    font-size: 0.78rem !important;
    line-height: 1.28 !important;
    font-weight: 400 !important;
    color: var(--muted) !important;
    text-align: center !important;
    margin-top: 0.35rem !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
}

/* Falls Streamlit/Browser den Hinweistext intern fett macht */
.result-assessment-hint,
.result-assessment-hint * {
    font-weight: 400 !important;
}



</style>
    """,
    unsafe_allow_html=True,
)

SHOW_ADMIN_PANEL = False
CSV_FILEPATH = "responses.csv"
GIVEAWAY_CSV_FILEPATH = "giveaway_entries.csv"
DEBUG_MODE = False

GOOGLE_SHEET_ID = "1F43LmzUGQRqwCpcHsuAMMEEV6xB95FVXa8nVzMDD-rE"

BOOK_COVER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "crashkurs_cover_sharp.png",
)


def image_to_base64(image_path):
    if not os.path.exists(image_path):
        return ""

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def render_giveaway_banner():
    cover_b64 = image_to_base64(BOOK_COVER_PATH)

    if cover_b64:
        cover_html = (
            '<div class="book-giveaway-cover-box-v2">'
            f'<img class="book-giveaway-cover-v2" src="data:image/png;base64,{cover_b64}" '
            'alt="Crashkurs People, Culture & Change" />'
            '</div>'
        )
        card_class = "book-giveaway-card-v2 screen-fade has-book-cover-v2"
    else:
        cover_html = ""
        card_class = "book-giveaway-card-v2 screen-fade no-book-cover-v2"

    return (
        f'<div class="{card_class}">'
        '<div class="book-giveaway-inner-v2">'
        f'{cover_html}'
        '<div class="book-giveaway-content-v2">'
        '<div class="book-giveaway-title-v2">Deine Teilnahme kann sich doppelt lohnen</div>'
        '<p class="book-giveaway-text-v2">'
        'Finde heraus, welches Arbeitsumfeld zu dir passt — und sichere dir die Chance auf eines von fünf Exemplaren von '
        '<strong>„Crashkurs People, Culture &amp; Change“</strong>.'
        '</p>'
        '<p class="book-giveaway-text-v2">'
        'Das Buch zeigt kompakt und praxisnah, wie moderne Transformation im Bereich People &amp; Culture verstanden, '
        'gestaltet und mit konkreten Tools umgesetzt werden kann.'
        '</p>'
        '<div class="book-giveaway-note-v2">'
        '<span class="book-giveaway-note-icon-v2">i</span>'
        '<span>Die Teilnahme an der Verlosung ist am Ende der Studie freiwillig möglich.</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )

st.markdown(
    """
    <style>
    :root {
        --primary-color: #6BAA75 !important;
        --primary-color-rgb: 107, 170, 117 !important;

        --bg: #FAF7F2;
        --card: #FFFFFF;
        --primary: #315C63;
        --primary-dark: #1F3A5F;
        --accent: #F2B872;
        --text: #2B2B2B;
        --muted: #667085;
        --border: #E5E1DA;
        --soft: #F3EEE7;
        --success: #6BAA75;
        --danger: #D98282;
    }

    .stApp {
    background: var(--bg);
    color: var(--text);
    --primary-color: #6BAA75 !important;
    --primary-color-rgb: 107, 170, 117 !important;
}

    .block-container {
        max-width: 920px;
        padding-top: 3.2rem;
        padding-bottom: 2.5rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    h1, h2, h3 {
        color: var(--primary) !important;
        letter-spacing: -0.025em;
    }

    p, li, label, .stMarkdown, .stCaption {
        color: var(--text) !important;
    }

    div[data-testid="stProgressBar"] > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent));
    }

.welcome-wrap {
    min-height: auto;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    border-radius: 32px;
    padding: 2.6rem 1.4rem 3.2rem 1.4rem;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.16), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.28), transparent 34%),
        linear-gradient(135deg, #FAF7F2 0%, #E8F0EF 48%, #F6EBDD 100%);
    box-shadow: inset 0 0 0 1px rgba(49,92,99,0.08);
    position: relative;
}

    .welcome-card {
        width: min(720px, 100%);
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(49,92,99,0.12);
        border-radius: 30px;
        padding: 2.1rem 2.2rem;
        box-shadow: 0 22px 55px rgba(49,92,99,0.15);
        backdrop-filter: blur(8px);
        text-align: left;
    }

    .screen-frame {
    border-radius: 32px;
    padding: 2.6rem 1.4rem 3.2rem 1.4rem;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.16), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.28), transparent 34%),
        linear-gradient(135deg, #FAF7F2 0%, #E8F0EF 48%, #F6EBDD 100%);
    box-shadow: inset 0 0 0 1px rgba(49,92,99,0.08);
    margin-bottom: 1rem;
}

.screen-frame-soft {
    border-radius: 32px;
    padding: 2.4rem 1.4rem 2.8rem 1.4rem;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.11), transparent 36%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.18), transparent 36%),
        linear-gradient(135deg, #FAF7F2 0%, #EDF3F1 50%, #F8EBD8 100%);
    box-shadow: inset 0 0 0 1px rgba(49,92,99,0.07);
    margin-bottom: 1rem;
}

.screen-card-main {
    width: min(720px, 100%);
    margin: 0 auto;
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(49,92,99,0.12);
    border-radius: 30px;
    padding: 2.1rem 2.2rem;
    box-shadow: 0 22px 55px rgba(49,92,99,0.13);
    backdrop-filter: blur(8px);
    text-align: left;
}

.result-assessment-wrap h3 {
    color: var(--primary) !important;
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.45rem;
}

.result-assessment-wrap p {
    margin-bottom: 0.7rem;
}

.result-assessment-wrap div[data-testid="stRadio"] {
    margin-top: -0.2rem;
}

.result-assessment-wrap div[role="radiogroup"] {
    gap: 0.25rem;
}

.result-assessment-wrap .stButton {
    margin-top: 0.65rem;
}

.screen-card-info {
    width: min(820px, 100%);
    margin: 0 auto;
    background: rgba(255,255,255,0.95);
    border: 1px solid rgba(49,92,99,0.12);
    border-radius: 30px 30px 20px 20px;
    padding: 1.7rem 1.8rem;
    box-shadow: 0 20px 48px rgba(49,92,99,0.11);
    backdrop-filter: blur(8px);
    text-align: left;
    line-height: 1.65;
}

.screen-card-info p {
    margin-top: 0;
    margin-bottom: 1rem;
}

.consent-action-area [data-testid="stCheckbox"] label {
    font-size: 1rem;
    color: var(--text) !important;
}

.consent-action-area .custom-muted {
    text-align: center;
}

.consent-spacing {
    height: 0.7rem;
}

.screen-fade {
    animation: screenFade 0.28s ease-out both;
}

@keyframes screenFade {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

    .welcome-pill {
        display: inline-block;
        background: rgba(242,184,114,0.26);
        border: 1px solid rgba(242,184,114,0.55);
        color: var(--primary);
        border-radius: 999px;
        padding: 0.32rem 0.8rem;
        font-size: 0.88rem;
        font-weight: 750;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 850;
        color: var(--primary);
        margin-bottom: 0.55rem;
        letter-spacing: -0.04em;
        line-height: 1.08;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.65;
        margin-bottom: 1.2rem;
    }

    .text-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 16px 38px rgba(49,92,99,0.10);
        margin-bottom: 1rem;
        color: var(--text);
        line-height: 1.65;
    }

    .topmatch-card {
        background:
            radial-gradient(circle at top right, rgba(242,184,114,0.22), transparent 38%),
            linear-gradient(180deg, #FFFFFF 0%, #F8F4ED 100%);
        border: 1px solid rgba(49,92,99,0.14);
        border-radius: 26px;
        padding: 1.5rem 1.55rem;
        box-shadow: 0 18px 42px rgba(49,92,99,0.13);
        margin-bottom: 1rem;
        color: var(--text);
        line-height: 1.65;
    }

    .result-hero-card {
    background:
        radial-gradient(circle at top right, rgba(242,184,114,0.26), transparent 38%),
        radial-gradient(circle at bottom left, rgba(49,92,99,0.10), transparent 40%),
        linear-gradient(135deg, #FFFFFF 0%, #F8F4ED 100%);
    border: 1px solid rgba(49,92,99,0.14);
    border-radius: 28px;
    padding: 1.55rem 1.65rem;
    box-shadow: 0 20px 48px rgba(49,92,99,0.13);
    margin-bottom: 1rem;
    color: var(--text);
}

.result-kicker {
    color: var(--primary);
    font-size: 0.9rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.result-company {
    color: var(--primary);
    font-size: 2.15rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    line-height: 1.08;
    margin-bottom: 0.75rem;
}

.result-score-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 0.8rem;
    flex-wrap: wrap;
}

.result-score {
    background: var(--primary);
    color: #FFFFFF;
    border-radius: 999px;
    padding: 0.55rem 0.95rem;
    font-size: 1.35rem;
    font-weight: 850;
    box-shadow: 0 10px 24px rgba(49,92,99,0.16);
}

.result-score-label {
    color: var(--muted);
    font-size: 0.95rem;
}

.result-meta-row {
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;
    margin-top: 0.75rem;
}

.result-pill {
    display: inline-block;
    background: rgba(49,92,99,0.09);
    border: 1px solid rgba(49,92,99,0.16);
    color: var(--primary);
    border-radius: 999px;
    padding: 0.35rem 0.8rem;
    font-size: 0.86rem;
    font-weight: 750;
}

.result-next-note {
    background: rgba(242,184,114,0.16);
    border: 1px solid rgba(242,184,114,0.42);
    border-radius: 18px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    line-height: 1.55;
}

.result-details-title {
    color: var(--primary);
    font-size: 1.45rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-top: 1.4rem;
    margin-bottom: 0.75rem;
}

/* Schöne Streamlit-Karte für die erste Einschätzung */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-assessment-marker) {
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(49,92,99,0.13) !important;
    border-radius: 26px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.11) !important;
    margin-top: 0.9rem !important;
    margin-bottom: 1.25rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-assessment-marker) > div {
    padding: 1.3rem 1.5rem 1.25rem 1.5rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-assessment-marker) div[data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

.result-assessment-marker {
    display: none;
}

.result-radio-label {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.2rem;
    margin-bottom: -0.15rem;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-assessment-marker) div[data-testid="stRadio"] {
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.result-assessment-marker) div[role="radiogroup"] {
    gap: 0.18rem !important;
}

.result-assessment-hint {
    text-align: center;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.2rem;
}

    .ranking-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 10px 25px rgba(49,92,99,0.07);
    }

    .custom-muted {
        color: var(--muted);
        font-size: 0.95rem;
    }

    .small-pill {
        display: inline-block;
        background: rgba(49,92,99,0.09);
        border: 1px solid rgba(49,92,99,0.16);
        color: var(--primary);
        border-radius: 999px;
        padding: 0.28rem 0.75rem;
        font-size: 0.86rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }

    .big-number {
        font-size: 2rem;
        font-weight: 850;
        color: var(--primary);
        margin: 0.2rem 0 0.2rem 0;
        letter-spacing: -0.03em;
    }

    .assessment-help {
        text-align: center;
        color: var(--muted);
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }

    .thanks-wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 4.5rem;
}

.thanks-card {
    width: min(760px, 100%);
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(49,92,99,0.12);
    border-radius: 30px;
    padding: 2.2rem 2.4rem;
    box-shadow: 0 22px 55px rgba(49,92,99,0.12);
    text-align: center;
}

.thanks-icon {
    width: 54px;
    height: 54px;
    border-radius: 999px;
    background: rgba(107,170,117,0.16);
    border: 1px solid rgba(107,170,117,0.35);
    color: var(--success);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    font-weight: 850;
    margin: 0 auto 1rem auto;
}

.thanks-title {
    color: var(--primary);
    font-size: 2.1rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    line-height: 1.12;
    margin-bottom: 0.65rem;
}

.thanks-text {
    color: var(--text);
    font-size: 1.05rem;
    line-height: 1.6;
}

    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .info-box {
        background: #F8F4ED;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 0.95rem;
        text-align: center;
    }

    .info-box strong {
        color: var(--primary);
        display: block;
        margin-bottom: 0.25rem;
    }

    .info-box span {
        color: var(--muted);
        font-size: 0.9rem;
    }

    .instruction-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .instruction-box {
        flex: 1;
        background: #F8F4ED;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
    }

    .instruction-box strong {
        color: var(--primary);
        display: block;
        margin-bottom: 0.3rem;
    }

    .instruction-box span {
        color: var(--muted);
        font-size: 0.95rem;
    }

    .study-progress {
        background: rgba(255,255,255,0.78);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 0.95rem 1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 12px 30px rgba(49,92,99,0.08);
    }

    .study-progress-label {
        color: var(--primary);
        font-size: 0.86rem;
        font-weight: 750;
        margin-bottom: 0.55rem;
    }

    .study-progress-track {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.55rem;
    }

    .study-progress-step {
        border-radius: 999px;
        padding: 0.55rem 0.75rem;
        text-align: center;
        font-size: 0.86rem;
        border: 1px solid var(--border);
        color: var(--muted);
        background: #F8F4ED;
    }

    .study-progress-step.done {
        color: var(--primary);
        border-color: rgba(49,92,99,0.22);
        background: rgba(49,92,99,0.08);
        font-weight: 700;
    }

    .study-progress-step.active {
        color: #FFFFFF;
        border-color: var(--primary);
        background: linear-gradient(90deg, var(--primary), #47747A);
        font-weight: 750;
    }

    .result-profile-text {
    font-size: 1rem;
    line-height: 1.55;
    color: var(--text) !important;
    margin-top: 0.75rem;
    margin-bottom: 0.55rem;
    max-width: 760px;
}

.result-method-text {
    font-size: 0.94rem;
    line-height: 1.5;
    color: var(--muted) !important;
    margin-bottom: 0.75rem;
}

    .soft-note {
        background: rgba(242,184,114,0.18);
        border: 1px solid rgba(242,184,114,0.46);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        color: var(--text);
        margin-bottom: 1rem;
        line-height: 1.65;
    }

    .questionnaire-header {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1rem;
        box-shadow: 0 16px 38px rgba(49,92,99,0.10);
    }

    .stButton > button {
        background: var(--primary);
        color: #FFFFFF;
        border: 1px solid var(--primary);
        border-radius: 999px;
        padding: 0.62rem 1.15rem;
        font-weight: 750;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        background: #274E55;
        border-color: #274E55;
        color: #FFFFFF;
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(49,92,99,0.18);
    }

    .stCheckbox label, .stRadio label {
        color: var(--text) !important;
    }

    /* Checkbox-Farbe auf Grün/Teal setzen */
div[data-testid="stCheckbox"] input[type="checkbox"] {
    accent-color: var(--success) !important;
}

div[data-testid="stCheckbox"] input[type="checkbox"]:checked {
    accent-color: var(--success) !important;
}

/* Fallback für neuere Streamlit/BaseWeb-Checkboxen */
[data-testid="stCheckbox"] [data-baseweb="checkbox"] div[aria-checked="true"] {
    background-color: var(--success) !important;
    border-color: var(--success) !important;
}

[data-testid="stCheckbox"] [data-baseweb="checkbox"] svg {
    fill: #FFFFFF !important;
}

/* Stärkerer Override gegen Streamlit-Standard-Rot */
[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {
    background-color: var(--success) !important;
    border-color: var(--success) !important;
}

[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] svg {
    fill: #FFFFFF !important;
}

    .stAlert {
        border-radius: 18px;
    }

        .stButton > button,
    .stButton > button *,
    button[kind="primary"],
    button[kind="primary"] * {
        color: #FFFFFF !important;
    }

    .stButton > button {
        background: var(--primary) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--primary) !important;
        border-radius: 999px !important;
        padding: 0.68rem 1.25rem !important;
        font-weight: 750 !important;
        transition: all 0.18s ease !important;
        box-shadow: 0 10px 24px rgba(49,92,99,0.16);
    }

    .stButton > button:hover {
        background: #274E55 !important;
        border-color: #274E55 !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(49,92,99,0.18);
    }

    .stButton > button:disabled,
    .stButton > button:disabled * {
        color: rgba(255,255,255,0.72) !important;
    }

    div[data-testid="stRadio"] input[type="radio"] {
        accent-color: var(--primary) !important;
    }

    div[data-testid="stRadio"] input[type="radio"]:checked {
        accent-color: var(--success) !important;
    }

    .stRadio [role="radiogroup"] label {
        color: var(--text) !important;
    }

.welcome-action {
    margin-top: 0.8rem;
    margin-bottom: 2rem;
    position: relative;
    z-index: 20;
}

    div[data-testid="stRadio"] input[type="radio"] {
        accent-color: var(--success) !important;
    }

    div[data-testid="stRadio"] input[type="radio"]:checked {
        accent-color: var(--success) !important;
    }

    div[data-testid="stRadio"] label:has(input[type="radio"]:checked) span {
        color: var(--primary) !important;
        font-weight: 700 !important;
    }

    div[role="radiogroup"] input[type="radio"] {
        accent-color: var(--success) !important;
    }

    div[role="radiogroup"] input[type="radio"]:checked {
        accent-color: var(--success) !important;
    }
    
    /* Ergebnis-Screen: weiße Karte für die erste Einschätzung */
div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 28px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    margin-top: 0.35rem !important;
    margin-bottom: 1.35rem !important;
}

div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

.result-assessment-marker {
    display: none;
}

.result-radio-label {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.15rem;
    margin-bottom: -0.15rem;
}

div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="stRadio"] {
    margin-top: 0 !important;
    margin-bottom: 0.45rem !important;
}

div[data-testid="column"]:has(.result-assessment-marker) div[role="radiogroup"] {
    gap: 0.12rem !important;
}

.result-assessment-hint {
    text-align: center;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

.result-radio-label {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.15rem;
}

.result-assessment-hint {
    text-align: center;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.25rem;
}

    @media (max-width: 700px) {
        .block-container {
            padding-top: 1.6rem;
        .thanks-wrap {
    margin-top: 2.2rem !important;
}

.thanks-card {
    width: 100% !important;
    padding: 1.45rem 1.15rem !important;
    border-radius: 22px !important;
}

.thanks-title {
    font-size: 1.65rem !important;
}

.thanks-text {
    font-size: 0.96rem !important;
}
        }

.welcome-wrap {
    min-height: auto;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    border-radius: 32px;
    padding: 2.6rem 1.4rem 3.2rem 1.4rem;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.16), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.28), transparent 34%),
        linear-gradient(135deg, #FAF7F2 0%, #E8F0EF 48%, #F6EBDD 100%);
    box-shadow: inset 0 0 0 1px rgba(49,92,99,0.08);
    position: relative;
}

        .welcome-card {
            padding: 1.45rem 1.25rem;
            border-radius: 20px;
        }

        .info-grid {
            grid-template-columns: 1fr;
        }

        .instruction-row {
            flex-direction: column;
        }

        .study-progress-track {
            grid-template-columns: 1fr;
        }

        .hero-title {
            font-size: 2rem;
        }
    }

/* FINAL OVERRIDE: Einschätzungskarte weiß machen */
div[data-testid="column"]:has(.result-assessment-marker) {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 28px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    padding: 1.25rem 1.45rem 1.15rem 1.45rem !important;
    margin-top: 0.35rem !important;
    margin-bottom: 1.35rem !important;
}

/* Innere Ebenen ebenfalls weiß halten */
div[data-testid="column"]:has(.result-assessment-marker) > div,
div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="stVerticalBlock"],
div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="element-container"],
div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="stHorizontalBlock"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
}

.result-assessment-marker {
    display: none !important;
}

.result-radio-label {
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.15rem !important;
    margin-bottom: -0.15rem !important;
}

div[data-testid="column"]:has(.result-assessment-marker) div[data-testid="stRadio"] {
    margin-top: 0 !important;
    margin-bottom: 0.45rem !important;
}

div[data-testid="column"]:has(.result-assessment-marker) div[role="radiogroup"] {
    gap: 0.12rem !important;
}

.result-assessment-hint {
    text-align: center !important;
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.25rem !important;
}

.result-radio-label {
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.15rem !important;
    margin-bottom: -0.15rem !important;
}

.result-assessment-hint {
    text-align: center !important;
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.25rem !important;
}

/* Ergebnis-Screen: gesamte Einschätzungsbox als Karte */
.st-key-result_assessment_card,
div[class*="st-key-result_assessment_card"] {
    width: 100% !important;
    max-width: none !important;
    box-sizing: border-box !important;
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 30px !important;
    box-shadow: 0 20px 48px rgba(49,92,99,0.11) !important;
    padding: 1.55rem 1.75rem 1.15rem 1.75rem !important;
    margin: 1.05rem auto 1.85rem auto !important;
}

.st-key-result_assessment_card div[data-testid="stVerticalBlock"],
.st-key-result_assessment_card div[data-testid="element-container"],
.st-key-result_assessment_card div[data-testid="stHorizontalBlock"],
div[class*="st-key-result_assessment_card"] div[data-testid="stVerticalBlock"],
div[class*="st-key-result_assessment_card"] div[data-testid="element-container"],
div[class*="st-key-result_assessment_card"] div[data-testid="stHorizontalBlock"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
}

.st-key-result_assessment_card div[data-testid="stRadio"],
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
    margin-top: 0 !important;
    margin-bottom: 0.45rem !important;
}

.st-key-result_assessment_card div[role="radiogroup"],
div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
    gap: 0.12rem !important;
}

/* Innerer HTML-Block soll keine eigene Karte sein */
.result-assessment-inner {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 0 0.85rem 0 !important;
}

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem !important;
    font-weight: 850 !important;
    letter-spacing: -0.035em !important;
    margin: 0 0 0.75rem 0 !important;
}

.result-assessment-inner p {
    margin: 0 0 0.5rem 0 !important;
    color: var(--text) !important;
}

/* Hinweis unter Button zentrieren */
.result-assessment-hint {
    text-align: center !important;
    color: var(--muted) !important;
    margin-top: 0.8rem !important;
    font-weight: 650 !important;
}

.result-radio-label {
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.15rem !important;
    margin-bottom: -0.15rem !important;
}

.result-assessment-hint {
    text-align: center !important;
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.25rem !important;
}

/* Radio-Buttons in der Ergebnis-Einschätzung sichtbar machen */
.st-key-result_assessment_card div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    gap: 0.45rem !important;
    cursor: pointer !important;
}

/* Abschlussfragebogen: Header, Progressbar, Legende und Item-Karte */
.questionnaire-title {
    text-align: center;
    color: var(--primary);
    font-size: 2.35rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    line-height: 1.08;
    margin-top: 0.4rem;
    margin-bottom: 0.35rem;
}

.questionnaire-subtitle {
    text-align: center;
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.5;
    margin-bottom: 1.1rem;
}

.questionnaire-progress-wrap {
    width: min(420px, 100%);
    margin: 0 auto 1.25rem auto;
}

.questionnaire-progress-track {
    width: 100%;
    height: 7px;
    border-radius: 999px;
    background: rgba(49,92,99,0.10);
    overflow: hidden;
}

.questionnaire-progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

.questionnaire-section-card {
    background: #FFFFFF;
    border: 1px solid rgba(49,92,99,0.12);
    border-radius: 24px;
    padding: 1.2rem 1.35rem;
    box-shadow: 0 16px 38px rgba(49,92,99,0.09);
    margin-bottom: 1rem;
}

.questionnaire-section-label {
    color: var(--muted);
    font-size: 0.86rem;
    font-weight: 750;
    margin-bottom: 0.2rem;
}

.questionnaire-section-title {
    color: var(--primary);
    font-size: 1.35rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.85rem;
}

.scale-legend-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.65rem;
}

.scale-legend-box {
    background: #F8F4ED;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 0.7rem 0.75rem;
    text-align: center;
}

.scale-legend-box strong {
    display: block;
    color: var(--primary);
    font-size: 1.05rem;
    margin-bottom: 0.15rem;
}

.scale-legend-box span {
    display: block;
    color: var(--muted);
    font-size: 0.86rem;
    line-height: 1.35;
}

.st-key-questionnaire_item_card,
div[class*="st-key-questionnaire_item_card"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 26px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    padding: 1.1rem 1.35rem 0.45rem 1.35rem !important;
    margin-bottom: 1.1rem !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"],
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
    margin-bottom: 0.65rem !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"] > label,
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label {
    color: var(--text) !important;
    font-weight: 500 !important;
    margin-bottom: 0.35rem !important;
}

.st-key-questionnaire_item_card div[role="radiogroup"],
div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
    gap: 0.9rem !important;
}

.questionnaire-button-row {
    margin-top: 0.45rem;
}

.questionnaire-hint {
    text-align: center;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.35rem;
    margin-bottom: 0.5rem;
}

/* Feinschliff Abschlussfragebogen */
.questionnaire-section-helper {
    color: var(--text) !important;
    font-size: 1rem;
    line-height: 1.55;
    margin-top: -0.25rem;
    margin-bottom: 0.95rem;
}

.st-key-questionnaire_item_card,
div[class*="st-key-questionnaire_item_card"] {
    margin-bottom: 0.45rem !important;
}

/* Item-Texte größer und besser lesbar */
.st-key-questionnaire_item_card div[data-testid="stRadio"] > label,
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label {
    margin-bottom: 0.45rem !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
    font-size: 1.08rem !important;
    line-height: 1.5 !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}

/* Skalenwerte etwas besser lesbar */
.st-key-questionnaire_item_card div[role="radiogroup"] label,
div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
    font-size: 1rem !important;
}

.questionnaire-hint {
    margin-top: 0.3rem !important;
}

/* Footer im Abschlussfragebogen näher an die Item-Karte ziehen */
.st-key-questionnaire_footer,
div[class*="st-key-questionnaire_footer"] {
    margin-top: -0.45rem !important;
    padding-top: 0 !important;
}

.st-key-questionnaire_footer div[data-testid="stHorizontalBlock"],
div[class*="st-key-questionnaire_footer"] div[data-testid="stHorizontalBlock"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.st-key-questionnaire_footer .stButton,
div[class*="st-key-questionnaire_footer"] .stButton {
    margin-top: 0 !important;
}

.st-key-questionnaire_footer .questionnaire-hint,
div[class*="st-key-questionnaire_footer"] .questionnaire-hint {
    text-align: center !important;
    margin-top: 0.35rem !important;
}

/* Screen 2: Consent-Bereich sauber unter der Info-Karte platzieren */
.st-key-consent_action_area,
div[class*="st-key-consent_action_area"] {
    margin-top: 0.15rem !important;
    padding-top: 0 !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"],
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}

.st-key-consent_action_area .stButton,
div[class*="st-key-consent_action_area"] .stButton {
    margin-top: 0 !important;
}

/* FINAL MOBILE OPTIMIZATION */
@media (max-width: 700px) {

    html, body, .stApp {
        overflow-x: hidden !important;
    }

    .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-bottom: 1.4rem !important;
    }

    .welcome-wrap,
    .screen-frame,
    .screen-frame-soft {
        border-radius: 22px !important;
        padding: 1.15rem 0.75rem 1.4rem 0.75rem !important;
        margin-bottom: 0.8rem !important;
    }

    .welcome-card,
    .screen-card-info,
    .screen-card-main,
    .text-card,
    .result-hero-card,
    .topmatch-card,
    .thanks-card,
    .questionnaire-section-card,
    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"],
    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        border-radius: 20px !important;
        padding: 1.05rem 1rem !important;
        box-shadow: 0 12px 28px rgba(49,92,99,0.10) !important;
    }

    .hero-title,
    .questionnaire-title {
        font-size: 1.75rem !important;
        line-height: 1.12 !important;
        letter-spacing: -0.04em !important;
        text-align: center !important;
        margin-bottom: 0.55rem !important;
    }

    .hero-subtitle,
    .questionnaire-subtitle,
    .assessment-help {
        font-size: 0.95rem !important;
        line-height: 1.45 !important;
        text-align: center !important;
    }

    .screen-card-info p,
    .text-card p,
    .result-profile-text,
    .result-method-text,
    .result-next-note {
        font-size: 0.96rem !important;
        line-height: 1.55 !important;
    }

    .info-grid {
        grid-template-columns: 1fr !important;
        gap: 0.55rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.8rem !important;
    }

    .info-box,
    .instruction-box,
    .scale-legend-box {
        border-radius: 16px !important;
        padding: 0.75rem 0.85rem !important;
    }

    .instruction-row {
        flex-direction: column !important;
        gap: 0.55rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.8rem !important;
    }

    .study-progress {
        border-radius: 18px !important;
        padding: 0.7rem !important;
        margin-bottom: 0.9rem !important;
    }

    .study-progress-label {
        font-size: 0.78rem !important;
        margin-bottom: 0.45rem !important;
    }

    .study-progress-track {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
    }

    .study-progress-step {
        font-size: 0.72rem !important;
        padding: 0.42rem 0.25rem !important;
        line-height: 1.2 !important;
        white-space: normal !important;
    }

    .result-company {
        font-size: 1.65rem !important;
        line-height: 1.12 !important;
    }

    .result-score-row {
        gap: 0.55rem !important;
        align-items: center !important;
    }

    .result-score {
        font-size: 1.05rem !important;
        padding: 0.45rem 0.75rem !important;
    }

    .result-score-label {
        font-size: 0.88rem !important;
    }

    .result-meta-row {
        gap: 0.4rem !important;
    }

    .result-pill {
        font-size: 0.78rem !important;
        padding: 0.28rem 0.6rem !important;
    }

    .result-details-title {
        font-size: 1.25rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.6rem !important;
    }

    .questionnaire-progress-wrap {
        width: min(320px, 90%) !important;
        margin-bottom: 1rem !important;
    }

    .questionnaire-section-title {
        font-size: 1.15rem !important;
        margin-bottom: 0.65rem !important;
    }

    .questionnaire-section-helper {
        font-size: 0.94rem !important;
        line-height: 1.45 !important;
        margin-bottom: 0.75rem !important;
    }

    .scale-legend-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.4rem !important;
    }

    .scale-legend-box strong {
        font-size: 0.95rem !important;
    }

    .scale-legend-box span {
        font-size: 0.74rem !important;
        line-height: 1.25 !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        font-size: 1.02rem !important;
        line-height: 1.45 !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"],
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        gap: 0.45rem !important;
        flex-wrap: wrap !important;
    }

    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: -0.15rem !important;
    }

    .questionnaire-hint {
        font-size: 0.86rem !important;
        line-height: 1.35 !important;
        padding-left: 0.3rem !important;
        padding-right: 0.3rem !important;
    }

    .stButton > button {
        min-height: 46px !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.96rem !important;
    }

    .consent-spacing {
        height: 0.25rem !important;
    }

    .st-key-consent_action_area,
div[class*="st-key-consent_action_area"] {
    margin-top: 0.15rem !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"],
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
    margin-top: 0 !important;
    margin-bottom: 0.25rem !important;
}

/* Ende FINAL MOBILE OPTIMIZATION */
}

@media (max-width: 390px) {
    .hero-title,
    .questionnaire-title {
        font-size: 1.55rem !important;
    }

    .study-progress-step {
        font-size: 0.66rem !important;
        padding: 0.38rem 0.18rem !important;
    }

    .scale-legend-grid {
        gap: 0.3rem !important;
    }

    .scale-legend-box {
        padding: 0.6rem 0.45rem !important;
    }

    .scale-legend-box span {
        font-size: 0.68rem !important;
    }

    .result-company {
        font-size: 1.45rem !important;
    }
}

/* Consent-Interaktion sauber unter der Karte */
.st-key-consent_action_area,
div[class*="st-key-consent_action_area"] {
    margin-top: 0.15rem !important;
    padding-top: 0 !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"],
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}

.st-key-consent_action_area .stButton,
div[class*="st-key-consent_action_area"] .stButton {
    margin-top: 0 !important;
}

/* Screen 2: saubere Informationskarte ohne äußeren Farbverlaufsrahmen */
.consent-clean-wrap {
    width: 100% !important;
    margin: 0 auto 0.75rem auto !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

.consent-clean-wrap .screen-card-info {
    width: min(820px, 100%) !important;
    margin: 0 auto !important;
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 30px !important;
    box-shadow: 0 20px 48px rgba(49,92,99,0.11) !important;
}

/* Screen 2: Checkbox und Button sauber unter der Karte */
.st-key-consent_action_area,
div[class*="st-key-consent_action_area"] {
    margin-top: 0.25rem !important;
    padding-top: 0 !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"],
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}

.st-key-consent_action_area .stButton,
div[class*="st-key-consent_action_area"] .stButton {
    margin-top: 0 !important;
}

.consent-clean-wrap .screen-card-info {
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.05), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.08), transparent 34%),
        rgba(255,255,255,0.96) !important;
}

/* Screen vor Abschlussfragebogen: saubere Informationskarte ohne äußeren Farbverlaufsrahmen */
.pre-questionnaire-clean-wrap {
    width: 100% !important;
    margin: 0 auto 1.35rem auto !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

.pre-questionnaire-clean-wrap .screen-card-info {
    width: 100% !important;
    max-width: none !important;
    box-sizing: border-box !important;
    margin: 0 auto !important;
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 30px !important;
    box-shadow: 0 20px 48px rgba(49,92,99,0.11) !important;
}

/* =========================================================
   FINAL: Native Checkbox & Radio Styling
   Theme-Farbe nutzen, native Kreise sichtbar lassen
   ========================================================= */

/* Radio-Buttons: native Darstellung behalten, nur Akzentfarbe setzen */
div[data-testid="stRadio"] input[type="radio"],
div[role="radiogroup"] input[type="radio"] {
    appearance: auto !important;
    -webkit-appearance: radio !important;
    accent-color: var(--success) !important;
    width: 16px !important;
    height: 16px !important;
    min-width: 16px !important;
    min-height: 16px !important;
    opacity: 1 !important;
    visibility: visible !important;
    display: inline-block !important;
    margin-right: 0.45rem !important;
}

/* Ausgewählte Antwort dezent hervorheben */
div[data-testid="stRadio"] label:has(input[type="radio"]:checked) p,
div[data-testid="stRadio"] label:has(input[type="radio"]:checked) span {
    color: var(--primary) !important;
    font-weight: 700 !important;
}

/* =========================================================
   FINAL MOBILE OVERRIDE V2
   Kompaktere Darstellung für Smartphone / WhatsApp-Browser
   ========================================================= */

@media (max-width: 900px) {

    html, body, .stApp {
        overflow-x: hidden !important;
    }

    .block-container {
        max-width: 100% !important;
        padding-top: 0.85rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-bottom: calc(6.5rem + env(safe-area-inset-bottom)) !important;
    }

    /* Fortschritt kompakter */
    .study-progress {
        border-radius: 18px !important;
        padding: 0.7rem 0.75rem !important;
        margin-bottom: 0.9rem !important;
        box-shadow: 0 10px 24px rgba(49,92,99,0.07) !important;
    }

    .study-progress-label {
        font-size: 0.78rem !important;
        margin-bottom: 0.45rem !important;
    }

    .study-progress-track {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
    }

    .study-progress-step {
        font-size: 0.72rem !important;
        padding: 0.45rem 0.18rem !important;
        line-height: 1.15 !important;
        min-height: 34px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
    }

    /* Allgemeine Karten kompakter */
    .welcome-wrap,
    .screen-frame,
    .screen-frame-soft {
        border-radius: 22px !important;
        padding: 0.95rem 0.65rem 1.25rem 0.65rem !important;
        margin-bottom: 0.75rem !important;
    }

    .welcome-card,
    .screen-card-info,
    .screen-card-main,
    .text-card,
    .result-hero-card,
    .topmatch-card,
    .thanks-card,
    .questionnaire-section-card,
    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"],
    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        border-radius: 21px !important;
        padding: 1.05rem 1rem !important;
        box-shadow: 0 12px 28px rgba(49,92,99,0.09) !important;
    }

    /* Hauptüberschriften */
    .hero-title,
    .questionnaire-title {
        font-size: 1.7rem !important;
        line-height: 1.12 !important;
        letter-spacing: -0.04em !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.55rem !important;
        text-align: center !important;
    }

    .welcome-card .hero-title {
        font-size: 1.55rem !important;
        line-height: 1.12 !important;
        text-align: left !important;
    }

    .hero-subtitle,
    .questionnaire-subtitle,
    .assessment-help {
        font-size: 0.94rem !important;
        line-height: 1.45 !important;
        margin-bottom: 0.85rem !important;
    }

    .welcome-card .hero-subtitle {
        text-align: left !important;
        font-size: 0.94rem !important;
        line-height: 1.48 !important;
    }

    .screen-card-info p,
    .text-card p,
    .result-profile-text,
    .result-method-text,
    .result-next-note,
    .soft-note {
        font-size: 0.95rem !important;
        line-height: 1.48 !important;
        margin-bottom: 0.75rem !important;
    }

    /* Info-Kacheln mobil kompakter */
    .info-grid {
        grid-template-columns: 1fr !important;
        gap: 0.55rem !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }

    .info-box,
    .instruction-box,
    .scale-legend-box {
        border-radius: 16px !important;
        padding: 0.68rem 0.75rem !important;
    }

    .info-box strong,
    .instruction-box strong {
        font-size: 0.95rem !important;
        margin-bottom: 0.15rem !important;
    }

    .info-box span,
    .instruction-box span {
        font-size: 0.86rem !important;
        line-height: 1.3 !important;
    }

    .instruction-row {
        flex-direction: column !important;
        gap: 0.55rem !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }

    .text-card h3 {
        font-size: 1.35rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.65rem !important;
    }

    /* Buttons kompakter und mit Abstand zur Browserleiste */
    .stButton > button {
        min-height: 46px !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.94rem !important;
    }

    .welcome-action,
    .st-key-consent_action_area,
    div[class*="st-key-consent_action_area"],
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-bottom: 1.2rem !important;
    }

    /* Ergebnis-Screen */
    .result-company {
        font-size: 1.55rem !important;
        line-height: 1.12 !important;
        margin-bottom: 0.65rem !important;
    }

    .result-kicker {
        font-size: 0.78rem !important;
    }

    .result-score-row {
        gap: 0.55rem !important;
        margin-bottom: 0.65rem !important;
    }

    .result-score {
        font-size: 1rem !important;
        padding: 0.42rem 0.72rem !important;
    }

    .result-score-label {
        font-size: 0.84rem !important;
        line-height: 1.25 !important;
    }

    .result-pill {
        font-size: 0.76rem !important;
        padding: 0.28rem 0.58rem !important;
    }

    .result-next-note {
        border-radius: 16px !important;
        padding: 0.78rem 0.85rem !important;
    }

    .result-details-title {
        font-size: 1.18rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.55rem !important;
    }

    .result-assessment-inner h3 {
        font-size: 1.35rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.65rem !important;
    }

    .result-assessment-inner p {
        font-size: 0.95rem !important;
        line-height: 1.45 !important;
    }

    .result-radio-label,
    .result-assessment-hint {
        font-size: 0.84rem !important;
        line-height: 1.35 !important;
    }

    /* Abschlussfragebogen */
    .questionnaire-progress-wrap {
        width: min(320px, 90%) !important;
        margin-bottom: 0.9rem !important;
    }

    .questionnaire-section-card {
        margin-bottom: 0.75rem !important;
    }

    .questionnaire-section-label {
        font-size: 0.76rem !important;
    }

    .questionnaire-section-title {
        font-size: 1.12rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.6rem !important;
    }

    .questionnaire-section-helper {
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
        margin-bottom: 0.7rem !important;
    }

    .scale-legend-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
    }

    .scale-legend-box {
        padding: 0.55rem 0.35rem !important;
    }

    .scale-legend-box strong {
        font-size: 0.9rem !important;
    }

    .scale-legend-box span {
        font-size: 0.68rem !important;
        line-height: 1.2 !important;
    }

    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"] {
        padding: 0.95rem 0.9rem 0.45rem 0.9rem !important;
        margin-bottom: 0.65rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        font-size: 0.98rem !important;
        line-height: 1.42 !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"],
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        gap: 0.28rem !important;
        justify-content: space-between !important;
        flex-wrap: nowrap !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"] label,
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
        font-size: 0.9rem !important;
    }

    div[data-testid="stRadio"] input[type="radio"],
    div[role="radiogroup"] input[type="radio"] {
        width: 15px !important;
        height: 15px !important;
        min-width: 15px !important;
        min-height: 15px !important;
        margin-right: 0.28rem !important;
    }

    .questionnaire-hint {
        font-size: 0.82rem !important;
        line-height: 1.35 !important;
        margin-top: 0.35rem !important;
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }

    /* Danke-Screen */
    .thanks-wrap {
        margin-top: 2rem !important;
    }

    .thanks-card {
        padding: 1.45rem 1.05rem !important;
    }

    .thanks-icon {
        width: 46px !important;
        height: 46px !important;
        font-size: 1.45rem !important;
        margin-bottom: 0.75rem !important;
    }

    .thanks-title {
        font-size: 1.45rem !important;
        line-height: 1.15 !important;
    }

    .thanks-text {
        font-size: 0.94rem !important;
        line-height: 1.45 !important;
    }
}

@media (max-width: 430px) {
    .block-container {
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
    }

    .hero-title,
    .questionnaire-title {
        font-size: 1.55rem !important;
    }

    .welcome-card .hero-title {
        font-size: 1.45rem !important;
    }

    .hero-subtitle,
    .questionnaire-subtitle,
    .assessment-help,
    .welcome-card .hero-subtitle {
        font-size: 0.9rem !important;
    }

    .screen-card-info p,
    .text-card p,
    .result-profile-text,
    .result-method-text,
    .result-next-note,
    .soft-note {
        font-size: 0.9rem !important;
    }

    .study-progress-step {
        font-size: 0.66rem !important;
        padding: 0.38rem 0.14rem !important;
    }

    .result-company {
        font-size: 1.42rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        font-size: 0.94rem !important;
    }
}

/* =========================================================
   FINAL MOBILE POLISH V3
   Kompakter, ruhiger, einheitlicher auf Smartphone
   ========================================================= */

@media (max-width: 900px) {

    html, body, .stApp {
        overflow-x: hidden !important;
    }

    .block-container {
        max-width: 100% !important;
        padding-top: 0.85rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-bottom: calc(6.2rem + env(safe-area-inset-bottom)) !important;
    }

    /* Einheitliche Buttonbreite mobil */
    .stButton > button {
        width: min(360px, 78vw) !important;
        max-width: 360px !important;
        min-height: 44px !important;
        padding: 0.62rem 1rem !important;
        font-size: 0.95rem !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        border-radius: 999px !important;
    }

    /* Buttonbereiche näher an Karten ziehen */
    .st-key-consent_action_area,
    div[class*="st-key-consent_action_area"] {
        margin-top: -0.15rem !important;
        margin-bottom: 0.75rem !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"],
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
        margin-bottom: 0.25rem !important;
    }

    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: -0.2rem !important;
        margin-bottom: 0.9rem !important;
    }

    /* Startscreen kompakter */
    .welcome-wrap {
        padding: 1.05rem 0.75rem 1.3rem 0.75rem !important;
        border-radius: 22px !important;
        margin-bottom: 0.55rem !important;
    }

    .welcome-card {
        padding: 1.2rem 1.05rem !important;
        border-radius: 22px !important;
    }

    .welcome-card .hero-title {
        font-size: 1.55rem !important;
        line-height: 1.12 !important;
        text-align: left !important;
        margin-bottom: 0.8rem !important;
    }

    .welcome-card .hero-subtitle {
        font-size: 0.92rem !important;
        line-height: 1.42 !important;
        text-align: left !important;
        margin-bottom: 0 !important;
    }

    /* etwas weniger Luft zwischen Startscreen-Karte und Button */
    .start-button-anchor + div,
    div:has(.start-button-anchor) + div {
        margin-top: -0.25rem !important;
    }

    /* Allgemeine Karten */
    .screen-card-info,
    .screen-card-main,
    .text-card,
    .result-hero-card,
    .topmatch-card,
    .questionnaire-section-card,
    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"],
    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        border-radius: 22px !important;
        padding: 1rem 1rem !important;
        box-shadow: 0 12px 28px rgba(49,92,99,0.09) !important;
    }

    /* Überschriften allgemein */
    .hero-title,
    .questionnaire-title {
        font-size: 1.58rem !important;
        line-height: 1.12 !important;
        letter-spacing: -0.04em !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.55rem !important;
        text-align: center !important;
    }

    .hero-subtitle,
    .questionnaire-subtitle,
    .assessment-help {
        font-size: 0.92rem !important;
        line-height: 1.42 !important;
        margin-bottom: 0.8rem !important;
    }

    .screen-card-info p,
    .text-card p,
    .result-profile-text,
    .result-method-text,
    .result-next-note {
        font-size: 0.92rem !important;
        line-height: 1.45 !important;
        margin-bottom: 0.68rem !important;
    }

    /* Fortschrittsanzeige bleibt kompakt */
    .study-progress {
        border-radius: 18px !important;
        padding: 0.68rem 0.75rem !important;
        margin-bottom: 0.85rem !important;
    }

    .study-progress-label {
        font-size: 0.78rem !important;
        margin-bottom: 0.45rem !important;
    }

    .study-progress-track {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
    }

    .study-progress-step {
        font-size: 0.72rem !important;
        min-height: 34px !important;
        padding: 0.42rem 0.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.15 !important;
    }

    /* Screen 2: Info-Kacheln nebeneinander, aber kleiner */
    .consent-clean-wrap .info-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.65rem !important;
    }

    .consent-clean-wrap .info-box {
        padding: 0.52rem 0.35rem !important;
        border-radius: 14px !important;
        min-height: 64px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .consent-clean-wrap .info-box strong {
        font-size: 0.78rem !important;
        margin-bottom: 0.1rem !important;
    }

    .consent-clean-wrap .info-box span {
        font-size: 0.68rem !important;
        line-height: 1.18 !important;
    }

    /* Pre-Questionnaire: Kacheln untereinander, aber kompakter */
    .pre-questionnaire-clean-wrap .info-grid {
        grid-template-columns: 1fr !important;
        gap: 0.45rem !important;
        margin-top: 0.65rem !important;
        margin-bottom: 0.65rem !important;
    }

    .pre-questionnaire-clean-wrap .info-box {
        padding: 0.58rem 0.7rem !important;
        border-radius: 14px !important;
        min-height: 58px !important;
    }

    .pre-questionnaire-clean-wrap .info-box strong {
        font-size: 0.86rem !important;
        margin-bottom: 0.08rem !important;
    }

    .pre-questionnaire-clean-wrap .info-box span {
        font-size: 0.78rem !important;
        line-height: 1.22 !important;
    }

    /* Anleitung Swipe/Likert */
    .text-card h3 {
        font-size: 1.32rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.45rem !important;
    }

    .instruction-row {
        flex-direction: row !important;
        gap: 0.42rem !important;
        margin-top: 0.65rem !important;
        margin-bottom: 0.65rem !important;
    }

    .instruction-box {
        border-radius: 15px !important;
        padding: 0.6rem 0.4rem !important;
        min-height: 70px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .instruction-box strong {
        font-size: 0.8rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.15rem !important;
    }

    .instruction-box span {
        font-size: 0.72rem !important;
        line-height: 1.2 !important;
    }

    /* Ergebnis-Screen kompakter */
    .result-company {
        font-size: 1.5rem !important;
        line-height: 1.12 !important;
        margin-bottom: 0.6rem !important;
    }

    .result-kicker {
        font-size: 0.76rem !important;
        margin-bottom: 0.35rem !important;
    }

    .result-score-row {
        gap: 0.5rem !important;
        margin-bottom: 0.6rem !important;
    }

    .result-score {
        font-size: 1rem !important;
        padding: 0.4rem 0.72rem !important;
    }

    .result-score-label {
        font-size: 0.82rem !important;
        line-height: 1.25 !important;
    }

    /* Redundante grüne Pills auf Ergebnis-Screen mobil ausblenden */
    .result-meta-row {
        display: none !important;
    }

    .result-next-note {
        border-radius: 15px !important;
        padding: 0.72rem 0.82rem !important;
        margin-bottom: 0.85rem !important;
    }

    .result-assessment-inner h3 {
        font-size: 1.35rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.35rem !important;
    }

    .result-assessment-inner p {
        font-size: 0.95rem !important;
        line-height: 1.38 !important;
        margin-bottom: 0.4rem !important;
    }

    .st-key-result_assessment_card div[data-testid="stRadio"] label p,
    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label p {
        font-size: 0.95rem !important;
        line-height: 1.35 !important;
    }

    .result-assessment-hint {
        font-size: 0.82rem !important;
        line-height: 1.3 !important;
        margin-top: 0.55rem !important;
    }

    .result-details-title {
        font-size: 1.14rem !important;
        margin-top: 0.9rem !important;
        margin-bottom: 0.55rem !important;
    }

    /* Abschlussfragebogen */
    .questionnaire-title {
        font-size: 1.58rem !important;
        margin-bottom: 0.25rem !important;
    }

    .questionnaire-subtitle {
        margin-bottom: 0.75rem !important;
    }

    .questionnaire-progress-wrap {
        width: min(330px, 88%) !important;
        margin-bottom: 0.85rem !important;
    }

    .questionnaire-section-card {
        margin-bottom: 0.75rem !important;
    }

    .questionnaire-section-label {
        font-size: 0.76rem !important;
    }

    .questionnaire-section-title {
        font-size: 1.12rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.5rem !important;
    }

    .questionnaire-section-helper {
        font-size: 0.9rem !important;
        line-height: 1.38 !important;
        margin-bottom: 0.65rem !important;
    }

    .scale-legend-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
    }

    .scale-legend-box {
        padding: 0.52rem 0.32rem !important;
        border-radius: 14px !important;
    }

    .scale-legend-box strong {
        font-size: 0.88rem !important;
    }

    .scale-legend-box span {
        font-size: 0.66rem !important;
        line-height: 1.18 !important;
    }

    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"] {
        padding: 1.1rem 0.95rem 0.55rem 0.95rem !important;
        margin-bottom: 0.65rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"],
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
        margin-bottom: 0.78rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        font-size: 0.98rem !important;
        line-height: 1.42 !important;
        font-weight: 500 !important;
        margin-bottom: 0.4rem !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"],
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        gap: 0.25rem !important;
        justify-content: space-between !important;
        flex-wrap: nowrap !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"] label,
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
        font-size: 0.98rem !important;
        line-height: 1.2 !important;
    }

    div[data-testid="stRadio"] input[type="radio"],
    div[role="radiogroup"] input[type="radio"] {
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        min-height: 16px !important;
        margin-right: 0.28rem !important;
    }

    .questionnaire-hint {
        font-size: 0.82rem !important;
        line-height: 1.32 !important;
        margin-top: 0.35rem !important;
        margin-bottom: 0.65rem !important;
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }

    /* Zurück-Button subtiler, falls er in eigenem Container liegt */
    .st-key-back_button_soft .stButton > button,
    div[class*="st-key-back_button_soft"] .stButton > button {
        background: transparent !important;
        color: var(--primary) !important;
        border: 1px solid rgba(49,92,99,0.28) !important;
        box-shadow: none !important;
    }

    .st-key-back_button_soft .stButton > button:hover,
    div[class*="st-key-back_button_soft"] .stButton > button:hover {
        background: rgba(49,92,99,0.06) !important;
        color: var(--primary) !important;
        transform: none !important;
        box-shadow: none !important;
    }
}

@media (max-width: 430px) {

    .block-container {
        padding-left: 0.72rem !important;
        padding-right: 0.72rem !important;
    }

    .hero-title,
    .questionnaire-title {
        font-size: 1.48rem !important;
    }

    .welcome-card .hero-title {
        font-size: 1.42rem !important;
    }

    .hero-subtitle,
    .questionnaire-subtitle,
    .assessment-help,
    .welcome-card .hero-subtitle {
        font-size: 0.88rem !important;
    }

    .screen-card-info p,
    .text-card p,
    .result-profile-text,
    .result-method-text,
    .result-next-note {
        font-size: 0.88rem !important;
    }

    .study-progress-step {
        font-size: 0.66rem !important;
        padding: 0.36rem 0.14rem !important;
    }

    .instruction-box strong {
        font-size: 0.76rem !important;
    }

    .instruction-box span {
        font-size: 0.68rem !important;
    }

    .result-company {
        font-size: 1.36rem !important;
    }
}

    

/* =========================================================
   FINAL MOBILE POLISH V4
   Einheitliches Spacing, schmalere Buttons, klarere Cards
   ========================================================= */

/* Einheitliche Button-Logik: Primary CTA schmaler und ruhiger */
@media (max-width: 900px) {
    .stButton > button {
        width: min(300px, 70vw) !important;
        max-width: 300px !important;
        min-height: 43px !important;
        padding: 0.58rem 0.95rem !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.01em !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
        box-shadow: 0 8px 20px rgba(49,92,99,0.13) !important;
    }

    /* Grundlayout etwas luftiger oben, aber kompakt zwischen Elementen */
    .block-container {
        padding-top: 0.85rem !important;
        padding-left: 0.72rem !important;
        padding-right: 0.72rem !important;
        padding-bottom: calc(5.8rem + env(safe-area-inset-bottom)) !important;
    }

    /* 1. Startscreen: zentriert, Button näher an die Karte */
    .welcome-wrap {
        margin-bottom: 0.15rem !important;
        padding: 1.05rem 0.7rem 1.15rem 0.7rem !important;
    }

    .welcome-card {
        text-align: center !important;
        padding: 1.25rem 1.05rem !important;
    }

    .welcome-card .hero-title {
        text-align: center !important;
        margin-bottom: 0.9rem !important;
    }

    .welcome-card .hero-subtitle {
        text-align: center !important;
        line-height: 1.42 !important;
    }

    .start-button-anchor {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .start-button-anchor + div,
    div:has(.start-button-anchor) + div {
        margin-top: -0.55rem !important;
    }

    /* 2. Consent: Meta-Elemente zentriert, Fließtext lesbar, CTA näher */
    .consent-clean-wrap {
        margin-bottom: 0.25rem !important;
    }

    .consent-clean-wrap .screen-card-info {
        padding: 1.1rem 1rem !important;
    }

    .consent-clean-wrap .hero-title,
    .consent-clean-wrap .hero-subtitle {
        text-align: center !important;
    }

    .consent-clean-wrap .info-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
        margin-top: 0.55rem !important;
        margin-bottom: 0.65rem !important;
    }

    .consent-clean-wrap .info-box {
        min-height: 58px !important;
        padding: 0.46rem 0.25rem !important;
        border-radius: 14px !important;
    }

    .consent-clean-wrap .info-box strong {
        font-size: 0.76rem !important;
        line-height: 1.15 !important;
    }

    .consent-clean-wrap .info-box span {
        font-size: 0.64rem !important;
        line-height: 1.15 !important;
        overflow-wrap: anywhere !important;
    }

    .st-key-consent_action_area,
    div[class*="st-key-consent_action_area"] {
        margin-top: -0.45rem !important;
        margin-bottom: 0.55rem !important;
        text-align: center !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"],
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
        width: fit-content !important;
        max-width: 100% !important;
        margin: 0 auto 0.2rem auto !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label {
        justify-content: center !important;
        font-size: 0.9rem !important;
        line-height: 1.3 !important;
    }

    /* 3/4. Anleitungen: zentrierter, kompakter, etwas mehr Luft nach Progress */
    .study-progress {
        margin-bottom: 1.05rem !important;
    }

    .text-card {
        text-align: center !important;
        padding: 1.05rem 1rem !important;
        margin-bottom: 0.75rem !important;
    }

    .text-card h3 {
        text-align: center !important;
        margin-bottom: 0.35rem !important;
    }

    .text-card p {
        text-align: center !important;
        margin-bottom: 0.55rem !important;
    }

    .instruction-row {
        flex-direction: row !important;
        gap: 0.45rem !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.6rem !important;
    }

    .instruction-box {
        min-height: 58px !important;
        padding: 0.48rem 0.35rem !important;
        border-radius: 14px !important;
    }

    .instruction-box strong {
        font-size: 0.75rem !important;
        line-height: 1.15 !important;
    }

    .instruction-box span {
        font-size: 0.68rem !important;
        line-height: 1.16 !important;
    }

    /* 7. Ergebnis-Screen: Hinweisbox symmetrischer, Einschätzung zentriert */
    .result-next-note {
        margin: 0.9rem auto 0.8rem auto !important;
        padding: 0.78rem 0.9rem !important;
        text-align: center !important;
        border-radius: 16px !important;
    }

    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        text-align: center !important;
        padding: 1.15rem 1rem 1rem 1rem !important;
        margin-top: 0.65rem !important;
        margin-bottom: 1.05rem !important;
    }

    .result-assessment-inner {
        margin-bottom: 0.55rem !important;
        text-align: center !important;
    }

    .result-assessment-inner h3 {
        text-align: center !important;
        margin-bottom: 0.35rem !important;
    }

    .result-assessment-inner p {
        text-align: center !important;
        margin-bottom: 0.35rem !important;
    }

    .st-key-result_assessment_card div[role="radiogroup"],
    div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
        width: fit-content !important;
        margin-left: auto !important;
        margin-right: auto !important;
        gap: 0.08rem !important;
    }

    .st-key-result_assessment_card div[data-testid="stRadio"] label p,
    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label p {
        font-size: 0.95rem !important;
        line-height: 1.28 !important;
    }

    /* 8. Pre-Questionnaire: zentriert, Kacheln nebeneinander */
    .pre-questionnaire-clean-wrap {
        margin-bottom: 0.55rem !important;
    }

    .pre-questionnaire-clean-wrap .screen-card-info {
        text-align: center !important;
        padding: 1.1rem 1rem !important;
    }

    .pre-questionnaire-clean-wrap .screen-card-info p {
        text-align: center !important;
    }

    .pre-questionnaire-clean-wrap .info-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
        margin-top: 0.55rem !important;
        margin-bottom: 0.6rem !important;
    }

    .pre-questionnaire-clean-wrap .info-box {
        min-height: 58px !important;
        padding: 0.45rem 0.25rem !important;
        border-radius: 14px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .pre-questionnaire-clean-wrap .info-box strong {
        font-size: 0.75rem !important;
        line-height: 1.15 !important;
    }

    .pre-questionnaire-clean-wrap .info-box span {
        font-size: 0.63rem !important;
        line-height: 1.14 !important;
        overflow-wrap: anywhere !important;
    }

    /* 9. Abschlussfragebogen: Header zentriert, Items bewusst linksbündig */
    .questionnaire-section-card {
        text-align: center !important;
        padding: 1.0rem 1rem !important;
        margin-bottom: 0.7rem !important;
    }

    .questionnaire-section-helper {
        text-align: center !important;
    }

    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"] {
        text-align: left !important;
        padding: 1.15rem 1rem 0.55rem 1rem !important;
        margin-bottom: 0.7rem !important;
        border-radius: 22px !important;
        box-shadow: 0 14px 30px rgba(49,92,99,0.08) !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"],
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
        padding: 0 0 0.95rem 0 !important;
        margin-bottom: 0.85rem !important;
        border-bottom: 1px solid rgba(49,92,99,0.08) !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"]:last-of-type,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"]:last-of-type {
        border-bottom: none !important;
        margin-bottom: 0.2rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        font-size: 1.02rem !important;
        line-height: 1.42 !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
        color: var(--text) !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"],
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        justify-content: space-between !important;
        gap: 0.18rem !important;
        flex-wrap: nowrap !important;
        padding-right: 0.1rem !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"] label,
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
        font-size: 0.96rem !important;
        line-height: 1.15 !important;
    }

    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: -0.1rem !important;
        margin-bottom: 0.75rem !important;
    }

    /* Secondary Back Button: sichtbar, grün, outlined */
    .st-key-back_button_soft .stButton > button,
    div[class*="st-key-back_button_soft"] .stButton > button {
        background: rgba(255,255,255,0.35) !important;
        border: 2px solid rgba(49,92,99,0.48) !important;
        color: var(--primary) !important;
        box-shadow: none !important;
    }

    .st-key-back_button_soft .stButton > button *,
    div[class*="st-key-back_button_soft"] .stButton > button * {
        color: var(--primary) !important;
    }

    .st-key-back_button_soft .stButton > button:hover,
    div[class*="st-key-back_button_soft"] .stButton > button:hover {
        background: rgba(49,92,99,0.07) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
        transform: none !important;
        box-shadow: none !important;
    }
}

@media (max-width: 430px) {
    .stButton > button {
        width: min(285px, 72vw) !important;
        max-width: 285px !important;
    }

    .welcome-card .hero-title {
        font-size: 1.36rem !important;
    }

    .welcome-card .hero-subtitle {
        font-size: 0.86rem !important;
        line-height: 1.4 !important;
    }

    .consent-clean-wrap .info-box span,
    .pre-questionnaire-clean-wrap .info-box span {
        font-size: 0.6rem !important;
    }

    .instruction-box strong {
        font-size: 0.7rem !important;
    }

    .instruction-box span {
        font-size: 0.64rem !important;
    }
}

/* =========================================================
   FINAL MOBILE POLISH
   Buttons, Abstände, Kacheln, Ergebnisbox, Fragebogen
   ========================================================= */

@media (max-width: 700px) {

    /* Grundlayout mobil etwas ruhiger */
    .block-container {
        padding-top: 1.25rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-bottom: 2.2rem !important;
    }

    /* Einheitliche Buttonbreite auf Mobile */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        margin-top: 0.35rem !important;
        margin-bottom: 0.35rem !important;
    }

    .stButton > button {
        width: min(76vw, 310px) !important;
        max-width: 310px !important;
        min-height: 52px !important;
        padding: 0.62rem 1.1rem !important;
        font-size: 1.02rem !important;
        border-radius: 999px !important;
    }

    /* Startscreen: Button näher an Karte */
    .start-button-anchor {
        height: 0.15rem !important;
        margin: 0 !important;
    }

    .welcome-wrap {
        padding-bottom: 1.45rem !important;
        margin-bottom: 0.15rem !important;
    }

    .welcome-card {
        padding: 1.55rem 1.25rem !important;
    }

    .welcome-card .hero-title {
        margin-bottom: 0.85rem !important;
    }

    .welcome-card .hero-subtitle {
        line-height: 1.58 !important;
    }

    /* Einwilligung: kompakter und näher an Checkbox/Button */
    .consent-spacing {
        height: 0.25rem !important;
    }

    .consent-clean-wrap,
    .pre-questionnaire-clean-wrap,
    .screen-frame-soft {
        margin-bottom: 0.45rem !important;
    }

    .screen-card-info {
        padding: 1.35rem 1.2rem !important;
        border-radius: 24px !important;
        line-height: 1.55 !important;
        text-align: center !important;
    }

    .screen-card-info p {
        margin-bottom: 0.8rem !important;
    }

    .screen-card-info .hero-title,
    .screen-card-info .hero-subtitle {
        text-align: center !important;
    }

    /* Info-Kacheln mobil nebeneinander, aber kompakter */
    .info-grid {
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.45rem !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }

    .info-box {
        min-height: auto !important;
        padding: 0.62rem 0.35rem !important;
        border-radius: 15px !important;
    }

    .info-box strong {
        font-size: 0.9rem !important;
        margin-bottom: 0.12rem !important;
        line-height: 1.15 !important;
    }

    .info-box span {
        font-size: 0.76rem !important;
        line-height: 1.22 !important;
        word-break: normal !important;
        hyphens: none !important;
    }

    /* Anleitung: kompaktere Boxen und Button näher heran */
    .text-card {
        padding: 1.35rem 1.2rem !important;
        border-radius: 24px !important;
        text-align: center !important;
        margin-bottom: 0.6rem !important;
    }

    .text-card h3 {
        margin-bottom: 0.5rem !important;
    }

    .instruction-row {
        flex-direction: row !important;
        gap: 0.55rem !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
    }

    .instruction-box {
        padding: 0.72rem 0.35rem !important;
        border-radius: 15px !important;
    }

    .instruction-box strong {
        font-size: 0.86rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.18rem !important;
    }

    .instruction-box span {
        font-size: 0.78rem !important;
        line-height: 1.2 !important;
    }

    /* Ergebnis-Screen: Hinweisbox gleichmäßiger */
    .result-next-note,
    .soft-note {
        padding: 0.85rem 0.9rem !important;
        margin-top: 0.65rem !important;
        margin-bottom: 0.85rem !important;
        border-radius: 16px !important;
        line-height: 1.5 !important;
        text-align: center !important;
    }

    /* Ergebnis-Einschätzung: kompakter, zentrierter */
    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        padding: 1.3rem 1.15rem 1.15rem 1.15rem !important;
        margin-top: 0.75rem !important;
        margin-bottom: 1.2rem !important;
        text-align: center !important;
    }

    .result-assessment-inner {
        text-align: center !important;
        margin-bottom: 0.45rem !important;
    }

    .result-assessment-inner h3 {
        font-size: 1.45rem !important;
        margin-bottom: 0.45rem !important;
    }

    .result-assessment-inner p {
        margin-bottom: 0.45rem !important;
    }

    .st-key-result_assessment_card div[data-testid="stRadio"] label,
    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label {
        font-size: 1rem !important;
        justify-content: flex-start !important;
    }

    .result-assessment-hint {
        margin-top: 0.55rem !important;
        margin-bottom: 0 !important;
        font-size: 0.9rem !important;
        line-height: 1.35 !important;
    }

    /* Pre-Questionnaire: Kacheln nebeneinander und kompakter */
    .pre-questionnaire-clean-wrap .info-grid,
    .screen-frame-soft .info-grid {
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.45rem !important;
    }

    .pre-questionnaire-clean-wrap .info-box,
    .screen-frame-soft .info-box {
        padding: 0.58rem 0.3rem !important;
    }

    /* Abschlussfragebogen: Box cleaner */
    .questionnaire-section-card {
        padding: 1.25rem 1.05rem !important;
        border-radius: 24px !important;
        text-align: center !important;
        margin-bottom: 0.8rem !important;
    }

    .questionnaire-section-title {
        font-size: 1.35rem !important;
        margin-bottom: 0.45rem !important;
    }

    .questionnaire-section-helper {
        font-size: 0.98rem !important;
        line-height: 1.45 !important;
        margin-bottom: 0.75rem !important;
    }

    .scale-legend-grid {
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.45rem !important;
    }

    .scale-legend-box {
        padding: 0.55rem 0.25rem !important;
        border-radius: 14px !important;
    }

    .scale-legend-box strong {
        font-size: 0.95rem !important;
    }

    .scale-legend-box span {
        font-size: 0.74rem !important;
        line-height: 1.15 !important;
    }

    /* Fragebogen-Items: linksbündig lassen, aber luftiger/cleaner */
    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"] {
        padding: 1.25rem 1.05rem 1.1rem 1.05rem !important;
        border-radius: 24px !important;
        margin-bottom: 0.85rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"],
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
        margin-bottom: 1.3rem !important;
    }

    .st-key-questionnaire_item_card div[data-testid="stRadio"] > label,
    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label {
        font-size: 1.02rem !important;
        line-height: 1.45 !important;
        font-weight: 600 !important;
        margin-bottom: 0.65rem !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"],
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        justify-content: space-between !important;
        gap: 0.25rem !important;
    }

    .st-key-questionnaire_item_card div[role="radiogroup"] label,
    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
        font-size: 1.02rem !important;
        line-height: 1.2 !important;
    }

    /* Fragebogen-Footer: Buttons näher an die Karte */
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: 0.35rem !important;
    }

    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] .stButton {
        margin-top: 0.25rem !important;
        margin-bottom: 0.65rem !important;
    }

    /* Zurück-Button subtil, aber sichtbar */
    .st-key-back_button_soft button,
    div[class*="st-key-back_button_soft"] button {
        background: transparent !important;
        color: var(--primary) !important;
        border: 2px solid rgba(49,92,99,0.45) !important;
        box-shadow: none !important;
    }

    .st-key-back_button_soft button *,
    div[class*="st-key-back_button_soft"] button * {
        color: var(--primary) !important;
    }

    .st-key-back_button_soft button:hover,
    div[class*="st-key-back_button_soft"] button:hover {
        background: rgba(49,92,99,0.06) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
        box-shadow: none !important;
    }

    .questionnaire-hint {
        margin-top: 0.45rem !important;
        font-size: 0.92rem !important;
        line-height: 1.4 !important;
    }
}

/* =========================================================
   FINAL MOBILE MICRO POLISH
   Abstände, Kacheln, Buttons, Fragebogen, Ergebnisbox
   ========================================================= */

@media (max-width: 700px) {

    /* 1. Genereller Abstand oben minimal reduzieren */
    .block-container {
        padding-top: 0.75rem !important;
    }

    /* Einheitliche, etwas schmalere Buttons */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.25rem !important;
    }

    .stButton > button {
        width: min(70vw, 285px) !important;
        max-width: 285px !important;
        min-height: 50px !important;
        padding: 0.58rem 1rem !important;
        font-size: 1rem !important;
        border-radius: 999px !important;
    }

    /* 1. Startscreen: Abstand Box -> Button reduzieren */
    .welcome-wrap {
        margin-bottom: 0 !important;
        padding-bottom: 0.7rem !important;
    }

    .start-button-anchor {
        height: 0 !important;
        margin: 0 !important;
    }

    /* Startscreen bewusst NICHT komplett zentrieren:
       Der längere Text bleibt linksbündig besser lesbar. */
    .welcome-card .hero-title {
        margin-bottom: 1rem !important;
    }

    .welcome-card .hero-subtitle {
        margin-top: 0.15rem !important;
    }

    .welcome-card p {
        margin-bottom: 0.9rem !important;
    }

    /* 2 / 3 / 4 / 8: Info- und Anleitungskacheln wieder etwas größer */
    .info-grid {
        gap: 0.55rem !important;
        margin-top: 0.85rem !important;
        margin-bottom: 0.85rem !important;
    }

    .info-box {
        padding: 0.78rem 0.42rem !important;
        min-height: 74px !important;
        border-radius: 16px !important;
    }

    .info-box strong {
        font-size: 0.98rem !important;
        line-height: 1.16 !important;
        margin-bottom: 0.18rem !important;
    }

    .info-box span {
        font-size: 0.82rem !important;
        line-height: 1.22 !important;
    }

    /* 2. Einwilligung: Checkbox-Text kleiner und besser ausgerichtet */
    div[data-testid="stCheckbox"] {
        display: flex !important;
        justify-content: center !important;
        margin-top: 0.25rem !important;
        margin-bottom: 0.15rem !important;
    }

    div[data-testid="stCheckbox"] label {
        font-size: 0.98rem !important;
        line-height: 1.3 !important;
        color: #2B2B2B !important;
        max-width: 88vw !important;
        text-align: left !important;
    }

    div[data-testid="stCheckbox"] label p {
        font-size: 0.98rem !important;
        line-height: 1.3 !important;
    }

    .consent-spacing {
        height: 0 !important;
        margin: 0 !important;
    }

    /* 3 / 4. Anleitung: Header-Abstände etwas großzügiger */
    .progress-card {
        margin-bottom: 1.05rem !important;
    }

    .page-title,
    .screen-title,
    h1 {
        margin-top: 0.8rem !important;
        margin-bottom: 0.7rem !important;
    }

    .text-card {
        margin-top: 0.65rem !important;
        margin-bottom: 0.45rem !important;
        padding: 1.45rem 1.25rem !important;
    }

    .text-card h3 {
        margin-bottom: 0.45rem !important;
    }

    .instruction-row {
        gap: 0.65rem !important;
        margin-top: 0.85rem !important;
        margin-bottom: 0.85rem !important;
    }

    .instruction-box {
        padding: 0.82rem 0.45rem !important;
        min-height: 74px !important;
        border-radius: 16px !important;
    }

    .instruction-box strong {
        font-size: 0.94rem !important;
        line-height: 1.18 !important;
    }

    .instruction-box span {
        font-size: 0.84rem !important;
        line-height: 1.2 !important;
    }

    /* Anleitung: Button näher an Box */
    .text-card + div .stButton,
    .text-card ~ div .stButton {
        margin-top: 0.1rem !important;
    }

    /* 5. Matcher Likert: Ziffern leicht kleiner */
    .likert-options,
    .likert-scale,
    .likert-number,
    .option-number {
        font-size: 0.92em !important;
    }

    /* 7. Ergebnis-Screen: Hinweisbox gleichmäßig einbetten */
    .result-next-note,
    .soft-note {
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
        padding: 0.8rem 0.9rem !important;
        text-align: center !important;
    }

    /* 7. Box "Deine erste Einschätzung": komplett linksbündig und ruhiger */
    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        text-align: left !important;
        padding: 1.45rem 1.25rem 1.1rem 1.25rem !important;
        margin-top: 0.85rem !important;
        margin-bottom: 1.05rem !important;
    }

    .result-assessment-inner {
        text-align: left !important;
        margin-bottom: 0.35rem !important;
    }

    .result-assessment-inner h3 {
        text-align: left !important;
        font-size: 1.42rem !important;
        margin-bottom: 0.65rem !important;
        line-height: 1.18 !important;
    }

    .result-assessment-inner p {
        text-align: left !important;
        margin-top: 0 !important;
        margin-bottom: 0.55rem !important;
        line-height: 1.42 !important;
    }

    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
        margin-top: 0.15rem !important;
        margin-bottom: 0.7rem !important;
    }

    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label {
        justify-content: flex-start !important;
        text-align: left !important;
        font-size: 1rem !important;
        line-height: 1.3 !important;
    }

    div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
        align-items: flex-start !important;
        justify-content: flex-start !important;
    }

    .result-assessment-hint {
        margin-top: 0.25rem !important;
        padding-top: 0 !important;
        font-size: 0.9rem !important;
        line-height: 1.35 !important;
        text-align: center !important;
    }

    /* 8. Pre-Questionnaire: Kacheln etwas größer, Abstände ruhiger */
    .pre-questionnaire-clean-wrap .info-grid,
    .screen-frame-soft .info-grid {
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.55rem !important;
        margin-top: 0.9rem !important;
        margin-bottom: 0.9rem !important;
    }

    .pre-questionnaire-clean-wrap .info-box,
    .screen-frame-soft .info-box {
        min-height: 76px !important;
        padding: 0.75rem 0.4rem !important;
    }

    /* 9. Abschlussfragebogen: Abschnittsbox sauber zentrieren */
    .questionnaire-section-card {
        text-align: center !important;
        padding: 1.35rem 1.15rem !important;
        margin-bottom: 0.7rem !important;
    }

    .questionnaire-section-card * {
        text-align: center !important;
    }

    .questionnaire-section-title {
        margin-bottom: 0.5rem !important;
    }

    .questionnaire-section-helper {
        margin-bottom: 0.8rem !important;
    }

    .scale-legend-grid {
        gap: 0.55rem !important;
    }

    .scale-legend-box {
        padding: 0.68rem 0.35rem !important;
        min-height: 68px !important;
    }

    .scale-legend-box strong {
        font-size: 0.96rem !important;
    }

    .scale-legend-box span {
        font-size: 0.78rem !important;
        line-height: 1.18 !important;
    }

    /* 9. Abschlussfragebogen: Itembox clean und responsiv zentriert */
    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"] {
        padding: 1.35rem 1.05rem 1.15rem 1.05rem !important;
        margin-bottom: 0.75rem !important;
        border-radius: 24px !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
        margin-bottom: 1.05rem !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label {
        text-align: center !important;
        justify-content: center !important;
        font-size: 1.04rem !important;
        line-height: 1.42 !important;
        font-weight: 600 !important;
        margin-bottom: 0.75rem !important;
        width: 100% !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        text-align: center !important;
        width: 100% !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 92% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        gap: 0 !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
        font-size: 1.02rem !important;
        line-height: 1.2 !important;
        min-width: auto !important;
    }

    /* 9. Weiter-/Zurück-Buttons näher an die Box */
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: 0.1rem !important;
    }

    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] .stButton {
        margin-top: 0.15rem !important;
        margin-bottom: 0.45rem !important;
    }

    .st-key-questionnaire_footer + div,
    div[class*="st-key-questionnaire_footer"] + div {
        margin-top: 0.25rem !important;
    }

    /* Zurück-Button: sichtbar, aber weiterhin sekundär */
    .st-key-back_button_soft button,
    div[class*="st-key-back_button_soft"] button {
        background: transparent !important;
        color: #315C63 !important;
        border: 2px solid rgba(49, 92, 99, 0.55) !important;
        box-shadow: none !important;
    }

    .st-key-back_button_soft button *,
    div[class*="st-key-back_button_soft"] button * {
        color: #315C63 !important;
    }

    .st-key-back_button_soft button:hover,
    div[class*="st-key-back_button_soft"] button:hover {
        background: rgba(49, 92, 99, 0.06) !important;
        border-color: #315C63 !important;
        color: #315C63 !important;
    }

    .questionnaire-hint {
        margin-top: 0.35rem !important;
        padding-top: 0 !important;
        font-size: 0.9rem !important;
        line-height: 1.35 !important;
    }
}

/* =========================================================
   FINAL MOBILE MICRO POLISH V2
   Letzter Override für mobile Feinausrichtung
   ========================================================= */

@media (max-width: 700px) {

    /* 1. Startscreen: oben minimal weniger Abstand, Button näher an Karte */
    .block-container {
        padding-top: 0.55rem !important;
    }

    .welcome-wrap {
        padding-top: 0.8rem !important;
        padding-bottom: 0.45rem !important;
        margin-bottom: -0.15rem !important;
    }

    .welcome-card {
        padding: 1.45rem 1.2rem !important;
    }

    .start-button-anchor {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div:has(.start-button-anchor) + div {
        margin-top: -0.75rem !important;
    }

    /* Einheitliche Buttongröße: etwas schmaler, aber weiterhin gut klickbar */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        margin-top: 0.1rem !important;
        margin-bottom: 0.25rem !important;
    }

    .stButton > button {
        width: min(68vw, 280px) !important;
        max-width: 280px !important;
        min-height: 48px !important;
        padding: 0.55rem 0.95rem !important;
        font-size: 0.98rem !important;
        border-radius: 999px !important;
    }

    /* 2 / 8. Info-Kacheln etwas größer und hochwertiger */
    .consent-clean-wrap .info-grid,
    .pre-questionnaire-clean-wrap .info-grid,
    .screen-frame-soft .info-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.5rem !important;
        margin-top: 0.85rem !important;
        margin-bottom: 0.85rem !important;
    }

    .consent-clean-wrap .info-box,
    .pre-questionnaire-clean-wrap .info-box,
    .screen-frame-soft .info-box {
        min-height: 78px !important;
        padding: 0.72rem 0.34rem !important;
        border-radius: 16px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }

    .consent-clean-wrap .info-box strong,
    .pre-questionnaire-clean-wrap .info-box strong,
    .screen-frame-soft .info-box strong {
        font-size: 0.92rem !important;
        line-height: 1.15 !important;
        margin-bottom: 0.16rem !important;
    }

    .consent-clean-wrap .info-box span,
    .pre-questionnaire-clean-wrap .info-box span,
    .screen-frame-soft .info-box span {
        font-size: 0.74rem !important;
        line-height: 1.18 !important;
        overflow-wrap: normal !important;
        word-break: normal !important;
        hyphens: none !important;
    }

    /* 2. Einwilligung: Checkbox-Text kleiner und sauberer zentriert */
    .st-key-consent_action_area,
    div[class*="st-key-consent_action_area"] {
        margin-top: -0.25rem !important;
        margin-bottom: 0.55rem !important;
        text-align: center !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"],
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
        width: fit-content !important;
        max-width: 92vw !important;
        margin: 0 auto 0.2rem auto !important;
        display: flex !important;
        justify-content: center !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label {
        font-size: 0.9rem !important;
        line-height: 1.28 !important;
        text-align: left !important;
        align-items: center !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label p {
        font-size: 0.9rem !important;
        line-height: 1.28 !important;
    }

    /* 3 / 4. Anleitung: Header mehr Luft, Kacheln größer, Button näher */
    .study-progress {
        margin-bottom: 1.15rem !important;
    }

    .hero-title[style*="So funktioniert die Bewertung"],
    div.hero-title {
        margin-top: 0.95rem !important;
        margin-bottom: 0.95rem !important;
    }

    .text-card {
        margin-top: 0.75rem !important;
        margin-bottom: 0.25rem !important;
        padding: 1.45rem 1.2rem !important;
    }

    .instruction-row {
        gap: 0.62rem !important;
        margin-top: 0.9rem !important;
        margin-bottom: 0.9rem !important;
    }

    .instruction-box {
        min-height: 80px !important;
        padding: 0.82rem 0.42rem !important;
        border-radius: 16px !important;
    }

    .instruction-box strong {
        font-size: 0.92rem !important;
        line-height: 1.16 !important;
        margin-bottom: 0.2rem !important;
    }

    .instruction-box span {
        font-size: 0.8rem !important;
        line-height: 1.18 !important;
    }

    .text-card + div .stButton,
    .text-card ~ div .stButton {
        margin-top: -0.1rem !important;
    }

    /* 7. Ergebnis: Box "Deine erste Einschätzung" komplett linksbündig und proportional sauber */
    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        text-align: left !important;
        padding: 1.35rem 1.2rem 1.05rem 1.2rem !important;
        margin-top: 0.75rem !important;
        margin-bottom: 1.05rem !important;
    }

    .result-assessment-inner {
        text-align: left !important;
        margin: 0 0 0.45rem 0 !important;
    }

    .result-assessment-inner h3 {
        text-align: left !important;
        font-size: 1.4rem !important;
        line-height: 1.15 !important;
        margin: 0 0 0.55rem 0 !important;
    }

    .result-assessment-inner p {
        text-align: left !important;
        font-size: 0.98rem !important;
        line-height: 1.38 !important;
        margin: 0 0 0.55rem 0 !important;
    }

    .result-radio-question {
        text-align: left !important;
        font-size: 0.98rem !important;
        line-height: 1.35 !important;
        margin: 0 0 0.3rem 0 !important;
        color: var(--text) !important;
    }

    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
        margin-top: 0 !important;
        margin-bottom: 0.55rem !important;
    }

    div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
        width: 100% !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        gap: 0.12rem !important;
    }

    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label {
        justify-content: flex-start !important;
        text-align: left !important;
        font-size: 0.98rem !important;
        line-height: 1.25 !important;
        min-height: 28px !important;
    }

    .result-assessment-hint {
        margin-top: 0.15rem !important;
        padding-top: 0 !important;
        font-size: 0.88rem !important;
        line-height: 1.28 !important;
        text-align: center !important;
    }

    /* 9. Abschlussfragebogen: Itembox harmonischer, Aussagen + Skala mittig */
    .st-key-questionnaire_item_card,
    div[class*="st-key-questionnaire_item_card"] {
        padding: 1.3rem 1.05rem 1rem 1.05rem !important;
        margin-bottom: 0.65rem !important;
        border-radius: 24px !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
        margin-bottom: 1.0rem !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 1px solid rgba(49,92,99,0.07) !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"]:last-of-type {
        margin-bottom: 0.15rem !important;
        padding-bottom: 0 !important;
        border-bottom: none !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
        margin-bottom: 0.72rem !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        width: 100% !important;
        max-width: 94% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        font-size: 1.02rem !important;
        line-height: 1.42 !important;
        font-weight: 560 !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        width: 100% !important;
        max-width: 92% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        align-items: center !important;
        justify-items: center !important;
        gap: 0 !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
        width: 100% !important;
        justify-content: center !important;
        font-size: 0.98rem !important;
        line-height: 1.15 !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label p {
        font-size: 0.98rem !important;
        line-height: 1.15 !important;
    }

    div[data-testid="stRadio"] input[type="radio"],
    div[role="radiogroup"] input[type="radio"] {
        width: 15px !important;
        height: 15px !important;
        min-width: 15px !important;
        min-height: 15px !important;
        margin-right: 0.25rem !important;
    }

    /* 9. Fragebogen-Footer: Buttons näher und logischer gestapelt */
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: -0.05rem !important;
        padding-top: 0 !important;
    }

    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] .stButton {
        margin-top: 0.1rem !important;
        margin-bottom: 0.45rem !important;
    }

    .st-key-back_button_soft,
    div[class*="st-key-back_button_soft"] {
        margin-top: -0.1rem !important;
    }

    .st-key-back_button_soft .stButton,
    div[class*="st-key-back_button_soft"] .stButton {
        margin-top: 0 !important;
    }

    .st-key-back_button_soft button,
    div[class*="st-key-back_button_soft"] button {
        min-height: 46px !important;
        background: transparent !important;
        color: #315C63 !important;
        border: 2px solid rgba(49, 92, 99, 0.55) !important;
        box-shadow: none !important;
    }

    .st-key-back_button_soft button *,
    div[class*="st-key-back_button_soft"] button * {
        color: #315C63 !important;
    }

    .questionnaire-hint {
        margin-top: 0.25rem !important;
        font-size: 0.88rem !important;
        line-height: 1.3 !important;
    }
}

@media (max-width: 430px) {

    .stButton > button {
        width: min(70vw, 275px) !important;
        max-width: 275px !important;
    }

    .consent-clean-wrap .info-box,
    .pre-questionnaire-clean-wrap .info-box,
    .screen-frame-soft .info-box {
        min-height: 74px !important;
        padding-left: 0.28rem !important;
        padding-right: 0.28rem !important;
    }

    .consent-clean-wrap .info-box strong,
    .pre-questionnaire-clean-wrap .info-box strong,
    .screen-frame-soft .info-box strong {
        font-size: 0.86rem !important;
    }

    .consent-clean-wrap .info-box span,
    .pre-questionnaire-clean-wrap .info-box span,
    .screen-frame-soft .info-box span {
        font-size: 0.68rem !important;
    }

    .instruction-box strong {
        font-size: 0.84rem !important;
    }

    .instruction-box span {
        font-size: 0.74rem !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
        font-size: 0.98rem !important;
    }

    div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
        max-width: 94% !important;
    }
}

/* === FINAL CLEANUP: Consent / Result / Questionnaire === */

/* 1) Screen "Kurz zur Studie" – cleaner Aktionsbereich */
.st-key-consent_action_area,
div[class*="st-key-consent_action_area"] {
    max-width: 620px !important;
    margin: 0.25rem auto 0 auto !important;
    padding: 0.85rem 0.95rem 0.35rem 0.95rem !important;
    background: rgba(255,255,255,0.72) !important;
    border: 1px solid rgba(49,92,99,0.10) !important;
    border-radius: 24px !important;
    box-shadow: 0 12px 30px rgba(49,92,99,0.08) !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"],
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
    display: flex !important;
    justify-content: center !important;
    margin: 0 0 0.45rem 0 !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"] label,
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label {
    width: auto !important;
    margin: 0 auto !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.6rem !important;
    font-size: 0.96rem !important;
    line-height: 1.35 !important;
    text-align: left !important;
}

.st-key-consent_action_area .stButton,
div[class*="st-key-consent_action_area"] .stButton {
    max-width: 520px !important;
    margin: 0 auto !important;
}

/* 2) Ergebnisscreen – Einschätzungsbox sauberer */
.st-key-result_assessment_card,
div[class*="st-key-result_assessment_card"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 28px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    padding: 1.35rem 1.45rem 1rem 1.45rem !important;
    margin-top: 0.3rem !important;
    margin-bottom: 1rem !important;
}

.result-assessment-inner,
.result-assessment-inner * {
    text-align: left !important;
}

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem !important;
    font-weight: 850 !important;
    letter-spacing: -0.03em !important;
    margin-top: 0 !important;
    margin-bottom: 0.6rem !important;
}

.result-assessment-inner p {
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
    color: var(--text) !important;
    line-height: 1.45 !important;
}

.result-radio-label {
    text-align: left !important;
    color: var(--text) !important;
    font-size: 1rem !important;
    margin-top: 0.05rem !important;
    margin-bottom: 0.25rem !important;
}

.st-key-result_assessment_card div[data-testid="stRadio"],
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
    margin-top: 0 !important;
    margin-bottom: 0.15rem !important;
}

.st-key-result_assessment_card div[role="radiogroup"],
div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
    gap: 0.18rem !important;
}

.st-key-result_assessment_card div[data-testid="stRadio"] label,
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label {
    justify-content: flex-start !important;
}

.st-key-result_assessment_card .stButton,
div[class*="st-key-result_assessment_card"] .stButton {
    max-width: 520px !important;
    margin: 0.3rem auto 0 auto !important;
}

.result-assessment-hint {
    text-align: center !important;
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.15rem !important;
    margin-bottom: 0 !important;
}

/* 3) Abschlussfragebogen – Aussagen lesbarer, klarer getrennt */
.st-key-questionnaire_item_card,
div[class*="st-key-questionnaire_item_card"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 26px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    padding: 0.8rem 1.15rem 0.35rem 1.15rem !important;
    margin-bottom: 0.55rem !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"],
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] {
    padding: 0.95rem 0 1rem 0 !important;
    margin-bottom: 0 !important;
    border-bottom: 1px solid rgba(49,92,99,0.09) !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"]:last-of-type,
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"]:last-of-type {
    border-bottom: none !important;
    padding-bottom: 0.4rem !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"] > label,
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label {
    display: block !important;
    text-align: left !important;
    margin-bottom: 0.65rem !important;
}

.st-key-questionnaire_item_card div[data-testid="stRadio"] > label p,
div[class*="st-key-questionnaire_item_card"] div[data-testid="stRadio"] > label p {
    text-align: left !important;
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    font-size: 1.08rem !important;
    line-height: 1.5 !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}

.st-key-questionnaire_item_card div[role="radiogroup"],
div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 0.35rem !important;
    max-width: 540px !important;
    margin: 0 auto !important;
    padding: 0 0.15rem !important;
    flex-wrap: nowrap !important;
}

.st-key-questionnaire_item_card div[role="radiogroup"] label,
div[class*="st-key-questionnaire_item_card"] div[role="radiogroup"] label {
    margin: 0 !important;
}

/* Footer enger an die Box ziehen */
.st-key-questionnaire_footer,
div[class*="st-key-questionnaire_footer"] {
    margin-top: 0.05rem !important;
    padding-top: 0 !important;
}

.st-key-questionnaire_footer .stButton,
div[class*="st-key-questionnaire_footer"] .stButton {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.questionnaire-hint {
    text-align: center !important;
    color: var(--muted) !important;
    font-size: 0.95rem !important;
    margin-top: 0.3rem !important;
    margin-bottom: 0.1rem !important;
}

/* =========================================================
   FINAL FIX: Consent, Result Assessment, Questionnaire Items
   ========================================================= */

/* Einwilligung: Checkbox als sauberer Consent-Baustein */
.st-key-consent_action_area,
div[class*="st-key-consent_action_area"] {
    max-width: 720px !important;
    margin: 0.45rem auto 0.7rem auto !important;
    padding: 1rem 1.1rem 0.9rem 1.1rem !important;
    background: rgba(255,255,255,0.82) !important;
    border: 1px solid rgba(49,92,99,0.11) !important;
    border-radius: 26px !important;
    box-shadow: 0 14px 34px rgba(49,92,99,0.08) !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"],
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
    margin: 0 0 0.75rem 0 !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"] label,
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.65rem !important;
    background: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 18px !important;
    padding: 0.7rem 0.85rem !important;
    box-shadow: 0 8px 20px rgba(49,92,99,0.06) !important;
    max-width: 100% !important;
}

.st-key-consent_action_area div[data-testid="stCheckbox"] label p,
div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label p {
    font-size: 0.95rem !important;
    line-height: 1.32 !important;
    margin: 0 !important;
}

/* Ergebnisscreen: erste Einschätzung kompakter und proportional sauber */
.st-key-result_assessment_card,
div[class*="st-key-result_assessment_card"] {
    padding: 1.45rem 1.35rem 1.05rem 1.35rem !important;
    margin-top: 0.55rem !important;
    margin-bottom: 1.05rem !important;
}

.result-assessment-inner {
    margin-bottom: 0.35rem !important;
}

.result-assessment-inner h3 {
    font-size: 1.55rem !important;
    line-height: 1.14 !important;
    margin: 0 0 0.45rem 0 !important;
}

.result-assessment-inner p {
    font-size: 1rem !important;
    line-height: 1.42 !important;
    margin: 0 0 0.45rem 0 !important;
}

.st-key-result_assessment_card div[data-testid="stRadio"],
div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
    margin-top: 0.15rem !important;
    margin-bottom: 0.45rem !important;
}

.st-key-result_assessment_card div[role="radiogroup"],
div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
    gap: 0.16rem !important;
}

.st-key-result_assessment_card .stButton,
div[class*="st-key-result_assessment_card"] .stButton {
    margin-top: 0.35rem !important;
    margin-bottom: 0.15rem !important;
}

.result-assessment-hint {
    margin-top: 0.35rem !important;
    margin-bottom: 0 !important;
}

/* Abschlussfragebogen: äußere Karte ruhiger */
div[class*="st-key-questionnaire_item_card"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 26px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    padding: 0.65rem 0.75rem !important;
    margin-bottom: 0.45rem !important;
}

/* Jede Aussage als eigener sauberer Mini-Block */
div[class*="st-key-questionnaire_single_item"] {
    border-radius: 20px !important;
    padding: 0.95rem 0.85rem 0.8rem 0.85rem !important;
    margin-bottom: 0.55rem !important;
    border: 1px solid rgba(49,92,99,0.08) !important;
    background: #FFFFFF !important;
}

div[class*="st-key-questionnaire_single_item"]:nth-of-type(even) {
    background: #FAF7F2 !important;
}

div[class*="st-key-questionnaire_single_item"]:last-child {
    margin-bottom: 0 !important;
}

/* Aussage linksbündig, Skala zentriert */
div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] {
    margin: 0 !important;
}

div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] > label {
    display: block !important;
    text-align: left !important;
    margin-bottom: 0.7rem !important;
}

div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] > label p {
    text-align: left !important;
    font-size: 1.02rem !important;
    line-height: 1.45 !important;
    font-weight: 600 !important;
    color: var(--text) !important;
    margin: 0 !important;
}

div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] {
    width: 100% !important;
    max-width: 540px !important;
    margin: 0 auto !important;
    display: grid !important;
    grid-template-columns: repeat(5, 1fr) !important;
    justify-items: center !important;
    align-items: center !important;
    gap: 0 !important;
}

div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label {
    justify-content: center !important;
    margin: 0 !important;
}

/* Footer direkt näher an Fragebogenbox */
.st-key-questionnaire_footer,
div[class*="st-key-questionnaire_footer"] {
    margin-top: 0.25rem !important;
    padding-top: 0 !important;
}

.st-key-questionnaire_footer .stButton,
div[class*="st-key-questionnaire_footer"] .stButton {
    margin-top: 0.05rem !important;
    margin-bottom: 0.35rem !important;
}

.questionnaire-back-spacer {
    height: 0.15rem !important;
}

/* Zurück-Button weiterhin outlined */
div[class*="st-key-back_button_soft"] button {
    background: transparent !important;
    color: #315C63 !important;
    border: 2px solid rgba(49,92,99,0.55) !important;
    box-shadow: none !important;
}

div[class*="st-key-back_button_soft"] button * {
    color: #315C63 !important;
}

div[class*="st-key-back_button_soft"] button:hover {
    background: rgba(49,92,99,0.06) !important;
    border-color: #315C63 !important;
    color: #315C63 !important;
    box-shadow: none !important;
}

/* Mobile Feinanpassung */
@media (max-width: 700px) {
    .st-key-consent_action_area,
    div[class*="st-key-consent_action_area"] {
        margin-top: 0.35rem !important;
        padding: 0.85rem 0.8rem 0.8rem 0.8rem !important;
        border-radius: 22px !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label {
        padding: 0.62rem 0.7rem !important;
        border-radius: 16px !important;
        gap: 0.55rem !important;
    }

    .st-key-consent_action_area div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_action_area"] div[data-testid="stCheckbox"] label p {
        font-size: 0.88rem !important;
        line-height: 1.28 !important;
    }

    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        padding: 1.25rem 1.1rem 0.95rem 1.1rem !important;
    }

    .result-assessment-inner h3 {
        font-size: 1.42rem !important;
        margin-bottom: 0.4rem !important;
    }

    .result-assessment-inner p {
        font-size: 0.96rem !important;
        margin-bottom: 0.4rem !important;
    }

    div[class*="st-key-questionnaire_item_card"] {
        padding: 0.55rem !important;
        border-radius: 24px !important;
    }

    div[class*="st-key-questionnaire_single_item"] {
        padding: 0.95rem 0.75rem 0.75rem 0.75rem !important;
        margin-bottom: 0.5rem !important;
        border-radius: 18px !important;
    }

    div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] > label p {
        font-size: 0.98rem !important;
        line-height: 1.42 !important;
    }

    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] {
        max-width: 100% !important;
    }

    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: 0.1rem !important;
    }

    .questionnaire-hint {
        margin-top: 0.25rem !important;
    }
}

/* =========================================================
   FINAL QUESTIONNAIRE ITEM SEPARATION
   Subtile Hintergrundwechsel pro Aussage
   ========================================================= */

/* Äußere Fragebogenkarte etwas ruhiger halten */
div[class*="st-key-questionnaire_item_card"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(49, 92, 99, 0.12) !important;
    border-radius: 26px !important;
    box-shadow: 0 18px 42px rgba(49, 92, 99, 0.10) !important;
    padding: 0.55rem !important;
    margin-bottom: 0.35rem !important;
}

/* Jede einzelne Aussage als eigener ruhiger Block */
div[class*="st-key-questionnaire_single_item_odd"],
div[class*="st-key-questionnaire_single_item_even"] {
    border-radius: 18px !important;
    padding: 0.95rem 0.85rem 0.85rem 0.85rem !important;
    margin-bottom: 0.5rem !important;
    border: 1px solid rgba(49, 92, 99, 0.07) !important;
    box-shadow: none !important;
}

/* Ungerade Aussagen: fast weiß */
div[class*="st-key-questionnaire_single_item_odd"] {
    background: rgba(255, 255, 255, 0.86) !important;
}

/* Gerade Aussagen: minimal warm abgesetzt */
div[class*="st-key-questionnaire_single_item_even"] {
    background: rgba(248, 244, 237, 0.86) !important;
}

/* Letztes Item ohne unnötigen unteren Abstand */
div[class*="st-key-questionnaire_single_item_odd"]:last-child,
div[class*="st-key-questionnaire_single_item_even"]:last-child {
    margin-bottom: 0 !important;
}

div[class*="st-key-questionnaire_single_item_odd"] div[data-testid="stRadio"] > label p,
div[class*="st-key-questionnaire_single_item_even"] div[data-testid="stRadio"] > label p {
    text-align: left !important;
    font-size: 1.0rem !important;
    line-height: 1.42 !important;
    font-weight: 600 !important;
    color: var(--text) !important;
    margin: 0 !important;
}

/* Skala weiterhin zentriert und gleichmäßig */
div[class*="st-key-questionnaire_single_item_odd"] div[role="radiogroup"],
div[class*="st-key-questionnaire_single_item_even"] div[role="radiogroup"] {
    width: 100% !important;
    max-width: 540px !important;
    margin: 0.55rem auto 0 auto !important;
    display: grid !important;
    grid-template-columns: repeat(5, 1fr) !important;
    align-items: center !important;
    justify-items: center !important;
    gap: 0 !important;
    padding: 0 !important;
}

/* Skalenlabels sauber mittig */
div[class*="st-key-questionnaire_single_item_odd"] div[role="radiogroup"] label,
div[class*="st-key-questionnaire_single_item_even"] div[role="radiogroup"] label {
    width: 100% !important;
    justify-content: center !important;
    margin: 0 !important;
    font-size: 0.98rem !important;
}

/* Keine alten Trennlinien innerhalb der Single-Items */
div[class*="st-key-questionnaire_single_item_odd"] div[data-testid="stRadio"],
div[class*="st-key-questionnaire_single_item_even"] div[data-testid="stRadio"] {
    border-bottom: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Footer näher an die Bewertungsbox */
.st-key-questionnaire_footer,
div[class*="st-key-questionnaire_footer"] {
    margin-top: 0.05rem !important;
    padding-top: 0 !important;
}

.st-key-questionnaire_footer .stButton,
div[class*="st-key-questionnaire_footer"] .stButton {
    margin-top: 0 !important;
    margin-bottom: 0.25rem !important;
}

.questionnaire-back-spacer {
    height: 0.1rem !important;
}

.questionnaire-hint {
    margin-top: 0.2rem !important;
    margin-bottom: 0 !important;
}

/* =========================================================
   FINAL FIX: Consent Screen Text wieder kompakter
   Muss ganz ans Ende des CSS-Blocks
   ========================================================= */

@media (max-width: 700px) {

    .st-key-consent_integrated_card,
    div[class*="st-key-consent_integrated_card"] {
        padding: 1.15rem 0.95rem 1.05rem 0.95rem !important;
        border-radius: 24px !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy p,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy p {
        font-size: 0.86rem !important;
        line-height: 1.42 !important;
        letter-spacing: 0 !important;
        margin-bottom: 0.68rem !important;
        text-align: center !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy .hero-title,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy .hero-title {
        font-size: 1.48rem !important;
        line-height: 1.12 !important;
        margin-bottom: 0.5rem !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy .hero-subtitle,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy .hero-subtitle {
        font-size: 0.86rem !important;
        line-height: 1.38 !important;
        margin-bottom: 0.75rem !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy .info-grid,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-grid {
        margin-top: 0.7rem !important;
        margin-bottom: 0.75rem !important;
        gap: 0.45rem !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy .info-box,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-box {
        min-height: 68px !important;
        padding: 0.58rem 0.3rem !important;
        border-radius: 15px !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy .info-box strong,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-box strong {
        font-size: 0.82rem !important;
        line-height: 1.14 !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy .info-box span,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy .info-box span {
        font-size: 0.68rem !important;
        line-height: 1.16 !important;
    }

    .st-key-consent_inline_box,
    div[class*="st-key-consent_inline_box"] {
        margin-top: 0.75rem !important;
        padding: 0.72rem 0.65rem 0.75rem 0.65rem !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        font-size: 0.86rem !important;
        line-height: 1.25 !important;
    }
}

/* =========================================================
   FINAL CONSENT REDESIGN
   Einwilligung als kompakter Abschluss der Hauptkarte
   ========================================================= */

/* Hauptkarte Screen 2 */
.st-key-consent_integrated_card,
div[class*="st-key-consent_integrated_card"] {
    width: min(820px, 100%) !important;
    margin: 0 auto 0.9rem auto !important;
    padding: 1.7rem 1.85rem 1.45rem 1.85rem !important;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.045), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.07), transparent 34%),
        rgba(255,255,255,0.97) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 30px !important;
    box-shadow: 0 20px 48px rgba(49,92,99,0.11) !important;
    text-align: center !important;
}

/* Textbereich */
.st-key-consent_integrated_card .consent-screen-copy p,
div[class*="st-key-consent_integrated_card"] .consent-screen-copy p {
    text-align: center !important;
    font-size: 0.95rem !important;
    line-height: 1.52 !important;
    margin: 0 0 0.75rem 0 !important;
}

/* Überschrift und Untertitel */
.st-key-consent_integrated_card .hero-title,
div[class*="st-key-consent_integrated_card"] .hero-title {
    text-align: center !important;
    margin-bottom: 0.5rem !important;
}

.st-key-consent_integrated_card .hero-subtitle,
div[class*="st-key-consent_integrated_card"] .hero-subtitle {
    text-align: center !important;
    margin-bottom: 0.9rem !important;
}

/* Info-Kacheln im Consent-Screen */
.st-key-consent_integrated_card .info-grid,
div[class*="st-key-consent_integrated_card"] .info-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 0.75rem !important;
    margin: 0.95rem 0 1rem 0 !important;
}

.st-key-consent_integrated_card .info-box,
div[class*="st-key-consent_integrated_card"] .info-box {
    min-height: 88px !important;
    padding: 0.88rem 0.48rem !important;
    border-radius: 19px !important;
    background: rgba(248,244,237,0.92) !important;
    border: 1px solid rgba(49,92,99,0.10) !important;
}

/* Feine Trennlinie vor der Einwilligung */
.consent-divider {
    width: 100%;
    height: 1px;
    margin: 1rem auto 0.75rem auto;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(49,92,99,0.14),
        transparent
    );
}

/* Die Einwilligung ist KEINE eigene große Card mehr */
.st-key-consent_inline_box,
div[class*="st-key-consent_inline_box"] {
    width: min(620px, 100%) !important;
    margin: 0 auto 0.75rem auto !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Checkbox-Zeile als leichte Pill */
.st-key-consent_inline_box div[data-testid="stCheckbox"],
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
    display: flex !important;
    justify-content: center !important;
    margin: 0 0 0.55rem 0 !important;
    padding: 0 !important;
}

/* Checkbox-Label */
.st-key-consent_inline_box div[data-testid="stCheckbox"] label,
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 0.72rem !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    padding: 0.62rem 1.05rem 0.62rem 0.78rem !important;
    background: rgba(248,244,237,0.78) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 18px !important;
    box-shadow: none !important;
    text-align: left !important;
}

/* Checkbox-Text */
.st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
    font-size: 0.88rem !important;
    line-height: 1.28 !important;
    margin: 0 !important;
    color: var(--text) !important;
    flex: 1 1 auto !important;
}

/* Button kompakter */
.st-key-consent_inline_box .stButton,
div[class*="st-key-consent_inline_box"] .stButton {
    display: flex !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
}

.st-key-consent_inline_box .stButton > button,
div[class*="st-key-consent_inline_box"] .stButton > button {
    width: min(290px, 78vw) !important;
    max-width: 290px !important;
    min-height: 46px !important;
    padding: 0.48rem 1rem !important;
    font-size: 0.91rem !important;
    border-radius: 999px !important;
    margin: 0 auto !important;
}

/* Kontakt klein und ruhig */
.consent-contact {
    margin: 0.85rem 0 0 0 !important;
    padding-top: 0.75rem !important;
    border-top: 1px solid rgba(49,92,99,0.08) !important;
    font-size: 0.84rem !important;
    line-height: 1.35 !important;
    text-align: center !important;
    color: var(--muted) !important;
}

.consent-contact strong {
    color: var(--text) !important;
}

/* Mobile Feinschliff */
@media (max-width: 700px) {
    .st-key-consent_integrated_card,
    div[class*="st-key-consent_integrated_card"] {
        width: 100% !important;
        padding: 1.2rem 0.95rem 1.05rem 0.95rem !important;
        border-radius: 24px !important;
        margin-bottom: 0.75rem !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy p,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy p {
        font-size: 0.86rem !important;
        line-height: 1.42 !important;
        margin-bottom: 0.68rem !important;
    }

    .st-key-consent_integrated_card .hero-title,
    div[class*="st-key-consent_integrated_card"] .hero-title {
        font-size: 1.48rem !important;
        line-height: 1.12 !important;
    }

    .st-key-consent_integrated_card .hero-subtitle,
    div[class*="st-key-consent_integrated_card"] .hero-subtitle {
        font-size: 0.86rem !important;
        line-height: 1.38 !important;
        margin-bottom: 0.75rem !important;
    }

    .st-key-consent_integrated_card .info-grid,
    div[class*="st-key-consent_integrated_card"] .info-grid {
        gap: 0.45rem !important;
        margin: 0.75rem 0 0.8rem 0 !important;
    }

    .st-key-consent_integrated_card .info-box,
    div[class*="st-key-consent_integrated_card"] .info-box {
        min-height: 82px !important;
        padding: 0.72rem 0.34rem !important;
        border-radius: 17px !important;
    }

    .st-key-consent_integrated_card .info-box strong,
    div[class*="st-key-consent_integrated_card"] .info-box strong {
        font-size: 0.88rem !important;
    }

    .st-key-consent_integrated_card .info-box span,
    div[class*="st-key-consent_integrated_card"] .info-box span {
        font-size: 0.72rem !important;
        line-height: 1.22 !important;
    }

    .consent-divider {
        margin: 0.85rem auto 0.65rem auto !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
        padding: 0.56rem 0.92rem 0.56rem 0.68rem !important;
        gap: 0.56rem !important;
        border-radius: 16px !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        font-size: 0.82rem !important;
        line-height: 1.24 !important;
    }

    .st-key-consent_inline_box .stButton > button,
    div[class*="st-key-consent_inline_box"] .stButton > button {
        width: min(276px, 76vw) !important;
        max-width: 276px !important;
        min-height: 44px !important;
        font-size: 0.88rem !important;
        padding: 0.46rem 0.95rem !important;
    }

    .consent-contact {
        margin-top: 0.75rem !important;
        padding-top: 0.65rem !important;
        font-size: 0.78rem !important;
        line-height: 1.32 !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL OVERRIDE: Consent Screen Mobile V2
   Checkbox-Pill volle Breite + Button-Text exakt zentriert
   Ganz am Ende des zweiten CSS-Blocks einsetzen
   ========================================================= */

@media (max-width: 700px) {

    /* Hauptkarte Screen 2 */
    .st-key-consent_integrated_card,
    div[class*="st-key-consent_integrated_card"] {
        width: 100% !important;
        padding: 1.18rem 0.95rem 1.05rem 0.95rem !important;
        border-radius: 24px !important;
        margin-bottom: 0.7rem !important;
        box-sizing: border-box !important;
    }

    /* Text kompakt halten */
    .st-key-consent_integrated_card .consent-screen-copy p,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy p {
        font-size: 0.86rem !important;
        line-height: 1.42 !important;
        margin-bottom: 0.68rem !important;
        text-align: center !important;
    }

    /* Drei Kacheln: wie vorher, nicht zu groß */
    .st-key-consent_integrated_card .info-grid,
    div[class*="st-key-consent_integrated_card"] .info-grid {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.48rem !important;
        margin: 0.78rem 0 0.8rem 0 !important;
    }

    .st-key-consent_integrated_card .info-box,
    div[class*="st-key-consent_integrated_card"] .info-box {
        min-height: 78px !important;
        padding: 0.68rem 0.32rem !important;
        border-radius: 16px !important;
        background: rgba(248,244,237,0.92) !important;
        border: 1px solid rgba(49,92,99,0.10) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        box-sizing: border-box !important;
    }

    .st-key-consent_integrated_card .info-box strong,
    div[class*="st-key-consent_integrated_card"] .info-box strong {
        font-size: 0.88rem !important;
        line-height: 1.14 !important;
        margin-bottom: 0.16rem !important;
    }

    .st-key-consent_integrated_card .info-box span,
    div[class*="st-key-consent_integrated_card"] .info-box span {
        font-size: 0.72rem !important;
        line-height: 1.18 !important;
    }

    /* Trennlinie */
    .consent-divider {
        margin: 0.85rem auto 0.62rem auto !important;
    }

    /* Consent-Bereich: nimmt die volle verfügbare Kartenbreite ein */
    .st-key-consent_inline_box,
    div[class*="st-key-consent_inline_box"] {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto 0.68rem auto !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
    }

    /* Checkbox-Element selbst über volle Breite */
    .st-key-consent_inline_box div[data-testid="stCheckbox"],
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
        width: 100% !important;
        max-width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 0 0.58rem 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    /* Checkbox-Pill: rechts deutlich breiter */
    .st-key-consent_inline_box div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 100% !important;
        box-sizing: border-box !important;

        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.58rem !important;

        padding: 0.58rem 0.74rem !important;
        border-radius: 16px !important;
        background: rgba(248,244,237,0.78) !important;
        border: 1px solid rgba(49,92,99,0.12) !important;
        box-shadow: none !important;
        text-align: left !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        font-size: 0.82rem !important;
        line-height: 1.24 !important;
        margin: 0 !important;
        padding: 0 !important;
        flex: 1 1 auto !important;
        text-align: left !important;
    }

    /* Button-Wrapper */
    .st-key-consent_integrated_card .st-key-consent_inline_box .stButton,
    div[class*="st-key-consent_integrated_card"] div[class*="st-key-consent_inline_box"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Button selbst: Text exakt mittig */
    .st-key-consent_integrated_card .st-key-consent_inline_box .stButton > button,
    div[class*="st-key-consent_integrated_card"] div[class*="st-key-consent_inline_box"] .stButton > button {
        width: min(276px, 70vw) !important;
        max-width: 276px !important;
        height: 44px !important;
        min-height: 44px !important;

        padding: 0 !important;
        margin: 0 auto !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        font-size: 0.88rem !important;
        line-height: 1 !important;
        text-align: center !important;
        border-radius: 999px !important;
        box-sizing: border-box !important;
    }

    /* Streamlit legt Text oft in p/span/div – alles sauber zentrieren */
    .st-key-consent_integrated_card .st-key-consent_inline_box .stButton > button p,
    .st-key-consent_integrated_card .st-key-consent_inline_box .stButton > button span,
    .st-key-consent_integrated_card .st-key-consent_inline_box .stButton > button div,
    div[class*="st-key-consent_integrated_card"] div[class*="st-key-consent_inline_box"] .stButton > button p,
    div[class*="st-key-consent_integrated_card"] div[class*="st-key-consent_inline_box"] .stButton > button span,
    div[class*="st-key-consent_integrated_card"] div[class*="st-key-consent_inline_box"] .stButton > button div {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    /* Kontakt */
    .consent-contact {
        margin-top: 0.68rem !important;
        padding-top: 0.62rem !important;
        font-size: 0.78rem !important;
        line-height: 1.3 !important;
        border-top: 1px solid rgba(49,92,99,0.08) !important;
        text-align: center !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL OVERRIDE: Result Assessment Card V2
   Muss ganz ans Ende des zweiten CSS-Blocks
   ========================================================= */

@media (max-width: 700px) {

    .st-key-result_assessment_card,
    div[class*="st-key-result_assessment_card"] {
        padding: 1.05rem 1.1rem 0.8rem 1.1rem !important;
        margin-top: 0.45rem !important;
        margin-bottom: 0.75rem !important;
        border-radius: 24px !important;
        text-align: left !important;
    }

    .st-key-result_assessment_card .result-assessment-inner,
    div[class*="st-key-result_assessment_card"] .result-assessment-inner {
        margin: 0 0 0.18rem 0 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    .st-key-result_assessment_card .result-assessment-inner h3,
    div[class*="st-key-result_assessment_card"] .result-assessment-inner h3 {
        font-size: 1.28rem !important;
        line-height: 1.12 !important;
        margin: 0 0 0.28rem 0 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    .st-key-result_assessment_card .result-assessment-inner p,
    div[class*="st-key-result_assessment_card"] .result-assessment-inner p {
        font-size: 0.92rem !important;
        line-height: 1.32 !important;
        margin: 0 0 0.22rem 0 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    .st-key-result_assessment_card div[data-testid="stRadio"],
    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] {
        margin-top: 0 !important;
        margin-bottom: 0.18rem !important;
        padding-top: 0 !important;
    }

    .st-key-result_assessment_card div[role="radiogroup"],
    div[class*="st-key-result_assessment_card"] div[role="radiogroup"] {
        gap: 0 !important;
        margin-top: 0 !important;
    }

    .st-key-result_assessment_card div[data-testid="stRadio"] label,
    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label {
        min-height: 27px !important;
        padding-top: 0.02rem !important;
        padding-bottom: 0.02rem !important;
        justify-content: flex-start !important;
    }

    .st-key-result_assessment_card div[data-testid="stRadio"] label p,
    div[class*="st-key-result_assessment_card"] div[data-testid="stRadio"] label p {
        font-size: 0.91rem !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }

    .st-key-result_assessment_card .stButton,
    div[class*="st-key-result_assessment_card"] .stButton {
        margin-top: 0.12rem !important;
        margin-bottom: 0.05rem !important;
    }

    .st-key-result_assessment_card .stButton > button,
    div[class*="st-key-result_assessment_card"] .stButton > button {
        min-height: 44px !important;
        height: 44px !important;
        padding: 0 !important;
        font-size: 0.9rem !important;
    }

    .st-key-result_assessment_card .result-assessment-hint,
    div[class*="st-key-result_assessment_card"] .result-assessment-hint {
        font-size: 0.74rem !important;
        line-height: 1.22 !important;
        font-weight: 400 !important;
        color: var(--muted) !important;
        text-align: center !important;
        margin: 0.22rem 0 0 0 !important;
        padding: 0 !important;
    }

    .st-key-result_assessment_card .result-assessment-hint *,
    div[class*="st-key-result_assessment_card"] .result-assessment-hint * {
        font-size: 0.74rem !important;
        line-height: 2 !important;
        font-weight: 400 !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL OVERRIDE: Questionnaire Footer Buttons
   Abstand zwischen Weiter und Zurück stark reduzieren
   ========================================================= */

@media (max-width: 700px) {

    /* Footer-Container des Weiter-Buttons ohne zusätzlichen unteren Abstand */
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: 0.05rem !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] .stButton {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .st-key-questionnaire_footer .stButton > button,
    div[class*="st-key-questionnaire_footer"] .stButton > button {
        margin-bottom: 0 !important;
    }

    /* Falls ein künstlicher Spacer zwischen Weiter und Zurück existiert */
    .questionnaire-back-spacer {
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: none !important;
    }

    /* Zurück-Button näher an den Weiter-Button ziehen */
    .st-key-back_button_soft,
    div[class*="st-key-back_button_soft"] {
        margin-top: 0.18rem !important;
        margin-bottom: 0.15rem !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .st-key-back_button_soft .stButton,
    div[class*="st-key-back_button_soft"] .stButton {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    .st-key-back_button_soft .stButton > button,
    div[class*="st-key-back_button_soft"] .stButton > button {
        margin-top: 0 !important;
    }

    /* Streamlit-Elementcontainer erzeugen manchmal extra vertikale Luft */
    .st-key-questionnaire_footer div[data-testid="element-container"],
    div[class*="st-key-questionnaire_footer"] div[data-testid="element-container"],
    .st-key-back_button_soft div[data-testid="element-container"],
    div[class*="st-key-back_button_soft"] div[data-testid="element-container"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    /* Hinweistext unter den Buttons wieder etwas näher ziehen */
    .questionnaire-hint {
        margin-top: 0.25rem !important;
    }
}

@media (max-width: 700px) {
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.3rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.4rem !important;
        padding: 0 !important;
    }

    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] .stButton {
        margin: 0 !important;
        padding: 0 !important;
    }

    .st-key-back_button_soft,
    div[class*="st-key-back_button_soft"] {
        margin: 0 !important;
        padding: 0 !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL FIX: Zurück-Button im Fragebogen zentrieren
   ========================================================= */

@media (max-width: 700px) {

    div[class*="st-key-back_button_soft"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0.35rem auto 0.15rem auto !important;
        padding: 0 !important;
    }

    div[class*="st-key-back_button_soft"] div[data-testid="stVerticalBlock"],
    div[class*="st-key-back_button_soft"] div[data-testid="element-container"],
    div[class*="st-key-back_button_soft"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    div[class*="st-key-back_button_soft"] .stButton > button {
        width: min(70vw, 285px) !important;
        max-width: 285px !important;
        min-height: 48px !important;
        margin-left: auto !important;
        margin-right: auto !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        background: transparent !important;
        color: #315C63 !important;
        border: 2px solid rgba(49, 92, 99, 0.55) !important;
        box-shadow: none !important;
        border-radius: 999px !important;
    }

    div[class*="st-key-back_button_soft"] .stButton > button * {
        color: #315C63 !important;
        margin: 0 !important;
        text-align: center !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL FIX: Abschlussfragebogen weiß + Aussagen zentriert
   Muss ganz am Ende des CSS-Blocks stehen
   ========================================================= */

@media (max-width: 700px) {

    /* Einzelne Aussage-Blöcke einheitlich weiß */
    div[class*="st-key-questionnaire_single_item_odd"],
    div[class*="st-key-questionnaire_single_item_even"],
    div[class*="questionnaire_single_item_odd"],
    div[class*="questionnaire_single_item_even"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1px solid rgba(49, 92, 99, 0.09) !important;
        border-radius: 18px !important;
        box-shadow: none !important;
    }

    /* Aussage selbst zentrieren */
    div[class*="st-key-questionnaire_single_item_odd"] div[data-testid="stRadio"] > label,
    div[class*="st-key-questionnaire_single_item_even"] div[data-testid="stRadio"] > label,
    div[class*="questionnaire_single_item_odd"] div[data-testid="stRadio"] > label,
    div[class*="questionnaire_single_item_even"] div[data-testid="stRadio"] > label {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
        margin-bottom: 0.7rem !important;
    }

    div[class*="st-key-questionnaire_single_item_odd"] div[data-testid="stRadio"] > label p,
    div[class*="st-key-questionnaire_single_item_even"] div[data-testid="stRadio"] > label p,
    div[class*="questionnaire_single_item_odd"] div[data-testid="stRadio"] > label p,
    div[class*="questionnaire_single_item_even"] div[data-testid="stRadio"] > label p {
        text-align: center !important;
        width: 100% !important;
        max-width: 94% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        font-size: 0.98rem !important;
        line-height: 1.42 !important;
        font-weight: 600 !important;
        color: var(--text) !important;
    }

    /* Skala weiterhin sauber zentriert */
    div[class*="st-key-questionnaire_single_item_odd"] div[role="radiogroup"],
    div[class*="st-key-questionnaire_single_item_even"] div[role="radiogroup"],
    div[class*="questionnaire_single_item_odd"] div[role="radiogroup"],
    div[class*="questionnaire_single_item_even"] div[role="radiogroup"] {
        width: 100% !important;
        max-width: 92% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        justify-items: center !important;
        align-items: center !important;
        gap: 0 !important;
    }
}

@media (min-width: 901px) {

    /* =========================================================
       SCREEN 2 DESKTOP FIX
       Nur Desktop – Mobile bleibt unberührt
       ========================================================= */

    /* Hauptkarte etwas luftiger */
    .st-key-consent_integrated_card,
    div[class*="st-key-consent_integrated_card"] {
        padding: 1.9rem 2rem 1.65rem 2rem !important;
    }

    /* Titel / Untertitel / Fließtext etwas mehr Luft */
    .st-key-consent_integrated_card .hero-title,
    div[class*="st-key-consent_integrated_card"] .hero-title {
        margin-bottom: 0.6rem !important;
    }

    .st-key-consent_integrated_card .hero-subtitle,
    div[class*="st-key-consent_integrated_card"] .hero-subtitle {
        margin-bottom: 1.15rem !important;
    }

    .st-key-consent_integrated_card .consent-screen-copy p,
    div[class*="st-key-consent_integrated_card"] .consent-screen-copy p {
        margin: 0 0 1rem 0 !important;
        line-height: 1.6 !important;
        text-align: center !important;
    }

    .st-key-consent_integrated_card .info-grid,
    div[class*="st-key-consent_integrated_card"] .info-grid {
        margin: 1.15rem 0 1.15rem 0 !important;
    }

    .consent-divider {
        margin: 1.1rem auto 0.95rem auto !important;
    }

    /* Checkbox-Bereich insgesamt mittig */
    .st-key-consent_inline_box,
    div[class*="st-key-consent_inline_box"] {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto 0.8rem auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"],
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 0 0.7rem 0 !important;
        padding: 0 !important;
    }

    /* Checkbox-Pill kompakt und zentriert */
    .st-key-consent_inline_box div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
        width: fit-content !important;
        max-width: 100% !important;
        margin: 0 auto !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.7rem !important;
        padding: 0.68rem 1.1rem !important;
        text-align: center !important;
    }

    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        margin: 0 !important;
        text-align: center !important;
        line-height: 1.3 !important;
    }

    /* Button-Wrapper mittig */
    .st-key-consent_inline_box .stButton,
    div[class*="st-key-consent_inline_box"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Button selbst: Text exakt mittig */
    .st-key-consent_inline_box .stButton > button,
    div[class*="st-key-consent_inline_box"] .stButton > button {
        width: min(290px, 100%) !important;
        max-width: 290px !important;
        min-height: 52px !important;
        padding: 0.68rem 1.35rem !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        text-align: center !important;
        line-height: 1.1 !important;
        border-radius: 999px !important;
        box-sizing: border-box !important;
    }

    .st-key-consent_inline_box .stButton > button p,
    .st-key-consent_inline_box .stButton > button span,
    .st-key-consent_inline_box .stButton > button div,
    div[class*="st-key-consent_inline_box"] .stButton > button p,
    div[class*="st-key-consent_inline_box"] .stButton > button span,
    div[class*="st-key-consent_inline_box"] .stButton > button div {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1 !important;
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FINAL: Abschlussfragebogen wirklich zentrieren
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    /* Einzelne Aussage-Karten */
    div[class*="st-key-questionnaire_single_item"] {
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    /* Neuer separater Aussage-Text */
    .questionnaire-question-text {
        width: 100% !important;
        max-width: 900px !important;
        margin: 0 auto 1rem auto !important;
        text-align: center !important;
        font-size: 1.05rem !important;
        line-height: 1.45 !important;
        font-weight: 650 !important;
        color: var(--text) !important;
    }

    /* Radio-Komponente über volle Itembreite */
    div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    /* Die eigentliche 1–5-Skala bekommt eine feste Breite */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] {
        width: 560px !important;
        min-width: 560px !important;
        max-width: 560px !important;

        margin: 0.25rem auto 0 auto !important;
        padding: 0 !important;

        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        justify-items: center !important;
        align-items: center !important;
        gap: 0 !important;
    }

    /* Jede Antwortoption gleich breit */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label {
        width: 100% !important;
        margin: 0 !important;

        display: flex !important;
        justify-content: center !important;
        align-items: center !important;

        text-align: center !important;
    }

    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label p {
        margin: 0 !important;
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FINAL POLISH: Fragebogen
   Button zentrieren, Items einheitlich weiß,
   Skala kompakter
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    /* 1) Alle Aussage-Blöcke einheitlich weiß */
    div[class*="st-key-questionnaire_single_item_odd"],
    div[class*="st-key-questionnaire_single_item_even"],
    div[class*="questionnaire_single_item_odd"],
    div[class*="questionnaire_single_item_even"] {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border: 1px solid rgba(49, 92, 99, 0.08) !important;
    }

    /* 2) Weiter-Button im Footer sauber zentrieren */
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 0.2rem !important;
        padding-top: 0 !important;
    }

    .st-key-questionnaire_footer div[data-testid="stVerticalBlock"],
    .st-key-questionnaire_footer div[data-testid="element-container"],
    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] div[data-testid="stVerticalBlock"],
    div[class*="st-key-questionnaire_footer"] div[data-testid="element-container"],
    div[class*="st-key-questionnaire_footer"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    .st-key-questionnaire_footer .stButton > button,
    div[class*="st-key-questionnaire_footer"] .stButton > button {
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 130px !important;
    }

    /* 3) Skalen kompakter machen */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] {
        width: 440px !important;
        min-width: 440px !important;
        max-width: 440px !important;

        margin: 0.15rem auto 0 auto !important;
        padding: 0 !important;

        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        justify-items: center !important;
        align-items: center !important;
        gap: 0 !important;
    }

    /* Zahlen/Optionen enger und sauber mittig */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label {
        width: 100% !important;
        margin: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FIX: Zurück-Button im Fragebogen zentrieren
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    .st-key-back_button_soft,
    div[class*="st-key-back_button_soft"] {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0.35rem auto 0 auto !important;
        padding: 0 !important;
    }

    .st-key-back_button_soft div[data-testid="stVerticalBlock"],
    .st-key-back_button_soft div[data-testid="element-container"],
    .st-key-back_button_soft .stButton,
    div[class*="st-key-back_button_soft"] div[data-testid="stVerticalBlock"],
    div[class*="st-key-back_button_soft"] div[data-testid="element-container"],
    div[class*="st-key-back_button_soft"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    .st-key-back_button_soft .stButton > button,
    div[class*="st-key-back_button_soft"] .stButton > button {
        margin: 0 auto !important;
        min-width: 140px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FIX: Anleitungstext zentrieren
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    /* Anleitungskarte insgesamt zentrieren */
    .text-card,
    .text-card * {
        text-align: center !important;
    }

    /* Überschrift "Deine Aufgabe" */
    .text-card h3 {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Fließtexte in der Anleitung */
    .text-card p {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        max-width: 980px !important;
    }

    /* Swipe-/Likert-Hinweisboxen bleiben sauber zentriert */
    .instruction-row {
        justify-content: center !important;
    }

    .instruction-box,
    .instruction-box * {
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FIX: obere Fragebogen-Box zentrieren
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    .questionnaire-section-card {
        text-align: center !important;
        padding-left: 1.6rem !important;
        padding-right: 1.6rem !important;
    }

    .questionnaire-section-label,
    .questionnaire-section-title,
    .questionnaire-section-helper {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    .questionnaire-section-title {
        margin-bottom: 0.9rem !important;
    }

    .questionnaire-section-helper {
        max-width: 920px !important;
        margin-bottom: 1.15rem !important;
    }

    .scale-legend-grid {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        justify-content: center !important;
    }

    .scale-legend-box,
    .scale-legend-box * {
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FIX: Pre-Questionnaire-Box zentrieren
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    .pre-questionnaire-clean-wrap .screen-card-info {
        text-align: center !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
    }

    .pre-questionnaire-clean-wrap .screen-card-info p,
    .pre-questionnaire-clean-wrap .screen-card-info div,
    .pre-questionnaire-clean-wrap .screen-card-info span {
        text-align: center !important;
    }

    .pre-questionnaire-clean-wrap .screen-card-info p {
        margin-left: auto !important;
        margin-right: auto !important;
        max-width: 1100px !important;
    }

    .pre-questionnaire-clean-wrap .info-grid {
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        justify-content: center !important;
    }

    .pre-questionnaire-clean-wrap .info-box,
    .pre-questionnaire-clean-wrap .info-box *,
    .pre-questionnaire-clean-wrap .screen-card-info .info-box,
    .pre-questionnaire-clean-wrap .screen-card-info .info-box * {
        text-align: center !important;
    }
}

/* =========================================================
   DESKTOP FIX: Fragebogen-Buttons sauber untereinander zentrieren
   Mobile bleibt unberührt
   ========================================================= */

@media (min-width: 901px) {

    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"],
    .st-key-back_button_soft,
    div[class*="st-key-back_button_soft"] {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding: 0 !important;
    }

    /* Weiter-Button */
    .st-key-questionnaire_footer,
    div[class*="st-key-questionnaire_footer"] {
        margin-top: 0.65rem !important;
        margin-bottom: 0.45rem !important;
    }

    /* Zurück-Button */
    .st-key-back_button_soft,
    div[class*="st-key-back_button_soft"] {
        margin-top: 0.15rem !important;
        margin-bottom: 0.35rem !important;
    }

    .st-key-questionnaire_footer .stButton,
    div[class*="st-key-questionnaire_footer"] .stButton,
    .st-key-back_button_soft .stButton,
    div[class*="st-key-back_button_soft"] .stButton {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    .st-key-questionnaire_footer .stButton > button,
    div[class*="st-key-questionnaire_footer"] .stButton > button,
    .st-key-back_button_soft .stButton > button,
    div[class*="st-key-back_button_soft"] .stButton > button {
        width: 180px !important;
        min-width: 180px !important;
        max-width: 180px !important;
        min-height: 50px !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        margin: 0 auto !important;
        text-align: center !important;
        border-radius: 999px !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL MOBILE FIX:
   Abschlussfragebogen Aussagen + Skalen zentrieren
   Desktop bleibt unberührt
   ========================================================= */

@media (max-width: 700px) {

    /* Äußere Fragebogenkarte */
    div[class*="st-key-questionnaire_item_card"] {
        text-align: center !important;
    }

    /* Einzelne Aussage-Karten zentrieren */
    div[class*="st-key-questionnaire_single_item"] {
        width: 100% !important;
        box-sizing: border-box !important;

        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;

        text-align: center !important;
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    /* Neuer separater Aussage-Text */
    .questionnaire-question-text {
        width: 100% !important;
        max-width: 100% !important;

        margin: 0 auto 1.05rem auto !important;
        padding: 0 0.15rem !important;

        display: block !important;
        text-align: center !important;

        font-size: 1.02rem !important;
        line-height: 1.45 !important;
        font-weight: 600 !important;
        color: var(--text) !important;
    }

    .questionnaire-question-text,
    .questionnaire-question-text * {
        text-align: center !important;
    }

    /* Radio-Widget selbst zentrieren */
    div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] {
        width: 100% !important;
        max-width: 100% !important;

        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;

        margin: 0 auto !important;
        padding: 0 !important;
        text-align: center !important;
    }

    /* Leeres Streamlit-Radio-Label ausblenden */
    div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] > label,
    div[class*="st-key-questionnaire_single_item"] div[data-testid="stWidgetLabel"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 1–5-Skala: feste mobile Breite und mittig */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] {
        width: min(330px, 92vw) !important;
        max-width: min(330px, 92vw) !important;
        min-width: 0 !important;

        margin: 0 auto !important;
        padding: 0 !important;

        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        justify-items: center !important;
        align-items: center !important;
        gap: 0 !important;

        text-align: center !important;
    }

    /* Jede Antwortoption gleich breit */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label {
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;

        display: flex !important;
        justify-content: center !important;
        align-items: center !important;

        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
    }

    /* Zahl neben dem Radio-Button sauber ausrichten */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label p,
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label span {
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        line-height: 1.1 !important;
    }

    /* Radio-Kreis etwas ruhiger platzieren */
    div[class*="st-key-questionnaire_single_item"] input[type="radio"] {
        margin-right: 0.28rem !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL MOBILE FIX:
   Fragebogen-Skala exakt zentrieren
   Desktop bleibt unberührt
   ========================================================= */

@media (max-width: 700px) {

    /* Radio-Widget in jeder Aussagebox vollständig zentrieren */
    div[class*="st-key-questionnaire_single_item"] div[data-testid="stRadio"] {
        width: 100% !important;
        max-width: 100% !important;

        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;

        margin-left: auto !important;
        margin-right: auto !important;
        padding: 0 !important;
        text-align: center !important;
    }

    /* Skala bewusst kompakter machen, damit sie optisch wirklich mittig steht */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] {
        width: min(285px, 76vw) !important;
        min-width: 0 !important;
        max-width: min(285px, 76vw) !important;

        margin-left: auto !important;
        margin-right: auto !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;

        padding: 0 !important;
        box-sizing: border-box !important;

        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        justify-items: center !important;
        align-items: center !important;
        gap: 0 !important;

        text-align: center !important;
    }

    /* Jede Antwortoption exakt in ihrer Spalte zentrieren */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;

        text-align: center !important;
    }

    /* Radio-Kreis + Zahl als kompakte Einheit */
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] input[type="radio"] {
        width: 16px !important;
        height: 16px !important;
        min-width: 16px !important;
        min-height: 16px !important;

        margin: 0 0.25rem 0 0 !important;
        padding: 0 !important;
        flex: 0 0 auto !important;
    }

    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label p,
    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label span {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        text-align: center !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL MOBILE FIX: Consent-Checkbox zentrieren
   Nur Mobile – Desktop bleibt unberührt
   ========================================================= */

@media (max-width: 700px) {

    /* Consent-Bereich insgesamt mittig halten */
    .st-key-consent_inline_box,
    div[class*="st-key-consent_inline_box"] {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;

        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Checkbox-Wrapper mittig */
    .st-key-consent_inline_box div[data-testid="stCheckbox"],
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] {
        width: 100% !important;
        max-width: 100% !important;

        display: flex !important;
        justify-content: center !important;
        align-items: center !important;

        margin: 0 auto 0.58rem auto !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    /* Checkbox-Pill NICHT mehr volle Breite, sondern kompakt und zentriert */
    .st-key-consent_inline_box div[data-testid="stCheckbox"] label,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label {
        width: fit-content !important;
        min-width: 0 !important;
        max-width: min(100%, 92vw) !important;

        margin-left: auto !important;
        margin-right: auto !important;

        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;

        gap: 0.58rem !important;
        padding: 0.58rem 0.78rem !important;

        border-radius: 16px !important;
        background: rgba(248,244,237,0.78) !important;
        border: 1px solid rgba(49,92,99,0.12) !important;
        box-shadow: none !important;

        box-sizing: border-box !important;
        text-align: left !important;
    }

    /* Text darf umbrechen, aber die gesamte Pill bleibt mittig */
    .st-key-consent_inline_box div[data-testid="stCheckbox"] label p,
    div[class*="st-key-consent_inline_box"] div[data-testid="stCheckbox"] label p {
        flex: 0 1 auto !important;
        width: auto !important;
        max-width: 100% !important;

        margin: 0 !important;
        padding: 0 !important;

        font-size: 0.82rem !important;
        line-height: 1.24 !important;
        text-align: left !important;
    }
}

/* =========================================================
   ABSCHLUSSFRAGEBOGEN: 4er-Skala final
   Nur Abschlussfragebogen, Hauptfragebogen bleibt unverändert
   ========================================================= */

.scale-legend-grid-4,
.questionnaire-section-card .scale-legend-grid-4 {
    display: grid !important;
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 0.55rem !important;
}

/* 4er-Radio-Skala im Abschlussfragebogen */
div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"],
div[class*="questionnaire_single_item"] div[role="radiogroup"] {
    width: 100% !important;
    max-width: 480px !important;
    margin: 0.55rem auto 0 auto !important;
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    justify-items: center !important;
    align-items: center !important;
    gap: 0 !important;
}

/* Jede Antwortoption gleichmäßig zentrieren */
div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"] label,
div[class*="questionnaire_single_item"] div[role="radiogroup"] label {
    width: 100% !important;
    justify-content: center !important;
    margin: 0 !important;
    text-align: center !important;
}

/* Mobile: 4er-Legende kompakt halten */
@media (max-width: 700px) {
    .scale-legend-grid-4,
    .questionnaire-section-card .scale-legend-grid-4 {
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 0.35rem !important;
    }

    .scale-legend-grid-4 .scale-legend-box {
        padding: 0.55rem 0.22rem !important;
        min-height: 64px !important;
        border-radius: 14px !important;
    }

    .scale-legend-grid-4 .scale-legend-box strong {
        font-size: 0.9rem !important;
    }

    .scale-legend-grid-4 .scale-legend-box span {
        font-size: 0.62rem !important;
        line-height: 1.15 !important;
    }

    div[class*="st-key-questionnaire_single_item"] div[role="radiogroup"],
    div[class*="questionnaire_single_item"] div[role="radiogroup"] {
        max-width: 94% !important;
        grid-template-columns: repeat(4, 1fr) !important;
    }
}

</style>
    """,
    unsafe_allow_html=True,
)

items = [
    {"id": 1, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich fühle mich wohl, wenn mein Team zusammenhält."},
    {"id": 2, "dimension": "Leistung / Wettbewerb", "text": "Klare Ziele motivieren mich im Arbeitsalltag."},
    {"id": 3, "dimension": "Innovation / Flexibilität", "text": "Ich mag es, wenn neue Ideen schnell ausprobiert werden."},
    {"id": 4, "dimension": "Struktur / Stabilität", "text": "Klare Abläufe geben mir Sicherheit bei der Arbeit."},

    {"id": 5, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "In Meetings ist mir wichtig, dass offen miteinander gesprochen wird."},
    {"id": 6, "dimension": "Leistung / Wettbewerb", "text": "Es motiviert mich, wenn gute Arbeit klar anerkannt wird."},
    {"id": 7, "dimension": "Innovation / Flexibilität", "text": "Wenn sich Pläne ändern, werde ich neugierig."},
    {"id": 8, "dimension": "Struktur / Stabilität", "text": "Ich arbeite gern, wenn Zuständigkeiten klar verteilt sind."},

    {"id": 9, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Bei Problemen suche ich zuerst den Austausch im Team."},
    {"id": 10, "dimension": "Leistung / Wettbewerb", "text": "Ich setze mir gern höhere Ziele als nötig."},
    {"id": 11, "dimension": "Innovation / Flexibilität", "text": "Zu viel Routine nimmt mir Energie bei der Arbeit."},
    {"id": 12, "dimension": "Struktur / Stabilität", "text": "Ich arbeite besser, wenn bei der Arbeit alles gut organisiert ist."},

    {"id": 13, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich fühle mich unwohl, wenn im Team jeder nur an sich denkt."},
    {"id": 14, "dimension": "Leistung / Wettbewerb", "text": "Mich mit anderen zu messen, motiviert mich."},
    {"id": 15, "dimension": "Innovation / Flexibilität", "text": "Ich blühe auf, wenn man Dinge besser machen kann."},
    {"id": 16, "dimension": "Struktur / Stabilität", "text": "Klare Regeln machen die Zusammenarbeit für mich leichter."},

    {"id": 17, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ein gutes Miteinander ist mir wichtiger als Konkurrenz im Team."},
    {"id": 18, "dimension": "Leistung / Wettbewerb", "text": "Ich möchte, dass mein beruflicher Erfolg sichtbar ist."},
    {"id": 19, "dimension": "Innovation / Flexibilität", "text": "Ich fühle mich lebendig, wenn sich bei der Arbeit viel bewegt."},
    {"id": 20, "dimension": "Struktur / Stabilität", "text": "Ich bevorzuge Planung statt ständiger Flexibilität."},

    {"id": 21, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich möchte möglichst wenig Konflikte im Arbeitsalltag."},
    {"id": 22, "dimension": "Leistung / Wettbewerb", "text": "Ein bisschen Konkurrenz bringt mich zu besseren Leistungen."},
    {"id": 23, "dimension": "Innovation / Flexibilität", "text": "Ich brauche nicht immer einen fertigen Plan, um loszulegen."},
    {"id": 24, "dimension": "Struktur / Stabilität", "text": "Ich werde unsicher, wenn Aufgaben sehr offen formuliert sind."},

    {"id": 25, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Wichtige Entscheidungen treffe ich lieber mit anderen."},
    {"id": 26, "dimension": "Leistung / Wettbewerb", "text": "Hohe Anforderungen motivieren mich mehr, als sie mich belasten."},
    {"id": 27, "dimension": "Innovation / Flexibilität", "text": "Etwas Chaos ist für mich okay, wenn daraus neue Ideen entstehen."},
    {"id": 28, "dimension": "Struktur / Stabilität", "text": "Zu viel Freiheit macht Arbeit für mich schnell unübersichtlich."},

    {"id": 29, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich arbeite gern in einem Team, in dem man aufeinander achtet."},
    {"id": 30, "dimension": "Leistung / Wettbewerb", "text": "Ich blühe dort auf, wo viel Leistung erwartet wird."},
    {"id": 31, "dimension": "Innovation / Flexibilität", "text": "Frei ausprobieren zu können ist mir wichtiger als klare Regeln."},
    {"id": 32, "dimension": "Struktur / Stabilität", "text": "Ich möchte nicht ständig Höchstleistung bringen müssen."},
]

companies = {
    "Nordlicht Care Solutions": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 5,
            "Leistung / Wettbewerb": 2,
            "Innovation / Flexibilität": 3,
            "Struktur / Stabilität": 4,
        },
        "archetype": "gemeinschaftsorientierter Arbeitgeber",
        "short_profile": "Dieses Profil steht für ein teamorientiertes Arbeitsumfeld mit viel Zusammenhalt, gegenseitiger Unterstützung und klarer Orientierung im Arbeitsalltag.",
        "description": "Nordlicht Care Solutions steht für ein stark teamorientiertes Arbeitsumfeld, in dem Zusammenhalt und gegenseitige Unterstützung eine zentrale Rolle spielen. Die Zusammenarbeit ist geprägt von Vertrauen, Wertschätzung und einem offenen Austausch auf Augenhöhe. Mitarbeitende erleben hier eine Kultur, in der man sich aufeinander verlassen kann und Erfolge gemeinsam erzielt werden. Klare Strukturen sorgen gleichzeitig für Orientierung und Stabilität im Arbeitsalltag.",
    },
    "Strive Consulting Group": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 2,
            "Leistung / Wettbewerb": 5,
            "Innovation / Flexibilität": 4,
            "Struktur / Stabilität": 3,
        },
        "archetype": "leistungsorientierter Arbeitgeber",
        "short_profile": "Dieses Profil steht für ein leistungsorientiertes Arbeitsumfeld mit ambitionierten Zielen, sichtbarer Anerkennung und hoher Eigenverantwortung.",
        "description": "Die Strive Consulting Group bietet ein leistungsorientiertes Umfeld, in dem ambitionierte Ziele und hohe Erwartungen den Arbeitsalltag prägen. Mitarbeitende werden aktiv gefordert und gefördert, ihre individuellen Stärken einzubringen und kontinuierlich weiterzuentwickeln. Erfolge werden sichtbar anerkannt und Leistung hat einen hohen Stellenwert. Gleichzeitig eröffnet das dynamische Umfeld Raum für innovative Lösungsansätze und eigenverantwortliches Arbeiten.",
    },
    "Vireon Labs": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 3,
            "Leistung / Wettbewerb": 3,
            "Innovation / Flexibilität": 5,
            "Struktur / Stabilität": 2,
        },
        "archetype": "innovationsorientierter Arbeitgeber",
        "short_profile": "Dieses Profil steht für ein innovationsorientiertes Arbeitsumfeld mit viel Offenheit, Experimentierfreude und Raum für neue Ideen.",
        "description": "Vireon Labs steht für ein kreatives und innovationsgetriebenes Arbeitsumfeld, in dem neue Ideen ausdrücklich willkommen sind. Mitarbeitende haben die Möglichkeit, aktiv an der Gestaltung von Prozessen und Lösungen mitzuwirken. Flexibilität, Offenheit und Experimentierfreude prägen die Unternehmenskultur. Feste Strukturen treten dabei bewusst in den Hintergrund, um Raum für Weiterentwicklung und neue Denkansätze zu schaffen.",
    },
    "Clarion Systems": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 3,
            "Leistung / Wettbewerb": 3,
            "Innovation / Flexibilität": 2,
            "Struktur / Stabilität": 5,
        },
        "archetype": "strukturorientierter Arbeitgeber",
        "short_profile": "Dieses Profil steht für ein strukturiertes Arbeitsumfeld mit klaren Prozessen, eindeutigen Zuständigkeiten und hoher Verlässlichkeit.",
        "description": "Clarion Systems bietet ein klar strukturiertes und verlässliches Arbeitsumfeld, in dem definierte Prozesse und eindeutige Zuständigkeiten im Mittelpunkt stehen. Mitarbeitende profitieren von stabilen Rahmenbedingungen, die Sicherheit und Planbarkeit im Arbeitsalltag ermöglichen. Die Organisation legt großen Wert auf Effizienz, Verlässlichkeit und eine klare Rollenverteilung, wodurch ein ruhiges und geordnetes Arbeitsumfeld entsteht.",
    },
}

questionnaire_items = [
    {
        "section": "A. Antworterleben",
        "prompt": "Wie hast du das Antworten erlebt?",
        "items": [
            ("q1", "Ich habe oft aus dem ersten Gefühl heraus geantwortet."),
            ("q2", "Ich habe über viele Antworten länger nachgedacht."),
            ("q3", "Bei vielen Aussagen fiel mir die Entscheidung leicht."),
            ("q4", "Ich habe genau darauf geachtet, wie ich antworte."),
            ("q5", "Bei manchen Antworten habe ich überlegt, wie sie auf andere wirken könnten."),
            ("q6", "Ich wollte mich durch meine Antworten möglichst positiv darstellen."),
        ],
    },
    {
        "section": "B. Nutzungserleben",
        "prompt": "Wie hat sich das Verfahren für dich angefühlt?",
        "items": [
            ("q7", "Die Beantwortung hat mich wenig angestrengt."),
            ("q8", "Die Art der Beantwortung fühlte sich für mich natürlich an."),
            ("q9", "Ich konnte meine Einschätzung gut über das Verfahren ausdrücken."),
            ("q10", "Das Verfahren war einfach zu bedienen."),
            ("q11", "Ich habe gut verstanden, was ich tun sollte."),
            ("q12", "Das Verfahren war unnötig kompliziert."),
        ],
    },
    {
        "section": "C. Ergebnis und Wirkung",
        "prompt": "Wie bewertest du dein Ergebnis?",
        "items": [
            ("q13", "Die Aussagen haben mich zum Nachdenken über meine Arbeitsweise gebracht."),
            ("q14", "Durch das Verfahren wurden mir eigene Arbeitspräferenzen bewusster."),
            ("q15", "Das Ergebnis fühlte sich für mich stimmig an."),
            ("q16", "Das Ergebnis wirkte auf mich glaubwürdig."),
            ("q17", "Ich würde mehr über das angezeigte Unternehmen erfahren wollen."),
            ("q18", "Ich könnte mir grundsätzlich vorstellen, mich dort zu bewerben."),
        ],
    },
]

if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())

if "condition" not in st.session_state:
    st.session_state.condition = random.choice(["swipe", "likert"])

if "phase" not in st.session_state:
    st.session_state.phase = "welcome"

if "answers" not in st.session_state:
    st.session_state.answers = []

if "questionnaire" not in st.session_state:
    st.session_state.questionnaire = {}

if "questionnaire_step" not in st.session_state:
    st.session_state.questionnaire_step = 0

if "data_saved" not in st.session_state:
    st.session_state.data_saved = False

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

if "self_assessment" not in st.session_state:
    st.session_state.self_assessment = None

if "giveaway" not in st.session_state:
    st.session_state.giveaway = {
        "participates": False,
        "email": "",
    }

if "giveaway_saved" not in st.session_state:
    st.session_state.giveaway_saved = False


def render_progress(active_step=0):
    steps = ["Präferenzen", "Ergebnis", "Einschätzung"]

    html = '<div class="study-progress">'
    html += '<div class="study-progress-label">Studienfortschritt</div>'
    html += '<div class="study-progress-track">'

    for idx, label in enumerate(steps, start=1):
        if active_step == 0:
            status = ""
            text = f"{idx}. {label}"
        elif idx < active_step:
            status = "done"
            text = f"✓ {label}"
        elif idx == active_step:
            status = "active"
            text = f"{idx}. {label}"
        else:
            status = ""
            text = f"{idx}. {label}"

        html += f'<div class="study-progress-step {status}">{text}</div>'

    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


def text_card(html_content):
    clean_html = dedent(html_content).strip()
    st.markdown(
        f'<div class="text-card">{clean_html}</div>',
        unsafe_allow_html=True,
    )


def reset_app():
    st.session_state.participant_id = str(uuid.uuid4())
    st.session_state.phase = "welcome"
    st.session_state.answers = []
    st.session_state.questionnaire = {}
    st.session_state.questionnaire_step = 0
    st.session_state.condition = random.choice(["swipe", "likert"])
    st.session_state.data_saved = False
    st.session_state.self_assessment = None
    st.session_state.giveaway = {
    "participates": False,
    "email": "",
}
    st.session_state.giveaway_saved = False

    for block in questionnaire_items:
        for key, _ in block["items"]:
            if key in st.session_state:
                del st.session_state[key]


def calculate_user_profile(answer_list):
    grouped = {}
    for answer in answer_list:
        grouped.setdefault(answer["dimension"], []).append(answer["value"])

    return {dim: round(sum(values) / len(values), 2) for dim, values in grouped.items()}


def calculate_ranking(user_profile):
    ranking = []

    for company_name, company_data in companies.items():
        company_profile = company_data["dimension_scores"]
        total_difference = sum(abs(user_profile[dim] - company_profile[dim]) for dim in user_profile)
        match_score = int(round((1 - total_difference / 16) * 100))

        ranking.append(
            {
                "company": company_name,
                "score": match_score,
                "short_profile": company_data["short_profile"],
                "differences": {dim: round(abs(user_profile[dim] - company_profile[dim]), 2) for dim in user_profile},
                "profile": company_profile,
                "archetype": company_data["archetype"],
                "description": company_data["description"],
            }
        )

    return sorted(ranking, key=lambda x: x["score"], reverse=True)


def build_export_row():
    end_time = datetime.utcnow()
    start_time = st.session_state.get("start_time")

    if start_time:
        duration_seconds = round((end_time - start_time).total_seconds(), 2)
        duration_minutes = round(duration_seconds / 60, 2)
    else:
        duration_seconds = ""
        duration_minutes = ""

    row = {
        "participant_id": st.session_state.participant_id,
        "timestamp_utc": end_time.isoformat(),
        "duration_seconds": duration_seconds,
        "duration_minutes": duration_minutes,
        "condition": st.session_state.condition,
        "self_assessment": st.session_state.self_assessment,
    }

    for item in items:
        item_id = item["id"]
        row[f"item_{item_id}_dimension"] = item["dimension"]
        row[f"item_{item_id}_text"] = item["text"]
        row[f"item_{item_id}_value"] = ""
        row[f"item_{item_id}_decision"] = ""

    for answer in st.session_state.answers:
        item_id = answer["id"]
        row[f"item_{item_id}_value"] = answer["value"]
        row[f"item_{item_id}_decision"] = answer["decision"] if answer["decision"] is not None else ""

    for block in questionnaire_items:
        for key, _ in block["items"]:
            row[key] = st.session_state.questionnaire.get(key, "")

    user_profile = calculate_user_profile(st.session_state.answers)
    ranking = calculate_ranking(user_profile)
    top_match = ranking[0]

    row["profile_zusammenarbeit"] = user_profile.get("Zusammenarbeit / Gemeinschaft", "")
    row["profile_leistung"] = user_profile.get("Leistung / Wettbewerb", "")
    row["profile_innovation"] = user_profile.get("Innovation / Flexibilität", "")
    row["profile_struktur"] = user_profile.get("Struktur / Stabilität", "")

    row["top_match_company"] = top_match["company"]
    row["top_match_score"] = top_match["score"]

    for i, entry in enumerate(ranking, start=1):
        row[f"ranking_{i}_company"] = entry["company"]
        row[f"ranking_{i}_score"] = entry["score"]

    return row


def save_response_to_csv(filepath=CSV_FILEPATH):
    row = build_export_row()
    file_exists = os.path.exists(filepath)

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def get_google_credentials():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        if "gcp_service_account" in st.secrets:
            return Credentials.from_service_account_info(
                dict(st.secrets["gcp_service_account"]),
                scopes=scope,
            )
    except Exception:
        pass

    credentials_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "credentials.json"
    )

    if os.path.exists(credentials_path):
        return Credentials.from_service_account_file(credentials_path, scopes=scope)

    return None


def save_response_to_google_sheets():
    row = build_export_row()
    creds = get_google_credentials()

    if creds is None:
        return False

    client = gspread.authorize(creds)
    worksheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

    columns = list(row.keys())
    existing_values = worksheet.get_all_values()

    if len(existing_values) == 0:
        worksheet.append_row(columns)

    ordered_values = [row[col] for col in columns]
    worksheet.append_row(ordered_values)

    return True


def save_response():
    try:
        saved_to_gsheet = save_response_to_google_sheets()

        if not saved_to_gsheet:
            save_response_to_csv(CSV_FILEPATH)

    except Exception:
        save_response_to_csv(CSV_FILEPATH)

def build_giveaway_row():
    giveaway = st.session_state.get("giveaway", {})
    email = giveaway.get("email", "").strip()

    if not giveaway.get("participates") or not email:
        return None

    return {
        "giveaway_timestamp_utc": datetime.utcnow().isoformat(),
        "giveaway_id": str(uuid.uuid4()),
        "email": email,
        "source": "cultural_fit_study",
    }


def save_giveaway_to_csv(filepath=GIVEAWAY_CSV_FILEPATH):
    row = build_giveaway_row()

    if row is None:
        return False

    file_exists = os.path.exists(filepath)

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return True


def save_giveaway_to_google_sheets():
    row = build_giveaway_row()

    if row is None:
        return False

    creds = get_google_credentials()

    if creds is None:
        return False

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    try:
        worksheet = spreadsheet.worksheet("giveaway")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title="giveaway",
            rows="1000",
            cols="10",
        )

    columns = list(row.keys())
    existing_values = worksheet.get_all_values()

    if len(existing_values) == 0:
        worksheet.append_row(columns)

    worksheet.append_row([row.get(column, "") for column in columns])
    return True


def save_giveaway_entry():
    google_saved = save_giveaway_to_google_sheets()

    if not google_saved:
        save_giveaway_to_csv()

    return True


def load_responses_df(filepath=CSV_FILEPATH):
    if not os.path.exists(filepath):
        return None
    return pd.read_csv(filepath)


def render_admin_panel():
    st.sidebar.markdown("## Admin / Daten")
    password = st.sidebar.text_input("Admin-Passwort", type="password", key="admin_password_input")
    ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "")

    if password == ADMIN_PASSWORD:
        st.session_state.admin_unlocked = True

    if st.session_state.admin_unlocked:
        st.sidebar.success("Admin-Bereich freigeschaltet")
        df = load_responses_df()

        if df is None or df.empty:
            st.sidebar.info("Noch keine gespeicherten lokalen Antworten vorhanden.")
            return

        st.sidebar.metric("Teilnahmen", len(df))
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="responses.csv herunterladen",
            data=csv_bytes,
            file_name="responses.csv",
            mime="text/csv",
        )


if SHOW_ADMIN_PANEL:
    render_admin_panel()

if DEBUG_MODE:
    if st.button("Neu starten"):
        reset_app()
        st.rerun()

st.markdown(
    """
    <style>
    /* =========================================================
       SCREEN 1: Giveaway Banner / Verlosungskarte
       ========================================================= */

    .giveaway-card {
        width: min(720px, 100%);
        margin: 1rem auto 1rem auto;
        background:
            radial-gradient(circle at top left, rgba(49,92,99,0.045), transparent 34%),
            radial-gradient(circle at bottom right, rgba(242,184,114,0.08), transparent 34%),
            rgba(255,255,255,0.97);
        border: 1px solid rgba(49,92,99,0.12);
        border-radius: 26px;
        box-shadow: 0 18px 42px rgba(49,92,99,0.10);
        padding: 1.05rem 1.15rem;
        box-sizing: border-box;
        display: grid;
        grid-template-columns: 150px minmax(0, 1fr);
        gap: 1.25rem;
        align-items: center;
    }

    .giveaway-cover-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .giveaway-cover {
        width: 132px;
        height: auto;
        display: block;
        border-radius: 8px;
        filter: drop-shadow(0 14px 24px rgba(49,92,99,0.16));
    }

    .giveaway-content {
        min-width: 0;
    }

    .giveaway-head-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.55rem;
    }

    .giveaway-icon {
        width: 42px;
        height: 42px;
        min-width: 42px;
        border-radius: 999px;
        background: rgba(242,184,114,0.18);
        border: 1px solid rgba(242,184,114,0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }

    .giveaway-title {
        color: var(--primary);
        font-size: 1.22rem;
        line-height: 1.18;
        font-weight: 850;
        letter-spacing: -0.035em;
    }

    .giveaway-text {
        color: var(--text) !important;
        font-size: 0.93rem;
        line-height: 1.48;
        margin: 0 0 0.55rem 0;
    }

    .giveaway-text strong {
        color: var(--primary);
        font-weight: 800;
    }

    .giveaway-note {
        margin-top: 0.65rem;
        padding: 0.62rem 0.75rem;
        border-radius: 16px;
        background: rgba(49,92,99,0.055);
        border: 1px solid rgba(49,92,99,0.09);
        display: flex;
        align-items: center;
        gap: 0.55rem;
        color: var(--text);
        font-size: 0.84rem;
        line-height: 1.35;
    }

    .giveaway-note-icon {
        width: 22px;
        height: 22px;
        min-width: 22px;
        border-radius: 999px;
        background: rgba(49,92,99,0.10);
        color: var(--primary);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 850;
        font-size: 0.82rem;
    }

    @media (max-width: 700px) {
        .giveaway-card {
            width: 100%;
            margin: 0.75rem auto 0.65rem auto;
            padding: 0.9rem 0.82rem;
            border-radius: 22px;
            grid-template-columns: 68px minmax(0, 1fr);
            gap: 0.78rem;
            align-items: start;
            box-shadow: 0 14px 30px rgba(49,92,99,0.09);
        }

        .giveaway-cover-wrap {
            align-self: start;
            padding-top: 0.18rem;
        }

        .giveaway-cover {
            width: 62px;
            border-radius: 7px;
            filter: drop-shadow(0 8px 16px rgba(49,92,99,0.14));
        }

        .giveaway-head-row {
            gap: 0.45rem;
            margin-bottom: 0.42rem;
        }

        .giveaway-icon {
            width: 30px;
            height: 30px;
            min-width: 30px;
            font-size: 0.95rem;
        }

        .giveaway-title {
            font-size: 1rem;
            line-height: 1.16;
            letter-spacing: -0.03em;
        }

        .giveaway-text {
            font-size: 0.8rem;
            line-height: 1.36;
            margin-bottom: 0.45rem;
        }

        .giveaway-note {
            grid-column: 1 / -1;
            margin-top: 0.35rem;
            padding: 0.56rem 0.62rem;
            border-radius: 14px;
            font-size: 0.76rem;
            line-height: 1.28;
            gap: 0.48rem;
        }

        .giveaway-note-icon {
            width: 20px;
            height: 20px;
            min-width: 20px;
            font-size: 0.74rem;
        }

        .welcome-wrap {
            padding-bottom: 0.85rem !important;
        }

        .start-button-anchor {
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
    }

    @media (max-width: 390px) {
        .giveaway-card {
            grid-template-columns: 58px minmax(0, 1fr);
            gap: 0.65rem;
            padding: 0.82rem 0.72rem;
        }

        .giveaway-cover {
            width: 54px;
        }

        .giveaway-title {
            font-size: 0.94rem;
        }

        .giveaway-text {
            font-size: 0.76rem;
        }

        .giveaway-note {
            font-size: 0.72rem;
        }
    }

    /* =========================================================
   FINAL CLEAN VERSION: Giveaway Card ohne Cover-Spalte
   ========================================================= */

.giveaway-card {
    width: min(720px, 100%) !important;
    margin: 1rem auto 1rem auto !important;
    padding: 1.25rem 1.35rem !important;
    display: block !important;
    background:
        radial-gradient(circle at top left, rgba(49,92,99,0.045), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242,184,114,0.08), transparent 34%),
        rgba(255,255,255,0.98) !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 26px !important;
    box-shadow: 0 16px 38px rgba(49,92,99,0.09) !important;
    box-sizing: border-box !important;
}

.giveaway-content {
    width: 100% !important;
    max-width: 100% !important;
}

.giveaway-head-row {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.7rem !important;
    margin-bottom: 0.75rem !important;
    text-align: center !important;
}

.giveaway-icon {
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    border-radius: 999px !important;
    background: rgba(242,184,114,0.18) !important;
    border: 1px solid rgba(242,184,114,0.35) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.15rem !important;
}

.giveaway-title {
    color: var(--primary) !important;
    font-size: 1.32rem !important;
    line-height: 1.15 !important;
    font-weight: 850 !important;
    letter-spacing: -0.035em !important;
    text-align: left !important;
}

.giveaway-text {
    max-width: 620px !important;
    margin: 0 auto 0.58rem auto !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    text-align: center !important;
}

.giveaway-text strong {
    color: var(--primary) !important;
    font-weight: 850 !important;
}

.giveaway-note {
    width: fit-content !important;
    max-width: 100% !important;
    margin: 0.85rem auto 0 auto !important;
    padding: 0.62rem 0.85rem !important;
    border-radius: 16px !important;
    background: rgba(49,92,99,0.055) !important;
    border: 1px solid rgba(49,92,99,0.09) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.55rem !important;
    color: var(--text) !important;
    font-size: 0.84rem !important;
    line-height: 1.35 !important;
    text-align: left !important;
}

.giveaway-note-icon {
    width: 22px !important;
    height: 22px !important;
    min-width: 22px !important;
    border-radius: 999px !important;
    background: rgba(49,92,99,0.10) !important;
    color: var(--primary) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 850 !important;
    font-size: 0.82rem !important;
}

@media (max-width: 700px) {
    .giveaway-card {
        width: 100% !important;
        margin: 0.75rem auto 0.75rem auto !important;
        padding: 1rem 0.9rem !important;
        border-radius: 22px !important;
        box-shadow: 0 12px 28px rgba(49,92,99,0.08) !important;
    }

    .giveaway-head-row {
        justify-content: flex-start !important;
        align-items: center !important;
        gap: 0.55rem !important;
        margin-bottom: 0.6rem !important;
        text-align: left !important;
    }

    .giveaway-icon {
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        font-size: 1rem !important;
    }

    .giveaway-title {
        font-size: 1.05rem !important;
        line-height: 1.15 !important;
        text-align: left !important;
    }

    .giveaway-text {
        max-width: 100% !important;
        font-size: 0.82rem !important;
        line-height: 1.4 !important;
        margin-bottom: 0.5rem !important;
        text-align: left !important;
    }

    .giveaway-note {
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 0.7rem !important;
        padding: 0.58rem 0.65rem !important;
        border-radius: 14px !important;
        font-size: 0.76rem !important;
        line-height: 1.3 !important;
        justify-content: flex-start !important;
    }

    .giveaway-note-icon {
        width: 20px !important;
        height: 20px !important;
        min-width: 20px !important;
        font-size: 0.74rem !important;
    }
}

@media (max-width: 390px) {
    .giveaway-card {
        padding: 0.9rem 0.78rem !important;
    }

    .giveaway-title {
        font-size: 0.98rem !important;
    }

    .giveaway-text {
        font-size: 0.78rem !important;
    }

    .giveaway-note {
        font-size: 0.72rem !important;
    }
}

/* =========================================================
   FINAL POLISH: Giveaway Card harmonischer auf Screen 1
   ========================================================= */

.giveaway-card {
    width: min(620px, 92%) !important;
    margin: 0.85rem auto 0.9rem auto !important;
    padding: 1.05rem 1.15rem !important;
    border-radius: 22px !important;
    box-shadow: 0 12px 30px rgba(49,92,99,0.075) !important;
}

.giveaway-head-row {
    justify-content: flex-start !important;
    max-width: 540px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    margin-bottom: 0.55rem !important;
}

.giveaway-icon {
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    font-size: 1rem !important;
}

.giveaway-title {
    font-size: 1.08rem !important;
    line-height: 1.16 !important;
    text-align: left !important;
}

.giveaway-text {
    max-width: 540px !important;
    text-align: left !important;
    font-size: 0.88rem !important;
    line-height: 1.45 !important;
    margin-bottom: 0.48rem !important;
}

.giveaway-note {
    max-width: 540px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    margin-top: 0.7rem !important;
    padding: 0.55rem 0.7rem !important;
    font-size: 0.78rem !important;
}

@media (max-width: 700px) {
    .giveaway-card {
        width: 100% !important;
        margin: 0.7rem auto 0.65rem auto !important;
        padding: 0.95rem 0.85rem !important;
        border-radius: 20px !important;
    }

    .giveaway-head-row {
        max-width: 100% !important;
        margin-bottom: 0.5rem !important;
    }

    .giveaway-title {
        font-size: 1rem !important;
    }

    .giveaway-text {
        max-width: 100% !important;
        font-size: 0.8rem !important;
        line-height: 1.38 !important;
        margin-bottom: 0.45rem !important;
    }

    .giveaway-note {
        max-width: 100% !important;
        font-size: 0.74rem !important;
        line-height: 1.28 !important;
        margin-top: 0.6rem !important;
    }
}

/* =========================================================
   FINAL POLISH: Giveaway Card mit kleinem Buchcover
   ========================================================= */

.giveaway-card {
    width: min(620px, 92%) !important;
    margin: 0.85rem auto 0.9rem auto !important;
    padding: 1.05rem 1.15rem !important;
    border-radius: 22px !important;
    box-shadow: 0 12px 30px rgba(49,92,99,0.075) !important;
    display: block !important;
}

.giveaway-inner {
    width: 100% !important;
    max-width: 540px !important;
    margin: 0 auto !important;
    display: grid !important;
    grid-template-columns: 72px minmax(0, 1fr) !important;
    gap: 0.95rem !important;
    align-items: center !important;
}

.giveaway-card.no-cover .giveaway-inner {
    grid-template-columns: 1fr !important;
}

.giveaway-cover-wrap {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.giveaway-cover {
    display: block !important;
    width: 66px !important;
    height: auto !important;
    border-radius: 7px !important;
    filter: drop-shadow(0 8px 16px rgba(49,92,99,0.16)) !important;
}

.giveaway-content {
    width: 100% !important;
    min-width: 0 !important;
}

.giveaway-head-row {
    display: block !important;
    margin: 0 0 0.45rem 0 !important;
    text-align: left !important;
}

.giveaway-icon {
    display: none !important;
}

.giveaway-title {
    color: var(--primary) !important;
    font-size: 1.08rem !important;
    line-height: 1.16 !important;
    font-weight: 850 !important;
    letter-spacing: -0.035em !important;
    text-align: left !important;
}

.giveaway-text {
    max-width: 100% !important;
    text-align: left !important;
    font-size: 0.88rem !important;
    line-height: 1.45 !important;
    margin: 0 0 0.48rem 0 !important;
    color: var(--text) !important;
}

.giveaway-text strong {
    color: var(--primary) !important;
    font-weight: 850 !important;
}

.giveaway-note {
    width: 100% !important;
    box-sizing: border-box !important;
    margin: 0.65rem 0 0 0 !important;
    padding: 0.55rem 0.7rem !important;
    border-radius: 15px !important;
    background: rgba(49,92,99,0.055) !important;
    border: 1px solid rgba(49,92,99,0.09) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 0.55rem !important;
    color: var(--text) !important;
    font-size: 0.78rem !important;
    line-height: 1.32 !important;
    text-align: left !important;
}

.giveaway-note-icon {
    width: 20px !important;
    height: 20px !important;
    min-width: 20px !important;
    border-radius: 999px !important;
    background: rgba(49,92,99,0.10) !important;
    color: var(--primary) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-weight: 850 !important;
    font-size: 0.72rem !important;
}

/* Mobile: Cover sehr kompakt, Text bleibt gut lesbar */
@media (max-width: 700px) {
    .giveaway-card {
        width: 100% !important;
        margin: 0.7rem auto 0.65rem auto !important;
        padding: 0.9rem 0.8rem !important;
        border-radius: 20px !important;
    }

    .giveaway-inner {
        max-width: 100% !important;
        grid-template-columns: 54px minmax(0, 1fr) !important;
        gap: 0.68rem !important;
        align-items: start !important;
    }

    .giveaway-card.no-cover .giveaway-inner {
        grid-template-columns: 1fr !important;
    }

    .giveaway-cover {
        width: 50px !important;
        border-radius: 6px !important;
        filter: drop-shadow(0 6px 12px rgba(49,92,99,0.14)) !important;
    }

    .giveaway-title {
        font-size: 0.98rem !important;
        line-height: 1.14 !important;
    }

    .giveaway-text {
        font-size: 0.78rem !important;
        line-height: 1.36 !important;
        margin-bottom: 0.42rem !important;
    }

    .giveaway-note {
        grid-column: 1 / -1 !important;
        font-size: 0.72rem !important;
        line-height: 1.28 !important;
        margin-top: 0.55rem !important;
        padding: 0.52rem 0.62rem !important;
    }
}

/* =========================================================
   ABSOLUTE FINAL FIX: Buchcover im Giveaway sichtbar machen
   ========================================================= */

.giveaway-card.has-cover .giveaway-inner {
    display: grid !important;
    grid-template-columns: 76px minmax(0, 1fr) !important;
    gap: 0.95rem !important;
    align-items: center !important;
}

.giveaway-cover-wrap {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 76px !important;
    min-width: 76px !important;
}

.giveaway-cover {
    display: block !important;
    width: 68px !important;
    height: auto !important;
    max-width: 68px !important;
    border-radius: 7px !important;
    object-fit: contain !important;
    filter: drop-shadow(0 8px 16px rgba(49,92,99,0.16)) !important;
}

.giveaway-card.no-cover .giveaway-inner {
    display: block !important;
}

@media (max-width: 700px) {
    .giveaway-card.has-cover .giveaway-inner {
        grid-template-columns: 58px minmax(0, 1fr) !important;
        gap: 0.68rem !important;
        align-items: start !important;
    }

    .giveaway-cover-wrap {
        width: 58px !important;
        min-width: 58px !important;
        padding-top: 0.1rem !important;
    }

    .giveaway-cover {
        width: 52px !important;
        max-width: 52px !important;
        border-radius: 6px !important;
    }

    .giveaway-note {
        grid-column: 1 / -1 !important;
    }
}

    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* =========================================================
       BOOK GIVEAWAY CARD V2
       Isolierte Version ohne Konflikt mit alten Giveaway-Styles
       ========================================================= */

    .book-giveaway-card-v2 {
        width: min(620px, 92%) !important;
        margin: 0.85rem auto 0.9rem auto !important;
        padding: 1.05rem 1.15rem !important;
        border-radius: 22px !important;
        background:
            radial-gradient(circle at top left, rgba(49,92,99,0.045), transparent 34%),
            radial-gradient(circle at bottom right, rgba(242,184,114,0.08), transparent 34%),
            rgba(255,255,255,0.98) !important;
        border: 1px solid rgba(49,92,99,0.12) !important;
        box-shadow: 0 12px 30px rgba(49,92,99,0.075) !important;
        box-sizing: border-box !important;
    }

    .book-giveaway-inner-v2 {
        width: 100% !important;
        max-width: 540px !important;
        margin: 0 auto !important;
        display: grid !important;
        grid-template-columns: 72px minmax(0, 1fr) !important;
        gap: 0.95rem !important;
        align-items: center !important;
    }

    .book-giveaway-card-v2.no-book-cover-v2 .book-giveaway-inner-v2 {
        grid-template-columns: 1fr !important;
    }

    .book-giveaway-cover-box-v2 {
        width: 72px !important;
        min-width: 72px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .book-giveaway-cover-v2 {
        display: block !important;
        width: 66px !important;
        max-width: 66px !important;
        height: auto !important;
        border-radius: 7px !important;
        object-fit: contain !important;
        filter: drop-shadow(0 8px 16px rgba(49,92,99,0.16)) !important;
    }

    .book-giveaway-content-v2 {
        min-width: 0 !important;
        width: 100% !important;
    }

    .book-giveaway-title-v2 {
        color: var(--primary) !important;
        font-size: 1.08rem !important;
        line-height: 1.16 !important;
        font-weight: 850 !important;
        letter-spacing: -0.035em !important;
        text-align: left !important;
        margin-bottom: 0.45rem !important;
    }

    .book-giveaway-text-v2 {
        color: var(--text) !important;
        font-size: 0.88rem !important;
        line-height: 1.45 !important;
        text-align: left !important;
        margin: 0 0 0.48rem 0 !important;
    }

    .book-giveaway-text-v2 strong {
        color: var(--primary) !important;
        font-weight: 850 !important;
    }

    .book-giveaway-note-v2 {
        width: 100% !important;
        box-sizing: border-box !important;
        margin: 0.65rem 0 0 0 !important;
        padding: 0.55rem 0.7rem !important;
        border-radius: 15px !important;
        background: rgba(49,92,99,0.055) !important;
        border: 1px solid rgba(49,92,99,0.09) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.55rem !important;
        color: var(--text) !important;
        font-size: 0.78rem !important;
        line-height: 1.32 !important;
        text-align: left !important;
    }

    .book-giveaway-note-icon-v2 {
        width: 20px !important;
        height: 20px !important;
        min-width: 20px !important;
        border-radius: 999px !important;
        background: rgba(49,92,99,0.10) !important;
        color: var(--primary) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 850 !important;
        font-size: 0.72rem !important;
    }

    @media (max-width: 700px) {
        .book-giveaway-card-v2 {
            width: 100% !important;
            margin: 0.7rem auto 0.65rem auto !important;
            padding: 0.9rem 0.8rem !important;
            border-radius: 20px !important;
        }

        .book-giveaway-inner-v2 {
            max-width: 100% !important;
            grid-template-columns: 54px minmax(0, 1fr) !important;
            gap: 0.68rem !important;
            align-items: start !important;
        }

        .book-giveaway-card-v2.no-book-cover-v2 .book-giveaway-inner-v2 {
            grid-template-columns: 1fr !important;
        }

        .book-giveaway-cover-box-v2 {
            width: 54px !important;
            min-width: 54px !important;
            padding-top: 0.1rem !important;
        }

        .book-giveaway-cover-v2 {
            width: 50px !important;
            max-width: 50px !important;
            border-radius: 6px !important;
            filter: drop-shadow(0 6px 12px rgba(49,92,99,0.14)) !important;
        }

        .book-giveaway-title-v2 {
            font-size: 0.98rem !important;
            line-height: 1.14 !important;
            margin-bottom: 0.38rem !important;
        }

        .book-giveaway-text-v2 {
            font-size: 0.78rem !important;
            line-height: 1.36 !important;
            margin-bottom: 0.42rem !important;
        }

        .book-giveaway-note-v2 {
            grid-column: 1 / -1 !important;
            font-size: 0.72rem !important;
            line-height: 1.28 !important;
            margin-top: 0.55rem !important;
            padding: 0.52rem 0.62rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* =========================================================
       BOOK GIVEAWAY NATIVE STREAMLIT VERSION
       Cleaner refined design
       ========================================================= */

    .st-key-book_giveaway_native,
    div[class*="st-key-book_giveaway_native"] {
        width: min(980px, 98%) !important;
        margin: 0.9rem auto 0.9rem auto !important;
        padding: 1.15rem 1.2rem !important;
        border-radius: 24px !important;
        background:
            radial-gradient(circle at top left, rgba(49,92,99,0.04), transparent 34%),
            radial-gradient(circle at bottom right, rgba(242,184,114,0.07), transparent 34%),
            rgba(255,255,255,0.98) !important;
        border: 1px solid rgba(49,92,99,0.10) !important;
        box-shadow: 0 10px 26px rgba(49,92,99,0.06) !important;
        box-sizing: border-box !important;
    }

    .st-key-book_giveaway_native div[data-testid="stImage"],
    div[class*="st-key-book_giveaway_native"] div[data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        align-items: flex-start !important;
        margin-top: 0.15rem !important;
    }

    .st-key-book_giveaway_native img,
    div[class*="st-key-book_giveaway_native"] img {
        border-radius: 8px !important;
        filter: drop-shadow(0 8px 16px rgba(49,92,99,0.14)) !important;
    }

    .book-native-title {
        color: var(--primary) !important;
        font-size: 1.02rem !important;
        line-height: 1.18 !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.35rem !important;
        text-align: left !important;
    }

    .book-native-text {
        color: var(--text) !important;
        font-size: 0.93rem !important;
        line-height: 1.48 !important;
        margin: 0 0 0.42rem 0 !important;
        text-align: left !important;
    }

    .book-native-text strong {
        color: var(--primary) !important;
        font-weight: 800 !important;
    }

    .book-native-note {
        width: 100% !important;
        box-sizing: border-box !important;
        margin: 0.65rem 0 0 0 !important;
        padding: 0.52rem 0.72rem !important;
        border-radius: 14px !important;
        background: rgba(49,92,99,0.045) !important;
        border: 1px solid rgba(49,92,99,0.08) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.5rem !important;
        color: var(--text) !important;
        font-size: 0.78rem !important;
        line-height: 1.3 !important;
        text-align: left !important;
    }

    .book-native-note-icon {
        width: 18px !important;
        height: 18px !important;
        min-width: 18px !important;
        border-radius: 999px !important;
        background: rgba(49,92,99,0.10) !important;
        color: var(--primary) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 800 !important;
        font-size: 0.68rem !important;
    }

    @media (max-width: 700px) {
        .st-key-book_giveaway_native,
        div[class*="st-key-book_giveaway_native"] {
            width: min(860px, 96%) !important;
            margin: 0.85rem auto 0.9rem auto !important;
            padding: 1.02rem 1.22rem 1.14rem 1.22rem !important;
            border-radius: 22px !important;
            box-shadow: 0 10px 24px rgba(49,92,99,0.06) !important;
        }

        .st-key-book_giveaway_native img,
        div[class*="st-key-book_giveaway_native"] img {
            max-width: 58px !important;
            border-radius: 7px !important;
        }

        .book-native-title {
            font-size: 0.94rem !important;
            line-height: 1.16 !important;
            margin-bottom: 0.28rem !important;
        }

        .book-native-text {
            font-size: 0.79rem !important;
            line-height: 1.38 !important;
            margin-bottom: 0.36rem !important;
        }

        .book-native-note {
            font-size: 0.71rem !important;
            line-height: 1.26 !important;
            margin-top: 0.5rem !important;
            padding: 0.48rem 0.58rem !important;
            border-radius: 12px !important;
        }

        .book-native-note-icon {
            width: 17px !important;
            height: 17px !important;
            min-width: 17px !important;
            font-size: 0.65rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* =========================================================
       ABSOLUTE FINAL: Book Giveaway Banner
       Überschrift luftiger + Feld etwas höher/länger
       ========================================================= */

    .st-key-book_giveaway_native,
    div[class*="st-key-book_giveaway_native"] {
        width: min(980px, 98%) !important;
        margin: 0.9rem auto 0.45rem auto !important;
        padding: 1.08rem 1.35rem 1.75rem 1.35rem !important;
        border-radius: 24px !important;
        background:
            radial-gradient(circle at top left, rgba(49,92,99,0.04), transparent 34%),
            radial-gradient(circle at bottom right, rgba(242,184,114,0.07), transparent 34%),
            rgba(255,255,255,0.985) !important;
        border: 1px solid rgba(49,92,99,0.10) !important;
        box-shadow: 0 10px 26px rgba(49,92,99,0.06) !important;
        box-sizing: border-box !important;
    }

    .st-key-book_giveaway_native div[data-testid="column"],
    div[class*="st-key-book_giveaway_native"] div[data-testid="column"] {
        display: flex !important;
        align-items: center !important;
    }

    .st-key-book_giveaway_native div[data-testid="stImage"],
    div[class*="st-key-book_giveaway_native"] div[data-testid="stImage"] {
        margin-top: 0 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    .st-key-book_giveaway_native img,
    div[class*="st-key-book_giveaway_native"] img {
        max-width: 125px !important;
        border-radius: 8px !important;
        filter: drop-shadow(0 7px 14px rgba(49,92,99,0.13)) !important;
    }

    .book-native-title {
        color: #315C63 !important;
        font-size: 1.14rem !important;
        line-height: 1.18 !important;
        font-weight: 850 !important;
        letter-spacing: -0.015em !important;
        margin-bottom: 0.72rem !important;
        text-align: left !important;
    }

    .book-native-text {
        color: #2B2B2B !important;
        font-size: 0.91rem !important;
        line-height: 1.42 !important;
        margin: 0 0 0.36rem 0 !important;
        text-align: left !important;
    }

    .book-native-text strong {
        color: #315C63 !important;
        font-weight: 850 !important;
    }

    .book-native-note {
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 0.72rem !important;
        padding: 0.55rem 0.8rem !important;
        border-radius: 14px !important;
        background: rgba(49,92,99,0.045) !important;
        border: 1px solid rgba(49,92,99,0.10) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.55rem !important;
        color: #2B2B2B !important;
        font-size: 0.74rem !important;
        line-height: 1.28 !important;
        text-align: left !important;
        font-weight: 700 !important;
    }

    .book-native-note-icon {
        width: 18px !important;
        height: 18px !important;
        min-width: 18px !important;
        border-radius: 999px !important;
        background: rgba(49,92,99,0.10) !important;
        color: #315C63 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 700 !important;
        font-size: 0.60rem !important;
    }

    @media (max-width: 700px) {
        .st-key-book_giveaway_native,
        div[class*="st-key-book_giveaway_native"] {
            width: 100% !important;
            margin: 0.75rem auto 0.85rem auto !important;
            padding: 0.92rem 0.82rem 1.05rem 0.82rem !important;
            border-radius: 20px !important;
        }

        .st-key-book_giveaway_native img,
        div[class*="st-key-book_giveaway_native"] img {
            max-width: 58px !important;
            border-radius: 7px !important;
        }

        .book-native-title {
            font-size: 0.98rem !important;
            line-height: 1.16 !important;
            margin-bottom: 0.5rem !important;
        }

        .book-native-text {
            font-size: 0.77rem !important;
            line-height: 1.34 !important;
            margin-bottom: 0.36rem !important;
        }

        .book-native-note {
            margin-top: 0.58rem !important;
            padding: 0.5rem 0.58rem !important;
            font-size: 0.60rem !important;
            line-height: 1.25 !important;
            border-radius: 12px !important;
        }

        .book-native-note-icon {
            width: 17px !important;
            height: 17px !important;
            min-width: 17px !important;
            font-size: 0.55rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* =========================================================
       FINAL FIX: Abstand Buchbanner zu Weiter-Button reduzieren
       ========================================================= */

    .start-button-anchor {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .st-key-welcome_button_area,
    div[class*="st-key-welcome_button_area"] {
        margin-top: -1.45rem !important;
        padding-top: 0 !important;
    }

    .st-key-welcome_button_area .stButton,
    div[class*="st-key-welcome_button_area"] .stButton {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    .st-key-welcome_button_area .stButton > button,
    div[class*="st-key-welcome_button_area"] .stButton > button {
        margin-top: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.session_state.phase == "welcome":
    st.markdown(
        """
        <div class="welcome-wrap">
            <div class="welcome-card">
                <div class="hero-title">Finde heraus, welches Arbeitsumfeld zu dir passt</div>
                <div class="hero-subtitle">
                    Stell dir vor, du suchst nicht einfach irgendeinen Job, sondern ein Arbeitsumfeld, das wirklich zu dir passt: ein Umfeld, in dem du dich wohlfühlst, gut arbeiten kannst und deine Art zu arbeiten ernst genommen wird.
                    <br><br>
                    Denn zwei Jobs können auf dem Papier ähnlich wirken, sich im Arbeitsalltag aber ganz unterschiedlich anfühlen. Oft liegt der Unterschied darin, wie Menschen zusammenarbeiten, wie viel Freiheit man hat, wie Leistung bewertet wird oder wie klar Strukturen sind.
                    <br><br>
                    In dieser Studie geht es um genau diese Unterschiede.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="book_giveaway_native"):
        book_col, text_col = st.columns([0.14, 0.86], gap="medium")

        with book_col:
            if os.path.exists(BOOK_COVER_PATH):
                st.image(BOOK_COVER_PATH, width=125)

        with text_col:
            st.markdown(
                """
                <div class="book-native-title">Deine Teilnahme kann sich doppelt lohnen</div>

                <div class="book-native-text">
                    Finde heraus, welches Arbeitsumfeld zu dir passt — und sichere dir die Chance auf eines von fünf Exemplaren von
                    <strong>„Crashkurs People, Culture &amp; Change“</strong>.
                </div>

                <div class="book-native-text">
                    Das Buch zeigt kompakt und praxisnah, wie moderne Transformation im Bereich People &amp; Culture verstanden,
                    gestaltet und mit konkreten Tools umgesetzt werden kann.
                </div>

                <div class="book-native-note">
                    <span class="book-native-note-icon">i</span>
                    <span>Die Teilnahme an der Verlosung ist am Ende der Studie freiwillig möglich.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="start-button-anchor"></div>', unsafe_allow_html=True)

    with st.container(key="welcome_button_area"):
        left, center, right = st.columns([1.7, 1.0, 1.7])
        with center:
            if st.button("Weiter", use_container_width=True):
                st.session_state.phase = "consent"
                st.rerun()

elif st.session_state.phase == "consent":
    consent_html = (
        '<div class="screen-fade consent-screen-copy">'
        '<div class="hero-title">Kurz zur Studie</div>'
        '<div class="hero-subtitle">Bevor es losgeht, erhältst du die wichtigsten Informationen zur Teilnahme.</div>'

        '<p>Gleich geht es los. Du bewertest kurze Aussagen zu Arbeitsumfeldern. Es geht zum Beispiel um Teamarbeit, Leistung, Veränderung und klare Strukturen.</p>'
        '<p>Es gibt keine richtigen oder falschen Antworten. Wichtig ist nur, was zu dir passt.</p>'

        '<div class="info-grid">'
        '<div class="info-box"><strong>Dauer</strong><span>ca. 8–10 Minuten</span></div>'
        '<div class="info-box"><strong>Anonym</strong><span>Ohne Personendaten</span></div>'
        '<div class="info-box"><strong>Freiwillig</strong><span>Abbruch jederzeit möglich</span></div>'
        '</div>'

        '<p>Deine Angaben werden <strong>anonym</strong> gespeichert und nur für diese Masterarbeit ausgewertet. Die Teilnahme ist <strong>freiwillig</strong>. Du kannst die Studie jederzeit abbrechen, ohne dass dir dadurch Nachteile entstehen.</p>'
        '<p>Wenn du die Checkbox aktivierst und auf „Studie beginnen“ klickst, stimmst du der Teilnahme zu.</p>'
        '</div>'
    )

    with st.container(key="consent_integrated_card"):
        st.markdown(consent_html, unsafe_allow_html=True)

        st.markdown('<div class="consent-divider"></div>', unsafe_allow_html=True)

        with st.container(key="consent_inline_box"):
            consent = st.checkbox(
                "Ich stimme der Teilnahme an dieser Studie zu.",
                key="consent_checkbox_unique",
            )

            if st.button(
                "Studie beginnen",
                key="start_after_consent_unique",
                use_container_width=True,
                disabled=not consent,
            ):
                st.session_state.start_time = datetime.utcnow()
                st.session_state.phase = "instructions"
                st.rerun()

        st.markdown(
            '<p class="consent-contact">'
            '<strong>Bei Fragen kannst du mich kontaktieren:</strong><br>'
            'Niklas Demtröder - niklas.demtroeder@iu-study.org'
            '</p>',
            unsafe_allow_html=True,
        )

elif st.session_state.phase == "instructions":
    render_progress(0)

    st.markdown(
    '<div class="hero-title" style="text-align:center; margin-bottom:1.4rem;">So funktioniert die Bewertung</div>',
    unsafe_allow_html=True,
)

    if st.session_state.condition == "swipe":
        text_card(
    """
    <h3><strong>Deine Aufgabe</strong></h3>
    <p>Du siehst gleich kurze Aussagen zu Arbeitsumfeldern. Entscheide bei jeder Aussage spontan, ob sie zu dir passt.</p>

    <div class="instruction-row">
        <div class="instruction-box"><strong>← Nach links wischen</strong><span>passt nicht zu mir</span></div>
        <div class="instruction-box"><strong>Nach rechts wischen →</strong><span>passt zu mir</span></div>
    </div>

    <p>Nutze am besten dein erstes Gefühl. Es gibt keine richtigen oder falschen Antworten.</p>
    """
)
    else:
        text_card(
    """
    <h3><strong>Deine Aufgabe</strong></h3>
    <p>Du siehst gleich kurze Aussagen zu Arbeitsumfeldern. Entscheide bei jeder Aussage spontan auf einer Skala von 1 bis 5, wie gut sie zu dir passt.</p>

    <div class="instruction-row">
        <div class="instruction-box"><strong>1</strong><span>passt nicht zu mir</span></div>
        <div class="instruction-box"><strong>5</strong><span>passt zu mir</span></div>
    </div>

    <p>Nutze am besten dein erstes Gefühl. Es gibt keine richtigen oder falschen Antworten.</p>
    """
)

    left, center, right = st.columns([1.55, 1.0, 1.55])
    with center:
        if st.button("Bewertung starten", use_container_width=True):
            st.session_state.phase = "assessment"
            st.rerun()

elif st.session_state.phase == "assessment":
    render_progress(1)

    st.markdown(
        '<div class="hero-title" style="text-align:center;">Cultural Fit Matcher</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.condition == "swipe":
        st.markdown(
            """
            <div class="assessment-help">
                Wische die Karte nach links oder rechts – je nachdem, ob die Aussage zu dir passt.
            </div>
            """,
            unsafe_allow_html=True,
        )
        result = swipe_component(items=items, mode="swipe", key="swipe_full_assessment")
    else:
        st.markdown(
            """
            <div class="assessment-help">
                Bewerte auf einer Skala von 1 bis 5, wie gut die Aussage zu dir passt.
            </div>
            """,
            unsafe_allow_html=True,
        )
        result = swipe_component(items=items, mode="likert", key="likert_full_assessment")

    if isinstance(result, dict) and result.get("completed") is True:
        st.session_state.answers = result.get("answers", [])
        st.session_state.phase = "results"
        st.rerun()

elif st.session_state.phase == "results":
    render_progress(2)

    user_profile = calculate_user_profile(st.session_state.answers)
    ranking = calculate_ranking(user_profile)
    top_match = ranking[0]

    sorted_dims = sorted(top_match["differences"].items(), key=lambda x: x[1])
    best_dims = [d[0] for d in sorted_dims[:2]]
    best_dims_html = "".join([f"<li>{escape(dim)}</li>" for dim in best_dims])

    st.markdown('<div class="hero-title">Dein Ergebnis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Auf Basis deiner Antworten wurde ein fiktives Unternehmensprofil mit der höchsten berechneten Übereinstimmung ermittelt.</div>',
        unsafe_allow_html=True,
    )

    result_hero_html = (
        '<div class="result-hero-card">'
        '<div class="result-kicker">Höchste berechnete Übereinstimmung</div>'
        f'<div class="result-company">{escape(top_match["company"])}</div>'
        '<div class="result-score-row">'
        f'<div class="result-score">{top_match["score"]} %</div>'
        '<div class="result-score-label">berechnete kulturelle Übereinstimmung</div>'
        '</div>'
        f'<p class="result-profile-text">{escape(top_match["short_profile"])}</p>'
'<p class="result-method-text">Dieses Ergebnis basiert auf dem Vergleich deiner Antworten mit einem hinterlegten, fiktiven Unternehmensprofil.</p>'
        '<div class="result-meta-row">'
        '</div>'
        '</div>'
    )

    st.markdown(result_hero_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="result-next-note">
            Bitte gib nun deine erste Einschätzung zum Ergebnis ab. Danach folgt ein kurzer Abschlussfragebogen von etwa 1–2 Minuten.
        </div>
        """,
        unsafe_allow_html=True,
    )

    assessment_result = swipe_component(
        items=[],
        mode="result_assessment",
        key="result_assessment_component",
    )

    if isinstance(assessment_result, dict) and assessment_result.get("completed") is True:
        st.session_state.self_assessment = assessment_result.get("value")
        st.session_state.phase = "pre_questionnaire"
        st.rerun()

    st.markdown('<div class="result-details-title">Mehr zum Ergebnis anzeigen</div>', unsafe_allow_html=True)

    with st.expander("Warum dieses Ergebnis?"):
        st.markdown(
            f"""
            Deine Antworten wurden mit dem Kulturprofil des angezeigten Unternehmens verglichen.
            Die höchste Übereinstimmung mit diesem Profil zeigt sich vor allem in:

            <ul>{best_dims_html}</ul>

            In diesen Bereichen liegen deine angegebenen Präferenzen besonders nah am dargestellten Unternehmensprofil.
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Über dieses Unternehmen"):
        st.markdown(
            f"""
            Bei dem folgenden Unternehmensprofil handelt es sich um ein fiktives Beispielunternehmen,
            das eine bestimmte Unternehmenskultur repräsentiert.

            <br><br>

            {escape(top_match["description"])}
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Weitere mögliche Matches"):
        for i, entry in enumerate(ranking[1:], start=2):
            st.markdown(
                f"""
                <div class="ranking-card">
                    <strong>{i}. {escape(entry['company'])}</strong><br>
                    <span class="custom-muted">{entry['score']} % Übereinstimmung · {escape(entry['archetype'])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("Wie wurde das Ergebnis berechnet?"):
        st.write(
            "Deine Antworten wurden zu vier Kulturdimensionen zusammengefasst und mit den "
            "hinterlegten Kulturprofilen der fiktiven Unternehmen verglichen. Je geringer die "
            "Abweichung zwischen deinem Antwortprofil und einem Unternehmensprofil, desto höher "
            "ist die angezeigte berechnete Übereinstimmung."
        )

elif st.session_state.phase == "pre_questionnaire":
    render_progress(3)

    st.markdown(
        '<div class="hero-title" style="text-align:center; margin-bottom:0.45rem;">Deine Einschätzung zum Verfahren</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle" style="text-align:center; margin-bottom:1.4rem;">Im letzten Teil geht es darum, wie du das Verfahren erlebt hast.</div>',
        unsafe_allow_html=True,
    )

    pre_questionnaire_html = (
        '<div class="pre-questionnaire-clean-wrap screen-fade">'
        '<div class="screen-card-info">'
        '<p>Bitte bewerte im folgenden kurzen Fragebogen, wie du die Bearbeitung, das Ergebnis und die Darstellung des Verfahrens erlebt hast.</p>'
        '<div class="info-grid">'
        '<div class="info-box"><strong>Dauer</strong><span>ca. 1–2 Minuten</span></div>'
        '<div class="info-box"><strong>Bewertung</strong><span>Keine richtigen oder falschen Antworten</span></div>'
        '<div class="info-box"><strong>Anonym</strong><span>Auswertung nur für die Masterarbeit</span></div>'
        '</div>'
        '<p>Antworte auch hier möglichst ehrlich und spontan.</p>'
        '</div>'
        '</div>'
    )

    st.markdown(pre_questionnaire_html, unsafe_allow_html=True)

    left, center, right = st.columns([1.55, 1.0, 1.55])
    with center:
        if st.button("Einschätzung starten", use_container_width=True):
            st.session_state.phase = "questionnaire"
            st.session_state.questionnaire_step = 0
            st.rerun()

elif st.session_state.phase == "questionnaire":
    questionnaire_payload = [
        {
            **block,
            "cover_b64": image_to_base64(BOOK_COVER_PATH),
        }
        for block in questionnaire_items
    ]

    result = swipe_component(
        items=questionnaire_payload,
        mode="closing_questionnaire",
        key="closing_questionnaire_component",
    )

    if isinstance(result, dict) and result.get("completed") is True:
        st.session_state.questionnaire = result.get("answers", {})
        st.session_state.giveaway = {
            "participates": bool(result.get("giveaway_participation", False)),
            "email": result.get("giveaway_email", "").strip(),
        }
        st.session_state.phase = "end"
        st.rerun()

elif st.session_state.phase == "end":
    if not st.session_state.data_saved:
        save_response()
        st.session_state.data_saved = True

    if not st.session_state.giveaway_saved:
        save_giveaway_entry()
        st.session_state.giveaway_saved = True

    st.markdown(
        """
        <div class="thanks-wrap screen-fade">
            <div class="thanks-card">
                <div class="thanks-icon">✓</div>
                <div class="thanks-title">Vielen Dank für deine Teilnahme</div>
                <div class="thanks-text">
                    Deine Antworten wurden erfolgreich gespeichert.
                    <br>
                    Du kannst das Browserfenster nun schließen.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )