# app.py
# Wichtig:
# DEBUG_MODE vor echter Erhebung auf False lassen.
# credentials.json nicht auf GitHub hochladen.

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
    </style>
    """,
    unsafe_allow_html=True,
)

SHOW_ADMIN_PANEL = False
CSV_FILEPATH = "responses.csv"
DEBUG_MODE = False

GOOGLE_SHEET_ID = "1F43LmzUGQRqwCpcHsuAMMEEV6xB95FVXa8nVzMDD-rE"

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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.45rem;
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

.result-assessment-inner p {
    margin-bottom: 1rem;
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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.45rem;
}

.result-assessment-inner p {
    margin-bottom: 0.9rem;
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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.35rem;
}

.result-assessment-inner p {
    margin-top: 0;
    margin-bottom: 0.75rem;
    color: var(--text) !important;
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

    .thanks-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.4rem;
        box-shadow: 0 18px 40px rgba(49,92,99,0.11);
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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.35rem;
}

.result-assessment-inner p {
    margin-top: 0;
    margin-bottom: 0.8rem;
    color: var(--text) !important;
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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.35rem;
}

.result-assessment-inner p {
    margin-top: 0;
    margin-bottom: 0.8rem;
    color: var(--text) !important;
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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem !important;
    font-weight: 850 !important;
    letter-spacing: -0.03em !important;
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}

.result-assessment-inner p {
    margin-top: 0 !important;
    margin-bottom: 0.8rem !important;
    color: var(--text) !important;
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

/* FINAL: Einschätzungskarte über Streamlit-Key stylen */
.st-key-result_assessment_card,
div[class*="st-key-result_assessment_card"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid rgba(49,92,99,0.12) !important;
    border-radius: 28px !important;
    box-shadow: 0 18px 42px rgba(49,92,99,0.10) !important;
    padding: 1.25rem 1.45rem 1.15rem 1.45rem !important;
    margin-top: 0.35rem !important;
    margin-bottom: 1.35rem !important;
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

.result-assessment-inner h3 {
    color: var(--primary) !important;
    font-size: 1.65rem !important;
    font-weight: 850 !important;
    letter-spacing: -0.03em !important;
    margin-top: 0 !important;
    margin-bottom: 0.35rem !important;
}

.result-assessment-inner p {
    margin-top: 0 !important;
    margin-bottom: 0.8rem !important;
    color: var(--text) !important;
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

.st-key-result_assessment_card input[type="radio"],
div[class*="st-key-result_assessment_card"] input[type="radio"] {
    appearance: auto !important;
    -webkit-appearance: radio !important;
    accent-color: var(--success) !important;
    width: 16px !important;
    height: 16px !important;
    opacity: 1 !important;
    display: inline-block !important;
    visibility: visible !important;
    margin-right: 0.45rem !important;
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
    font-size: 1.2rem !important;
    line-height: 1.55 !important;
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

    </style>
    """,
    unsafe_allow_html=True,
)

items = [
    {"id": 1, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Mir ist ein unterstützendes Miteinander im Team wichtig."},

    {"id": 2, "dimension": "Leistung / Wettbewerb", "text": "Klare Ziele und hohe Erwartungen motivieren mich."},

    {"id": 3, "dimension": "Innovation / Flexibilität", "text": "Ich bevorzuge ein Arbeitsumfeld, in dem neue Ideen willkommen sind."},

    {"id": 4, "dimension": "Struktur / Stabilität", "text": "Klare Prozesse und feste Abläufe geben mir Sicherheit."},

    {"id": 5, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ein gutes Arbeitsklima ist mir wichtiger als interner Wettbewerb."},

    {"id": 6, "dimension": "Leistung / Wettbewerb", "text": "Ein gewisser Wettbewerb im Arbeitsalltag spornt mich an."},

    {"id": 7, "dimension": "Innovation / Flexibilität", "text": "Zu viel Routine im Arbeitsalltag empfinde ich als einschränkend."},

    {"id": 8, "dimension": "Struktur / Stabilität", "text": "Ich bevorzuge ein gut organisiertes Arbeitsumfeld."},

    {"id": 9, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Mir ist wichtig, dass im Team offen miteinander kommuniziert wird."},

    {"id": 10, "dimension": "Leistung / Wettbewerb", "text": "Sichtbarer beruflicher Erfolg ist für mich ein wichtiger Antrieb."},

    {"id": 11, "dimension": "Innovation / Flexibilität", "text": "Ich mag es, wenn Dinge ausprobiert und weiterentwickelt werden."},

    {"id": 12, "dimension": "Struktur / Stabilität", "text": "Ein vorhersehbarer Arbeitsalltag ist mir wichtiger als maximale Flexibilität."},

    {"id": 13, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich arbeite lieber in kooperativen als in stark konkurrenzorientierten Teams."},

    {"id": 14, "dimension": "Leistung / Wettbewerb", "text": "Ich arbeite gerne in einem Umfeld, in dem Leistung sichtbar anerkannt wird."},

    {"id": 15, "dimension": "Innovation / Flexibilität", "text": "Veränderung im Arbeitsalltag empfinde ich eher als spannend als belastend."},

    {"id": 16, "dimension": "Struktur / Stabilität", "text": "Feste Strukturen helfen mir dabei, effizient zu arbeiten."},

    {"id": 17, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Mir ist ein harmonisches Teamklima wichtiger als persönliche Karrierechancen."},

    {"id": 18, "dimension": "Leistung / Wettbewerb", "text": "Ich möchte beruflich möglichst erfolgreich sein."},

    {"id": 19, "dimension": "Innovation / Flexibilität", "text": "Ich fühle mich in dynamischen Arbeitsumfeldern wohler als in stark routinierten."},

    {"id": 20, "dimension": "Struktur / Stabilität", "text": "Ich schätze Arbeitsumfelder, in denen Verantwortlichkeiten klar verteilt sind."},

    {"id": 21, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich arbeite am liebsten in einem Umfeld, in dem Zusammenhalt spürbar ist."},

    {"id": 22, "dimension": "Leistung / Wettbewerb", "text": "Hohe Leistungsanforderungen empfinde ich eher als motivierend als belastend."},

    {"id": 23, "dimension": "Innovation / Flexibilität", "text": "Ich nehme unklare Abläufe in Kauf, wenn dadurch mehr Raum für neue Ideen entsteht."},

    {"id": 24, "dimension": "Struktur / Stabilität", "text": "Ich arbeite gerne in einem Umfeld mit eindeutigen Regeln und Zuständigkeiten."},

    {"id": 25, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich lege Wert darauf, dass Kolleginnen und Kollegen sich gegenseitig unterstützen."},

    {"id": 26, "dimension": "Leistung / Wettbewerb", "text": "Ich finde es motivierend, wenn Kolleginnen und Kollegen um die besten Ergebnisse konkurrieren."},

    {"id": 27, "dimension": "Innovation / Flexibilität", "text": "Ich nehme organisatorisches Chaos in Kauf, wenn dadurch Innovation möglich wird."},

    {"id": 28, "dimension": "Struktur / Stabilität", "text": "Zu viel Freiheit im Arbeitsalltag kann die Zusammenarbeit erschweren."},

    {"id": 29, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich arbeite lieber in einem harmonischen Team als in einem leistungsstarken Team mit vielen Konflikten."},

    {"id": 30, "dimension": "Leistung / Wettbewerb", "text": "Karrierechancen sind mir wichtiger als ein besonders familiäres Arbeitsumfeld."},

    {"id": 31, "dimension": "Innovation / Flexibilität", "text": "Klare Regeln sind für mich weniger wichtig als kreative Freiheit."},

    {"id": 32, "dimension": "Struktur / Stabilität", "text": "Ich arbeite lieber nach klaren Vorgaben als völlig eigenständig."},
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
        "section": "A. Dein Antwortgefühl",
        "items": [
            ("q1", "Ich habe mich bei meinen Antworten stark auf mein erstes Gefühl verlassen."),
            ("q2", "Ich habe lange über meine Antworten nachgedacht."),
            ("q3", "Die Beantwortung fiel mir eher intuitiv als analytisch."),
            ("q4", "Ich musste meine Antworten stark abwägen."),
        ],
    },
    {
        "section": "B. Bewusste Antwortsteuerung",
        "items": [
            ("q5", "Ich habe meine Antworten bewusst gesteuert."),
            ("q6", "Ich habe während der Bearbeitung stark darauf geachtet, wie ich antworte."),
        ],
    },
    {
        "section": "C. Wirkung der eigenen Antworten",
        "items": [
            ("q7", "Ich habe darauf geachtet, mit meinen Antworten einen möglichst positiven Eindruck zu vermitteln."),
            ("q8", "Bei meinen Antworten war mir wichtig, wie diese auf andere wirken könnten."),
            ("q9", "Ich habe eher so geantwortet, wie es gesellschaftlich erwünscht oder positiv bewertet wird."),
            ("q10", "Ich habe versucht, mich durch meine Antworten möglichst vorteilhaft darzustellen."),
        ],
    },
    {
        "section": "D. Bedienung und Verständlichkeit",
        "items": [
            ("q11", "Das Verfahren war einfach zu bedienen."),
            ("q12", "Die Bearbeitung war für mich verständlich und nachvollziehbar."),
            ("q13", "Ich fand die Beantwortung insgesamt angenehm."),
            ("q14", "Das Verfahren wirkte auf mich unnötig kompliziert."),
        ],
    },
    {
        "section": "E. Einschätzung des Ergebnisses",
        "items": [
            ("q15", "Das angezeigte Ergebnis passt gut zu mir."),
            ("q16", "Das Ergebnis wirkt auf mich plausibel."),
            ("q17", "Ich kann gut nachvollziehen, warum mir dieses Unternehmen als bestes Match angezeigt wurde."),
        ],
    },
    {
        "section": "F. Interesse am Unternehmen",
        "items": [
            ("q18", "Ich würde mich näher über das angezeigte Unternehmen informieren."),
            ("q19", "Ich könnte mir vorstellen, die Karriereseite des angezeigten Unternehmens anzusehen."),
            ("q20", "Ich könnte mir grundsätzlich vorstellen, mich bei diesem Unternehmen zu bewerben."),
        ],
    },
    {
        "section": "G. Gesamtbewertung",
        "items": [
            ("q21", "Insgesamt halte ich dieses Verfahren für eine sinnvolle Möglichkeit, kulturelle Passung im Recruiting sichtbar zu machen."),
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


def load_responses_df(filepath=CSV_FILEPATH):
    if not os.path.exists(filepath):
        return None
    return pd.read_csv(filepath)


def render_admin_panel():
    st.sidebar.markdown("## Admin / Daten")
    password = st.sidebar.text_input("Admin-Passwort", type="password", key="admin_password_input")
    ADMIN_PASSWORD = "Flietzpiepe11!"

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

    st.markdown('<div class="start-button-anchor"></div>', unsafe_allow_html=True)

    left, center, right = st.columns([1.45, 1.25, 1.45])
    with center:
        if st.button("Weiter", use_container_width=True):
            st.session_state.phase = "consent"
            st.rerun()

elif st.session_state.phase == "consent":
    consent_html = (
        '<div class="screen-frame-soft screen-fade">'
        '<div class="screen-card-info">'
        '<div class="hero-title">Kurz zur Studie</div>'
        '<div class="hero-subtitle">Bevor es losgeht, erhältst du die wichtigsten Informationen zur Teilnahme.</div>'
        '<p>Gleich geht es los. Du bewertest kurze Aussagen zu Arbeitsumfeldern. Es geht zum Beispiel um Teamarbeit, Leistung, Veränderung und klare Strukturen.</p>'
        '<p>Es gibt keine richtigen oder falschen Antworten. Wichtig ist nur, was zu dir passt.</p>'
        '<div class="info-grid">'
        '<div class="info-box"><strong>Dauer</strong><span>ca. 8–10 Minuten</span></div>'
        '<div class="info-box"><strong>Anonym</strong><span>Keine personenbezogenen Daten</span></div>'
        '<div class="info-box"><strong>Freiwillig</strong><span>Abbruch jederzeit möglich</span></div>'
        '</div>'
        '<p>Deine Angaben werden <strong>anonym</strong> gespeichert und nur für diese Masterarbeit ausgewertet. Die Teilnahme ist <strong>freiwillig</strong>. Du kannst die Studie jederzeit abbrechen, ohne dass dir dadurch Nachteile entstehen.</p>'
        '<p>Wenn du die Checkbox unten aktivierst und auf „Studie beginnen“ klickst, stimmst du der Teilnahme zu.</p>'
        '<p><strong>Bei Fragen kannst du mich kontaktieren:</strong><br>'
        'Niklas Demtröder - niklas.demtroeder@iu-study.org</p>'
        '</div>'
        '</div>'
    )

    st.markdown(consent_html, unsafe_allow_html=True)

    st.markdown('<div class="consent-spacing"></div>', unsafe_allow_html=True)

    with st.container(key="consent_action_area"):
        left, center, right = st.columns([1.0, 2.2, 1.0])

    with center:
        consent = st.checkbox(
            "Ich stimme der Teilnahme an der Studie zu.",
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

    left, center, right = st.columns([1.2, 1.4, 1.2])
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
                Wische nach links oder rechts – je nachdem, ob die Aussage zu dir passt.
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
        '<div class="result-pill">Fiktives Unternehmensprofil</div>'
        f'<div class="result-pill">{escape(top_match["archetype"])}</div>'
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

    left, card_col, right = st.columns([0.025, 0.90, 0.025])

    with card_col:
        with st.container(key="result_assessment_card"):
            st.markdown(
                """
                <div class="result-assessment-inner">
                    <h3>Deine erste Einschätzung</h3>
                    <p>Wie passend erscheint dir das angezeigte Ergebnis?</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            self_assessment = st.radio(
                "Bitte wähle eine Antwort aus:",
                options=[
                    "Sehr passend",
                    "Eher passend",
                    "Teils / teils",
                    "Eher nicht passend",
                    "Gar nicht passend",
                ],
                index=None,
                key="result_self_assessment",
                label_visibility="collapsed",
            )

            btn_left, btn_center, btn_right = st.columns([0.01, 0.70, 0.01])
            with btn_center:
                if st.button(
                    "Zum Abschlussfragebogen",
                    use_container_width=True,
                    disabled=self_assessment is None,
                    key="continue_to_questionnaire",
                ):
                    st.session_state.self_assessment = self_assessment
                    st.session_state.phase = "pre_questionnaire"
                    st.rerun()

            if self_assessment is None:
                st.markdown(
                    '<div class="result-assessment-hint">Bitte wähle eine Einschätzung aus, um fortzufahren.</div>',
                    unsafe_allow_html=True,
                )

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
        '<div class="screen-frame-soft screen-fade">'
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

    left, center, right = st.columns([1.25, 1.5, 1.25])
    with center:
        if st.button("Einschätzung starten", use_container_width=True):
            st.session_state.phase = "questionnaire"
            st.session_state.questionnaire_step = 0
            st.rerun()

elif st.session_state.phase == "questionnaire":
    render_progress(3)

    current_step = st.session_state.questionnaire_step
    current_block = questionnaire_items[current_step]
    total_blocks = len(questionnaire_items)

    progress_percent = round(((current_step + 1) / total_blocks) * 100, 1)

    st.markdown(
        '<div class="questionnaire-title">Deine Einschätzung</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="questionnaire-subtitle">Abschnitt {current_step + 1} von {total_blocks}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="questionnaire-progress-wrap">
            <div class="questionnaire-progress-track">
                <div class="questionnaire-progress-fill" style="width: {progress_percent}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_text = current_block["section"]
    if ". " in section_text:
        section_letter, section_title = section_text.split(". ", 1)
    else:
        section_letter = f"{current_step + 1}"
        section_title = section_text

    questionnaire_section_html = (
    '<div class="questionnaire-section-card">'
    f'<div class="questionnaire-section-label">Abschnitt {escape(section_letter)}</div>'
    f'<div class="questionnaire-section-title">{escape(section_title)}</div>'
    '<p class="questionnaire-section-helper">Bitte bewerte die folgenden Aussagen danach, wie sehr du ihnen zustimmst.</p>'
    '<div class="scale-legend-grid">'
    '<div class="scale-legend-box"><strong>1</strong><span>stimme gar nicht zu</span></div>'
    '<div class="scale-legend-box"><strong>3</strong><span>teils / teils</span></div>'
    '<div class="scale-legend-box"><strong>5</strong><span>stimme voll zu</span></div>'
    '</div>'
    '</div>'
)

    st.markdown(questionnaire_section_html, unsafe_allow_html=True)

    with st.container(key="questionnaire_item_card"):
        for key, question_text in current_block["items"]:
            value = st.radio(
                question_text,
                options=[1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=f"{key}_radio",
            )

            if value is not None:
                st.session_state.questionnaire[key] = value

    current_keys = [key for key, _ in current_block["items"]]
    current_complete = all(
        key in st.session_state.questionnaire
        for key in current_keys
    )

    with st.container(key="questionnaire_footer"):
        if current_step == 0:
            left, center, right = st.columns([1.25, 1.5, 1.25])

            with center:
                if st.button(
                    "Weiter",
                    use_container_width=True,
                    disabled=not current_complete,
                    key=f"questionnaire_next_first_{current_step}",
                ):
                    st.session_state.questionnaire_step += 1
                    st.rerun()

        else:
            left, back_col, gap, next_col, right = st.columns([0.85, 1.15, 0.2, 1.15, 0.85])

            with back_col:
                if st.button(
                    "Zurück",
                    use_container_width=True,
                    key=f"questionnaire_back_{current_step}",
                ):
                    st.session_state.questionnaire_step -= 1
                    st.rerun()

            with next_col:
                if current_step < total_blocks - 1:
                    if st.button(
                        "Weiter",
                        use_container_width=True,
                        disabled=not current_complete,
                        key=f"questionnaire_next_{current_step}",
                    ):
                        st.session_state.questionnaire_step += 1
                        st.rerun()
                else:
                    if st.button(
                    "Fragebogen absenden",
                    use_container_width=True,
                    disabled=not current_complete,
                    key="questionnaire_submit",
                ):
                        st.session_state.phase = "end"
                        st.rerun()

    if not current_complete:
        st.markdown(
            '<div class="questionnaire-hint">Bitte beantworte alle Aussagen in diesem Abschnitt, bevor du fortfährst.</div>',
            unsafe_allow_html=True,
        )

elif st.session_state.phase == "end":
    if not st.session_state.data_saved:
        save_response()
        st.session_state.data_saved = True

    st.title("Vielen Dank für deine Teilnahme")
    st.markdown(
        """
        <div class="thanks-card">
            Deine Antworten wurden erfolgreich gespeichert.
        </div>
        """,
        unsafe_allow_html=True,
    )