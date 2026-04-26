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

SHOW_ADMIN_PANEL = False
CSV_FILEPATH = "responses.csv"
DEBUG_MODE = False

GOOGLE_SHEET_ID = "1F43LmzUGQRqwCpcHsuAMMEEV6xB95FVXa8nVzMDD-rE"

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top, rgba(59,130,246,0.09), transparent 32%),
            #0f172a;
        color: #e5e7eb;
    }

    .block-container {
        max-width: 920px;
        padding-top: 3.4rem;
        padding-bottom: 2.5rem;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }

    p, li, label, .stMarkdown, .stCaption {
        color: #cbd5e1 !important;
    }

    div[data-testid="stProgressBar"] > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 850;
        color: #f8fafc;
        margin-bottom: 0.45rem;
        letter-spacing: -0.035em;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }

    .text-card {
        background: rgba(30, 41, 59, 0.96);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.28);
        margin-bottom: 1rem;
        backdrop-filter: blur(6px);
        color: #cbd5e1;
        line-height: 1.65;
    }

    .topmatch-card {
        background: linear-gradient(180deg, #1e293b 0%, #172554 100%);
        border: 1px solid rgba(96,165,250,0.24);
        border-radius: 24px;
        padding: 1.45rem 1.5rem;
        box-shadow: 0 18px 42px rgba(0,0,0,0.32);
        margin-bottom: 1rem;
        color: #cbd5e1;
        line-height: 1.65;
    }

    .ranking-card {
        background: rgba(30, 41, 59, 0.96);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.75rem;
    }

    .custom-muted {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .small-pill {
        display: inline-block;
        background: rgba(96,165,250,0.13);
        border: 1px solid rgba(96,165,250,0.24);
        color: #bfdbfe;
        border-radius: 999px;
        padding: 0.28rem 0.75rem;
        font-size: 0.86rem;
        margin-top: 0.35rem;
    }

    .big-number {
        font-size: 2rem;
        font-weight: 850;
        color: #f8fafc;
        margin: 0.2rem 0 0.2rem 0;
        letter-spacing: -0.03em;
    }

    .assessment-help {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }

    .thanks-card {
        background: linear-gradient(180deg, rgba(30,41,59,1) 0%, rgba(15,23,42,1) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 1.4rem;
        box-shadow: 0 18px 40px rgba(0,0,0,0.28);
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .info-box {
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.9rem;
        text-align: center;
    }

    .info-box strong {
        color: #f8fafc;
        display: block;
        margin-bottom: 0.25rem;
    }

    .info-box span {
        color: #94a3b8;
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
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
    }

    .instruction-box strong {
        color: #f8fafc;
        display: block;
        margin-bottom: 0.3rem;
    }

    .instruction-box span {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .study-progress {
        background: rgba(15,23,42,0.66);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 0.9rem 1rem;
        margin-bottom: 1.2rem;
    }

    .study-progress-label {
        color: #93c5fd;
        font-size: 0.86rem;
        font-weight: 700;
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
        border: 1px solid rgba(255,255,255,0.08);
        color: #94a3b8;
        background: rgba(30,41,59,0.75);
    }

    .study-progress-step.done {
        color: #bfdbfe;
        border-color: rgba(96,165,250,0.35);
        background: rgba(59,130,246,0.16);
    }

    .study-progress-step.active {
        color: #f8fafc;
        border-color: rgba(96,165,250,0.65);
        background: linear-gradient(90deg, rgba(37,99,235,0.35), rgba(59,130,246,0.18));
        font-weight: 750;
    }

    .soft-note {
        background: rgba(37,99,235,0.12);
        border: 1px solid rgba(96,165,250,0.22);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        color: #cbd5e1;
        margin-bottom: 1rem;
        line-height: 1.65;
    }

    .questionnaire-header {
        background: linear-gradient(180deg, rgba(30,41,59,0.98), rgba(15,23,42,0.98));
        border: 1px solid rgba(96,165,250,0.16);
        border-radius: 24px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1rem;
        box-shadow: 0 16px 38px rgba(0,0,0,0.25);
    }

    @media (max-width: 700px) {
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
    </style>
    """,
    unsafe_allow_html=True,
)

items = [
    {"id": 1, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Mir ist ein unterstützendes Miteinander im Team wichtig."},
    {"id": 2, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ich arbeite am liebsten in einem Umfeld, in dem Zusammenhalt spürbar ist."},
    {"id": 3, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Ein gutes Arbeitsklima ist mir wichtiger als interner Wettbewerb."},
    {"id": 4, "dimension": "Zusammenarbeit / Gemeinschaft", "text": "Mir ist ein harmonisches Teamklima wichtiger als persönliche Karrierechancen."},
    {"id": 5, "dimension": "Leistung / Wettbewerb", "text": "Klare Ziele und hohe Erwartungen motivieren mich."},
    {"id": 6, "dimension": "Leistung / Wettbewerb", "text": "Ich arbeite gerne in einem Umfeld, in dem Leistung sichtbar anerkannt wird."},
    {"id": 7, "dimension": "Leistung / Wettbewerb", "text": "Ein gewisser Wettbewerb im Arbeitsalltag spornt mich an."},
    {"id": 8, "dimension": "Leistung / Wettbewerb", "text": "Ich finde es motivierend, wenn Leistung im Team sichtbar miteinander verglichen wird."},
    {"id": 9, "dimension": "Innovation / Flexibilität", "text": "Ich bevorzuge ein Arbeitsumfeld, in dem neue Ideen willkommen sind."},
    {"id": 10, "dimension": "Innovation / Flexibilität", "text": "Ich mag es, wenn Dinge ausprobiert und weiterentwickelt werden."},
    {"id": 11, "dimension": "Innovation / Flexibilität", "text": "Zu viel Routine im Arbeitsalltag empfinde ich als einschränkend."},
    {"id": 12, "dimension": "Innovation / Flexibilität", "text": "Ich nehme unklare Abläufe in Kauf, wenn dadurch mehr Raum für neue Ideen entsteht."},
    {"id": 13, "dimension": "Struktur / Stabilität", "text": "Klare Prozesse und feste Abläufe geben mir Sicherheit."},
    {"id": 14, "dimension": "Struktur / Stabilität", "text": "Ich arbeite gerne in einem Umfeld mit eindeutigen Regeln und Zuständigkeiten."},
    {"id": 15, "dimension": "Struktur / Stabilität", "text": "Ich bevorzuge ein gut organisiertes Arbeitsumfeld."},
    {"id": 16, "dimension": "Struktur / Stabilität", "text": "Ich arbeite lieber mit klaren Vorgaben als mit viel Freiheit."},
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
        "description": "Clarion Systems bietet ein klar strukturiertes und verlässliches Arbeitsumfeld, in dem definierte Prozesse und eindeutige Zuständigkeiten im Mittelpunkt stehen. Mitarbeitende profitieren von stabilen Rahmenbedingungen, die Sicherheit und Planbarkeit im Arbeitsalltag ermöglichen. Die Organisation legt großen Wert auf Effizienz, Verlässlichkeit und eine klare Rollenverteilung, wodurch ein ruhiges und geordnetes Arbeitsumfeld entsteht.",
    },
}

questionnaire_items = [
    {
        "section": "A. Dein Antwortgefühl",
        "items": [
            ("q1", "Ich habe mich bei meinen Antworten stark auf mein erstes Gefühl verlassen."),
            ("q2", "Ich habe lange über meine Antworten nachgedacht. (invertiert)"),
            ("q3", "Die Beantwortung fiel mir eher intuitiv als analytisch."),
            ("q4", "Ich musste meine Antworten stark abwägen. (invertiert)"),
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
            ("q14", "Das Verfahren wirkte auf mich unnötig kompliziert. (invertiert)"),
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
    st.session_state.phase = "consent"

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
    st.session_state.phase = "consent"
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
                "differences": {dim: round(abs(user_profile[dim] - company_profile[dim]), 2) for dim in user_profile},
                "profile": company_profile,
                "archetype": company_data["archetype"],
                "description": company_data["description"],
            }
        )

    return sorted(ranking, key=lambda x: x["score"], reverse=True)


def build_export_row():
    row = {
        "participant_id": st.session_state.participant_id,
        "timestamp_utc": datetime.utcnow().isoformat(),
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


if st.session_state.phase == "consent":
    st.markdown('<div class="hero-title">Studienteilnahme</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Vielen Dank, dass du an dieser kurzen Studie teilnimmst.</div>', unsafe_allow_html=True)

    text_card(
        """
        <p>Im Rahmen dieser Masterarbeit wird untersucht, wie Personen ihre Präferenzen in Bezug auf Arbeitsumfelder angeben und wie daraus eine kulturelle Passung zu Unternehmen abgeleitet werden kann.</p>

        <div class="info-grid">
            <div class="info-box"><strong>Dauer</strong><span>ca. 5–7 Minuten</span></div>
            <div class="info-box"><strong>Anonym</strong><span>Es werden keine personenbezogenen Daten erhoben.</span></div>
            <div class="info-box"><strong>Freiwillig</strong><span>Abbruch jederzeit möglich</span></div>
        </div>

        <p>Alle Angaben werden anonym gespeichert und ausschließlich zu wissenschaftlichen Zwecken ausgewertet. Mit dem Aktivieren der Checkbox und dem Klick auf „Weiter“ erklärst du dich mit der Teilnahme einverstanden. Die Teilnahme ist freiwillig und kann jederzeit ohne Angabe von Gründen abgebrochen werden.</p>

        <p><strong>Kontakt bei Rückfragen:</strong><br>
        Niklas Demtröder · niklas.demtroeder@iu-study.org</p>
        """
    )

    consent = st.checkbox("Ich stimme der Teilnahme an der Studie zu.")

    if consent and st.button("Weiter"):
        st.session_state.phase = "intro"
        st.rerun()


elif st.session_state.phase == "intro":
    render_progress(0)

    st.markdown('<div class="hero-title">Cultural Fit Matcher</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Welche Arbeitsumgebung passt wirklich zu dir?</div>', unsafe_allow_html=True)

    text_card(
        """
        <p>Stell dir vor, du befindest dich aktuell auf Jobsuche. Im folgenden Verfahren gibst du an, welche Merkmale dir in einem Arbeitsumfeld wichtig sind.</p>

        <p>Anschließend erhältst du ein Matching mit mehreren fiktiven Unternehmen, die unterschiedliche Unternehmenskulturen repräsentieren.</p>

        <p>Danach folgt noch eine kurze Einschätzung dazu, wie du das Verfahren erlebt hast.</p>

        <p><strong>Ablauf dieser Studie</strong></p>

        <div class="info-grid">
            <div class="info-box"><strong>1. Präferenzen</strong><span>Arbeitsumfeld bewerten</span></div>
            <div class="info-box"><strong>2. Ergebnis</strong><span>Matching ansehen</span></div>
            <div class="info-box"><strong>3. Einschätzung</strong><span>kurzer Fragebogen</span></div>
        </div>

        <p>Es gibt keine richtigen oder falschen Antworten. Entscheidend ist, was zu deinen persönlichen Präferenzen passt.</p>
        """
    )

    if st.button("Jetzt starten"):
        st.session_state.phase = "instructions"
        st.rerun()


elif st.session_state.phase == "instructions":
    render_progress(0)

    st.markdown('<div class="hero-title">Hinweise zum Ablauf</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Bitte beantworte die Aussagen so, wie sie deinen persönlichen Präferenzen entsprechen.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.condition == "swipe":
        text_card(
            """
            <h3>Deine Aufgabe</h3>
            <p>Beurteile jede Aussage über die Wischrichtung.</p>

            <div class="instruction-row">
                <div class="instruction-box"><strong>← Nach links</strong><span>eher keine Zustimmung</span></div>
                <div class="instruction-box"><strong>Nach rechts →</strong><span>eher Zustimmung</span></div>
            </div>

            <p>Bitte nutze für die Bewertung die Wischbewegung.</p>
            """
        )
    else:
        text_card(
            """
            <h3>Deine Aufgabe</h3>
            <p>Bewerte jede Aussage auf einer Skala von 1 bis 5.</p>

            <div class="instruction-row">
                <div class="instruction-box"><strong>1</strong><span>stimme überhaupt nicht zu</span></div>
                <div class="instruction-box"><strong>5</strong><span>stimme voll zu</span></div>
            </div>

            <p>Wähle jeweils die Antwort aus, die am besten zu dir passt.</p>
            """
        )

    if st.button("Bewertung starten"):
        st.session_state.phase = "assessment"
        st.rerun()


elif st.session_state.phase == "assessment":
    render_progress(1)

    st.title("Cultural Fit Matcher")

    if st.session_state.condition == "swipe":
        st.markdown(
            """
            <div class="assessment-help">
                Nach rechts bedeutet eher Zustimmung, nach links eher keine Zustimmung.
            </div>
            """,
            unsafe_allow_html=True,
        )
        result = swipe_component(items=items, mode="swipe", key="swipe_full_assessment")
    else:
        st.markdown(
            """
            <div class="assessment-help">
                Wähle jeweils einen Wert von 1 bis 5.
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

    st.markdown('<div class="hero-title">Dein Ergebnis – kurze Einordnung</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Auf Basis deiner Antworten wurde ein fiktives Unternehmensprofil mit hoher kultureller Übereinstimmung berechnet.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="soft-note">
            Die Studie ist nach dieser Ergebnisanzeige noch nicht abgeschlossen.
            Im nächsten Schritt geht es darum, wie du das Ergebnis und das Verfahren wahrgenommen hast.
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_profile = calculate_user_profile(st.session_state.answers)
    ranking = calculate_ranking(user_profile)
    top_match = ranking[0]

    sorted_user_dims = sorted(user_profile.items(), key=lambda x: x[1], reverse=True)
    top_dims = [d[0] for d in sorted_user_dims[:2]]

    st.markdown(
        f"""
        <div class="topmatch-card">
            <h3>Höchste Übereinstimmung</h3>
            <div class="big-number">{escape(top_match["company"])}</div>
            <p>Basierend auf deinen Antworten ergibt sich die höchste Übereinstimmung mit <strong>{escape(top_match["company"])}</strong>. Die berechnete kulturelle Übereinstimmung liegt bei <strong>{top_match["score"]} %</strong>.</p>
            <div class="small-pill">{escape(top_match["archetype"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_card(
        f"""
        <h3>Über dieses Unternehmen</h3>
        <p>Bei dem folgenden Unternehmensprofil handelt es sich um ein fiktives Beispielunternehmen, das eine bestimmte Unternehmenskultur repräsentiert.</p>
        <p>{escape(top_match["description"])}</p>
        """
    )

    sorted_dims = sorted(top_match["differences"].items(), key=lambda x: x[1])
    best_dims = [d[0] for d in sorted_dims[:2]]
    best_dims_html = "".join([f"<li>{escape(dim)}</li>" for dim in best_dims])

    text_card(
        f"""
        <h3>Warum dieses Ergebnis zustande kommt</h3>
        <p>Deine Antworten zeigen, dass dir besonders <strong>{escape(top_dims[0])}</strong> und <strong>{escape(top_dims[1])}</strong> wichtig sind.</p>
        <p>Die größte Übereinstimmung mit diesem Unternehmen zeigt sich vor allem in:</p>
        <ul>{best_dims_html}</ul>
        <p>Das bedeutet: Es gibt in diesen Bereichen eine höhere Übereinstimmung zwischen deinen angegebenen Präferenzen und dem dargestellten Unternehmensprofil.</p>
        """
    )

    with st.expander("Wie wurde das Ergebnis berechnet?"):
        st.write(
            "Deine Antworten wurden zu vier Kulturdimensionen zusammengefasst und mit den "
            "hinterlegten Kulturprofilen der Unternehmen verglichen. Je geringer die Abweichung, "
            "desto höher ist die angezeigte Übereinstimmung."
        )

    st.subheader("Weitere mögliche Matches")

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

    st.subheader("Deine erste Einschätzung")

    self_assessment = st.radio(
        "Wie passend erscheint dir das angezeigte Ergebnis?",
        options=[
            "Sehr passend",
            "Eher passend",
            "Teils / teils",
            "Eher nicht passend",
            "Gar nicht passend",
        ],
        index=None,
    )

    if self_assessment is None:
        st.info("Bitte gib zuerst deine Einschätzung zum Ergebnis ab, bevor du fortfährst.")
    else:
        left, center, right = st.columns([1.1, 1.4, 1.1])
        with center:
            if st.button("Ergebnis bewerten & fortfahren", use_container_width=True):
                st.session_state.self_assessment = self_assessment
                st.session_state.phase = "pre_questionnaire"
                st.rerun()


elif st.session_state.phase == "pre_questionnaire":
    render_progress(3)

    st.markdown('<div class="hero-title">Deine Einschätzung zum Verfahren</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Im letzten Teil geht es darum, wie du das Verfahren erlebt hast.</div>',
        unsafe_allow_html=True,
    )

    text_card(
        """
        <p>Bitte bewerte im folgenden kurzen Fragebogen, wie du die Bearbeitung, das Ergebnis und die Darstellung des Verfahrens wahrgenommen hast.</p>
        <p>Die Einschätzung dauert etwa 1–2 Minuten. Auch hier gibt es keine richtigen oder falschen Antworten.</p>
        """
    )

    if st.button("Einschätzung starten"):
        st.session_state.phase = "questionnaire"
        st.session_state.questionnaire_step = 0
        st.rerun()


elif st.session_state.phase == "questionnaire":
    render_progress(3)

    current_step = st.session_state.questionnaire_step
    current_block = questionnaire_items[current_step]
    total_blocks = len(questionnaire_items)

    st.markdown('<div class="hero-title">Deine Einschätzung</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero-subtitle">Abschnitt {current_step + 1} von {total_blocks}</div>',
        unsafe_allow_html=True,
    )

    st.progress((current_step + 1) / total_blocks)

    st.markdown(
        f"""
        <div class="questionnaire-header">
            <h3>{escape(current_block["section"])}</h3>
            <p style="color:#94a3b8; font-size:0.92rem;">
                1 = stimme überhaupt nicht zu | 2 = stimme eher nicht zu |
                3 = teils/teils | 4 = stimme eher zu | 5 = stimme voll zu
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for key, question_text in current_block["items"]:
        value = st.radio(
            question_text,
            options=[1, 2, 3, 4, 5],
            index=None,
            horizontal=True,
            key=f"{key}_radio",
        )

        # SOFORT speichern
        if value is not None:
            st.session_state.questionnaire[key] = value

    current_keys = [key for key, _ in current_block["items"]]
    current_complete = all(
        key in st.session_state.questionnaire
        for key in current_keys
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if current_step > 0:
            if st.button("Zurück", use_container_width=True):
                st.session_state.questionnaire_step -= 1
                st.rerun()

    with col2:
        if current_step < total_blocks - 1:
            if st.button("Weiter", use_container_width=True, disabled=not current_complete):
                for key in current_keys:
                    st.session_state.questionnaire[key] = st.session_state.get(key)
                st.session_state.questionnaire_step += 1
                st.rerun()
        else:
            if st.button("Fragebogen absenden", use_container_width=True, disabled=not current_complete):
                for key in current_keys:
                    st.session_state.questionnaire[key] = st.session_state.get(key)

                for block in questionnaire_items:
                    for key, _ in block["items"]:
                        st.session_state.questionnaire[key] = st.session_state.get(key)

                st.session_state.phase = "end"
                st.rerun()

    if not current_complete:
        st.info("Bitte beantworte alle Aussagen in diesem Abschnitt, bevor du fortfährst.")


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