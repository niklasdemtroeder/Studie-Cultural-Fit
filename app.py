import csv
import os
import random
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st
from swipe_component import swipe_component

st.set_page_config(page_title="Cultural Fit Prototype", layout="centered")

# -----------------------------
# Steuerung
# -----------------------------
SHOW_ADMIN_PANEL = False
CSV_FILEPATH = "responses.csv"
DEBUG_MODE = False

# -----------------------------
# Globales Styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top, rgba(59,130,246,0.08), transparent 30%),
            #0f172a;
        color: #e5e7eb;
    }

    .block-container {
        max-width: 920px;
        padding-top: 4rem;
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

    .custom-card {
        background: rgba(30, 41, 59, 0.96);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.28);
        margin-bottom: 1rem;
        backdrop-filter: blur(6px);
    }

    .custom-muted {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .ranking-card {
        background: rgba(30, 41, 59, 0.96);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.75rem;
    }

    .topmatch-card {
        background: linear-gradient(180deg, #1e293b 0%, #172554 100%);
        border: 1px solid rgba(96,165,250,0.22);
        border-radius: 22px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 18px 42px rgba(0,0,0,0.32);
        margin-bottom: 1rem;
    }

    .small-pill {
        display: inline-block;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        color: #cbd5e1;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-size: 0.85rem;
        margin-top: 0.35rem;
    }

    .big-number {
        font-size: 2rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 0.2rem 0 0.2rem 0;
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

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .info-box {
        background: rgba(15,23,42,0.7);
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

    .step-card {
        background: rgba(30,41,59,0.96);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.28);
        margin-bottom: 1rem;
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

    @media (max-width: 700px) {
        .info-grid {
            grid-template-columns: 1fr;
        }

        .instruction-row {
            flex-direction: column;
        }

        .hero-title {
            font-size: 2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Datenbasis
# -----------------------------
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
        "description": (
            "Nordlicht Care Solutions steht für ein stark teamorientiertes Arbeitsumfeld, "
            "in dem Zusammenhalt und gegenseitige Unterstützung eine zentrale Rolle spielen. "
            "Die Zusammenarbeit ist geprägt von Vertrauen, Wertschätzung und einem offenen Austausch auf Augenhöhe. "
            "Mitarbeitende erleben hier eine Kultur, in der man sich aufeinander verlassen kann und Erfolge gemeinsam erzielt werden. "
            "Klare Strukturen sorgen gleichzeitig für Orientierung und Stabilität im Arbeitsalltag."
        ),
    },
    "Strive Consulting Group": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 2,
            "Leistung / Wettbewerb": 5,
            "Innovation / Flexibilität": 4,
            "Struktur / Stabilität": 3,
        },
        "archetype": "leistungsorientierter Arbeitgeber",
        "description": (
            "Die Strive Consulting Group bietet ein leistungsorientiertes Umfeld, in dem ambitionierte Ziele "
            "und hohe Erwartungen den Arbeitsalltag prägen. Mitarbeitende werden aktiv gefordert und gefördert, "
            "ihre individuellen Stärken einzubringen und kontinuierlich weiterzuentwickeln. "
            "Erfolge werden sichtbar anerkannt und Leistung hat einen hohen Stellenwert. "
            "Gleichzeitig eröffnet das dynamische Umfeld Raum für innovative Lösungsansätze und eigenverantwortliches Arbeiten."
        ),
    },
    "Vireon Labs": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 3,
            "Leistung / Wettbewerb": 3,
            "Innovation / Flexibilität": 5,
            "Struktur / Stabilität": 2,
        },
        "archetype": "innovationsorientierter Arbeitgeber",
        "description": (
            "Vireon Labs steht für ein kreatives und innovationsgetriebenes Arbeitsumfeld, "
            "in dem neue Ideen ausdrücklich willkommen sind. Mitarbeitende haben die Möglichkeit, "
            "aktiv an der Gestaltung von Prozessen und Lösungen mitzuwirken. "
            "Flexibilität, Offenheit und Experimentierfreude prägen die Unternehmenskultur. "
            "Feste Strukturen treten dabei bewusst in den Hintergrund, um Raum für Weiterentwicklung und neue Denkansätze zu schaffen."
        ),
    },
    "Clarion Systems": {
        "dimension_scores": {
            "Zusammenarbeit / Gemeinschaft": 3,
            "Leistung / Wettbewerb": 3,
            "Innovation / Flexibilität": 2,
            "Struktur / Stabilität": 5,
        },
        "archetype": "strukturorientierter Arbeitgeber",
        "description": (
            "Clarion Systems bietet ein klar strukturiertes und verlässliches Arbeitsumfeld, "
            "in dem definierte Prozesse und eindeutige Zuständigkeiten im Mittelpunkt stehen. "
            "Mitarbeitende profitieren von stabilen Rahmenbedingungen, die Sicherheit und Planbarkeit im Arbeitsalltag ermöglichen. "
            "Die Organisation legt großen Wert auf Effizienz, Verlässlichkeit und eine klare Rollenverteilung, "
            "wodurch ein ruhiges und geordnetes Arbeitsumfeld entsteht."
        ),
    },
}

questionnaire_items = [
    {
        "section": "A. Intuitives Antwortverhalten",
        "items": [
            ("q1", "Ich habe mich bei meinen Antworten stark auf mein erstes Gefühl verlassen."),
            ("q2", "Ich habe lange über meine Antworten nachgedacht. (invertiert)"),
            ("q3", "Die Beantwortung fiel mir eher intuitiv als analytisch."),
            ("q4", "Ich musste meine Antworten stark abwägen. (invertiert)"),
        ],
    },
    {
        "section": "B. Bewusste Antwortkontrolle",
        "items": [
            ("q5", "Ich habe meine Antworten bewusst gesteuert."),
            ("q6", "Ich habe während der Bearbeitung stark darauf geachtet, wie ich antworte."),
        ],
    },
    {
        "section": "C. Soziale Erwünschtheit",
        "items": [
            ("q7", "Ich habe darauf geachtet, mit meinen Antworten einen möglichst positiven Eindruck zu vermitteln."),
            ("q8", "Bei meinen Antworten war mir wichtig, wie diese auf andere wirken könnten."),
            ("q9", "Ich habe eher so geantwortet, wie es gesellschaftlich erwünscht oder positiv bewertet wird."),
            ("q10", "Ich habe versucht, mich durch meine Antworten möglichst vorteilhaft darzustellen."),
        ],
    },
    {
        "section": "D. Wahrgenommene Benutzerfreundlichkeit",
        "items": [
            ("q11", "Das Verfahren war einfach zu bedienen."),
            ("q12", "Die Bearbeitung war für mich verständlich und nachvollziehbar."),
            ("q13", "Ich fand die Beantwortung insgesamt angenehm."),
            ("q14", "Das Verfahren wirkte auf mich unnötig kompliziert. (invertiert)"),
        ],
    },
    {
        "section": "E. Wahrgenommene Passung des Ergebnisses",
        "items": [
            ("q15", "Das angezeigte Ergebnis passt gut zu mir."),
            ("q16", "Das Ergebnis wirkt auf mich plausibel."),
            ("q17", "Ich kann gut nachvollziehen, warum mir dieses Unternehmen als bestes Match angezeigt wurde."),
        ],
    },
    {
        "section": "F. Bewerbungsintention",
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

# -----------------------------
# Session State
# -----------------------------
if "participant_id" not in st.session_state:
    st.session_state.participant_id = str(uuid.uuid4())

if "condition" not in st.session_state:
    st.session_state.condition = random.choice(["swipe", "likert"])

if "phase" not in st.session_state:
    st.session_state.phase = "consent"

if "step" not in st.session_state:
    st.session_state.step = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "questionnaire" not in st.session_state:
    st.session_state.questionnaire = {}

if "data_saved" not in st.session_state:
    st.session_state.data_saved = False

if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

if "self_assessment" not in st.session_state:
    st.session_state.self_assessment = None

# -----------------------------
# Hilfsfunktionen
# -----------------------------
def reset_app():
    st.session_state.participant_id = str(uuid.uuid4())
    st.session_state.phase = "consent"
    st.session_state.step = 0
    st.session_state.answers = []
    st.session_state.questionnaire = {}
    st.session_state.condition = random.choice(["swipe", "likert"])
    st.session_state.data_saved = False
    st.session_state.self_assessment = None

def calculate_user_profile(answer_list):
    grouped = {}
    for answer in answer_list:
        dim = answer["dimension"]
        val = answer["value"]
        if dim not in grouped:
            grouped[dim] = []
        grouped[dim].append(val)

    return {
        dim: round(sum(values) / len(values), 2)
        for dim, values in grouped.items()
    }

def calculate_ranking(user_profile):
    ranking = []

    for company_name, company_data in companies.items():
        company_profile = company_data["dimension_scores"]

        total_difference = 0
        for dim in user_profile:
            total_difference += abs(user_profile[dim] - company_profile[dim])

        match_score = round((1 - total_difference / 16) * 100, 1)

        ranking.append(
            {
                "company": company_name,
                "score": match_score,
                "differences": {
                    dim: round(abs(user_profile[dim] - company_profile[dim]), 2)
                    for dim in user_profile
                },
                "profile": company_profile,
                "archetype": company_data["archetype"],
                "description": company_data["description"],
            }
        )

    ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)
    return ranking

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
            st.sidebar.info("Noch keine gespeicherten Antworten vorhanden.")
            return

        st.sidebar.metric("Teilnahmen", len(df))

        if "condition" in df.columns:
            swipe_count = int((df["condition"] == "swipe").sum())
            likert_count = int((df["condition"] == "likert").sum())
            st.sidebar.write(f"Swipe: {swipe_count}")
            st.sidebar.write(f"Likert: {likert_count}")

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="responses.csv herunterladen",
            data=csv_bytes,
            file_name="responses.csv",
            mime="text/csv",
        )

        with st.sidebar.expander("Vorschau der letzten Einträge"):
            preview_df = df.tail(5)
            st.dataframe(preview_df, use_container_width=True)

        with st.expander("Admin-Datenansicht öffnen"):
            st.subheader("Gespeicherte Teilnahmen")
            st.dataframe(df, use_container_width=True)

            st.subheader("Letzte 10 Einträge")
            st.dataframe(df.tail(10), use_container_width=True)

            if "condition" in df.columns:
                st.subheader("Verteilung der Bedingungen")
                counts = df["condition"].value_counts()
                st.bar_chart(counts)

# -----------------------------
# Admin-Bereich optional
# -----------------------------
if SHOW_ADMIN_PANEL:
    render_admin_panel()

if DEBUG_MODE:
    if st.button("Neu starten"):
        reset_app()
        st.rerun()

# -----------------------------
# PHASE 0: Einwilligung
# -----------------------------
if st.session_state.phase == "consent":
    st.markdown('<div class="hero-title">Studienteilnahme</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Vielen Dank, dass du an dieser kurzen Studie teilnimmst.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write(
        "Im Rahmen dieser Masterarbeit wird untersucht, wie Personen ihre Präferenzen in Bezug auf "
        "Arbeitsumfelder angeben und wie daraus eine kulturelle Passung zu Unternehmen abgeleitet werden kann."
    )

    st.markdown(
        """
<div class="info-grid">
    <div class="info-box">
        <strong>Dauer</strong>
        <span>ca. 5–7 Minuten</span>
    </div>
    <div class="info-box">
        <strong>Anonym</strong>
        <span>Es werden keine personenbezogenen Daten erhoben.</span>
    </div>
    <div class="info-box">
        <strong>Freiwillig</strong>
        <span>Abbruch jederzeit möglich</span>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Alle Angaben werden anonym gespeichert und ausschließlich zu wissenschaftlichen Zwecken ausgewertet. "
        "Mit dem Aktivieren der Checkbox und dem Klick auf „Weiter“ erklärst du dich mit der Teilnahme einverstanden."
        " Die Teilnahme ist freiwillig und kann jederzeit ohne Angabe von Gründen abgebrochen werden."
    )

    st.write("**Kontakt bei Rückfragen:**")
    st.write("Niklas Demtröder · niklas.demtroeder@iu-study.org")
    st.markdown("</div>", unsafe_allow_html=True)

    consent = st.checkbox("Ich stimme der Teilnahme an der Studie zu.")

    if consent and st.button("Weiter"):
        st.session_state.phase = "intro"
        st.rerun()

# -----------------------------
# PHASE 1: Startscreen
# -----------------------------
elif st.session_state.phase == "intro":
    st.markdown('<div class="hero-title">Cultural Fit Matcher</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Welche Arbeitsumgebung passt wirklich zu dir?</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write(
        "Stell dir vor, du befindest dich aktuell auf Jobsuche. "
        "Im folgenden Verfahren gibst du an, welche Merkmale dir in einem Arbeitsumfeld wichtig sind."
    )
    st.write(
        "Anschließend erhältst du ein Matching mit mehreren fiktiven Unternehmen, "
        "die unterschiedliche Unternehmenskulturen repräsentieren. Dies zeigt, welches Arbeitsumfeld besonders gut zu deinen Präferenzen passt."
    )
    st.write(
        "Zum Abschluss beantwortest du noch einen kurzen Fragebogen zu deiner Wahrnehmung des Verfahrens."
    )

    st.write("**Ablauf dieser Studie**")

    st.markdown(
        """
<div class="info-grid">
    <div class="info-box">
        <strong>1. Präferenzen</strong>
        <span>Arbeitsumfeld bewerten</span>
    </div>
    <div class="info-box">
        <strong>2. Match</strong>
        <span>passendes Unternehmen ansehen</span>
    </div>
    <div class="info-box">
        <strong>3. Feedback</strong>
        <span>kurzer Abschlussfragebogen</span>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Es gibt keine richtigen oder falschen Antworten. Entscheidend ist, was zu deinen persönlichen Präferenzen passt."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Jetzt starten"):
        st.session_state.phase = "instructions"
        st.rerun()

# -----------------------------
# PHASE 2: Instruktionsscreen
# -----------------------------
elif st.session_state.phase == "instructions":
    st.markdown('<div class="hero-title">Hinweise zum Ablauf</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Bitte beantworte die Aussagen so, wie sie deinen persönlichen Präferenzen entsprechen.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="step-card">', unsafe_allow_html=True)

    if st.session_state.condition == "swipe":
        st.subheader("Deine Aufgabe")
        st.write("Beurteile jede Aussage möglichst spontan.")

        st.markdown(
            """
<div class="instruction-row">
    <div class="instruction-box">
        <strong>← Nach links</strong>
        <span>eher keine Zustimmung</span>
    </div>
    <div class="instruction-box">
        <strong>Nach rechts →</strong>
        <span>eher Zustimmung</span>
    </div>
</div>
            """,
            unsafe_allow_html=True,
        )

        st.write("Du kannst entweder wischen oder die Buttons unter der Karte verwenden.")

    else:
        st.subheader("Deine Aufgabe")
        st.write("Bewerte jede Aussage auf einer Skala von 1 bis 5.")

        st.markdown(
            """
<div class="instruction-row">
    <div class="instruction-box">
        <strong>1</strong>
        <span>stimme überhaupt nicht zu</span>
    </div>
    <div class="instruction-box">
        <strong>5</strong>
        <span>stimme voll zu</span>
    </div>
</div>
            """,
            unsafe_allow_html=True,
        )

        st.write("Wähle jeweils die Antwort aus, die am besten zu dir passt.")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Starten"):
        st.session_state.phase = "assessment"
        st.rerun()

# -----------------------------
# PHASE 3: Hauptassessment
# -----------------------------
elif st.session_state.phase == "assessment":
    st.title("Cultural Fit Matcher")

    if st.session_state.condition == "swipe":
        st.markdown(
            """
            <div class="assessment-help">
                Beantworte die Aussagen möglichst spontan. Nach rechts bedeutet eher Zustimmung, nach links eher keine Zustimmung.
            </div>
            """,
            unsafe_allow_html=True,
        )

        result = swipe_component(
            items=items,
            mode="swipe",
            key="swipe_full_assessment",
        )

    else:
        st.markdown(
            """
            <div class="assessment-help">
                Beantworte die Aussagen möglichst passend für dich. Wähle jeweils einen Wert von 1 bis 5.
            </div>
            """,
            unsafe_allow_html=True,
        )

        result = swipe_component(
            items=items,
            mode="likert",
            key="likert_full_assessment",
        )

    if DEBUG_MODE:
        st.write("Debug Rückgabe:", result)

    if isinstance(result, dict) and result.get("completed") is True:
        st.session_state.answers = result.get("answers", [])
        st.session_state.phase = "results"
        st.rerun()

# -----------------------------
# PHASE 4: Ergebnisse
# -----------------------------
elif st.session_state.phase == "results":
    st.title("Dein Cultural Fit Match")

    user_profile = calculate_user_profile(st.session_state.answers)
    ranking = calculate_ranking(user_profile)
    top_match = ranking[0]

    sorted_user_dims = sorted(user_profile.items(), key=lambda x: x[1], reverse=True)
    top_dims = [d[0] for d in sorted_user_dims[:2]]

    st.markdown('<div class="topmatch-card">', unsafe_allow_html=True)
    st.subheader("Dein stärkstes Match")

    st.markdown(
        f'<div class="big-number">{top_match["company"]}</div>',
        unsafe_allow_html=True,
    )

    st.write(
        f"Du matchst besonders gut mit **{top_match['company']}**. "
        f"Die berechnete kulturelle Übereinstimmung liegt bei **{top_match['score']} %**."
    )

    st.markdown(
        f'<div class="small-pill">{top_match["archetype"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("Über dieses Unternehmen")

    st.write(
        "Bei dem folgenden Unternehmensprofil handelt es sich um ein fiktives Beispielunternehmen, "
        "das eine bestimmte Unternehmenskultur repräsentiert."
    )

    st.write(top_match["description"])
    st.markdown("</div>", unsafe_allow_html=True)

    sorted_dims = sorted(top_match["differences"].items(), key=lambda x: x[1])
    best_dims = [d[0] for d in sorted_dims[:2]]

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("Warum dieses Match zustande kommt")

    st.write(
        f"Deine Antworten zeigen, dass dir besonders **{top_dims[0]}** "
        f"und **{top_dims[1]}** wichtig sind."
    )

    st.write("Die größte Übereinstimmung mit diesem Unternehmen zeigt sich vor allem in:")

    for dim in best_dims:
        st.write(f"- {dim}")

    st.write(
        "Das bedeutet: Die Kultur dieses Unternehmens entspricht in zentralen Bereichen "
        "deinen angegebenen Präferenzen für ein Arbeitsumfeld."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Wie wurde das Match berechnet?"):
        st.write(
            "Deine Antworten wurden zu vier Kulturdimensionen zusammengefasst und mit den "
            "hinterlegten Kulturprofilen der Unternehmen verglichen. Je geringer die Abweichung, "
            "desto höher ist die angezeigte Übereinstimmung."
        )

    st.subheader("Weitere passende Unternehmen")

    for i, entry in enumerate(ranking[1:], start=2):
        st.markdown(
            f"""
            <div class="ranking-card">
                <strong>{i}. {entry['company']}</strong><br>
                <span class="custom-muted">
                    {entry['score']} % Übereinstimmung · {entry['archetype']}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("Deine Einschätzung")

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

    st.markdown("</div>", unsafe_allow_html=True)

    if self_assessment is None:
        st.info("Bitte gib zuerst deine Einschätzung zum Top-Match ab, bevor du fortfährst.")
    else:
        left, center, right = st.columns([1.4, 1, 1.4])
        with center:
          if st.button("Weiter", use_container_width=True):
            st.session_state.self_assessment = self_assessment
            st.session_state.phase = "pre_questionnaire"
            st.rerun()

# -----------------------------
# PHASE 5: Übergang zum Abschlussfragebogen
# -----------------------------
elif st.session_state.phase == "pre_questionnaire":
    st.markdown('<div class="hero-title">Fast geschafft</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Im nächsten Schritt folgen einige kurze Aussagen zum gerade durchlaufenen Verfahren.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.write(
        "Bitte gib im folgenden Abschlussfragebogen an, wie du das Verfahren erlebt hast "
        "und wie passend das angezeigte Ergebnis für dich wirkt."
    )
    st.write(
        "Auch hier gibt es keine richtigen oder falschen Antworten. "
        "Entscheidend ist dein persönlicher Eindruck."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Abschlussfragebogen starten"):
        st.session_state.phase = "questionnaire"
        st.rerun()

# -----------------------------
# PHASE 6: Abschlussfragebogen
# -----------------------------
elif st.session_state.phase == "questionnaire":
    st.title("Abschlussfragebogen")

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write(
        "Im Folgenden findest du einige Aussagen zu dem gerade durchlaufenen Verfahren. "
        "Bitte gib an, inwieweit du den Aussagen zustimmst."
    )
    st.caption(
        "1 = stimme überhaupt nicht zu | 2 = stimme eher nicht zu | "
        "3 = teils/teils | 4 = stimme eher zu | 5 = stimme voll zu"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    questionnaire_responses = {}

    for block in questionnaire_items:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader(block["section"])
        for key, question_text in block["items"]:
            questionnaire_responses[key] = st.radio(
                question_text,
                options=[1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=key,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    if all(value is not None for value in questionnaire_responses.values()):
        if st.button("Fragebogen absenden"):
            st.session_state.questionnaire = questionnaire_responses
            st.session_state.phase = "end"
            st.rerun()
    else:
        st.info("Bitte beantworte alle Aussagen, bevor du fortfährst.")

# -----------------------------
# PHASE 7: Endscreen
# -----------------------------
elif st.session_state.phase == "end":
    if not st.session_state.data_saved:
        save_response_to_csv(CSV_FILEPATH)
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

    if DEBUG_MODE:
        st.subheader("Debug: Gesamtdaten")
        st.write(
            {
                "participant_id": st.session_state.participant_id,
                "condition": st.session_state.condition,
                "answers": st.session_state.answers,
                "questionnaire": st.session_state.questionnaire,
                "self_assessment": st.session_state.self_assessment,
            }
        )