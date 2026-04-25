import React, { useEffect, useMemo, useState } from "react";
import TinderCard from "react-tinder-card";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

function App({ args }) {
  const items = args?.items || [];
  const mode = args?.mode || "swipe";

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [swipeDirection, setSwipeDirection] = useState(null);
  const [selectedValue, setSelectedValue] = useState(null);
  const [finished, setFinished] = useState(false);

  const isMobile = typeof window !== "undefined" && window.innerWidth < 600;
  const currentItem = items[currentIndex];

  const cardWidth = useMemo(() => {
    if (typeof window === "undefined") return 340;
    const maxWidth = isMobile ? window.innerWidth - 32 : 440;
    return Math.min(Math.max(maxWidth, 280), 440);
  }, [isMobile]);

  const cardHeight = isMobile ? 420 : 500;
  const fontSize = isMobile ? "22px" : "28px";

  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(isMobile ? 790 : 890);
  }, [isMobile, mode, currentIndex]);

  const finishAssessment = (updatedAnswers) => {
    setFinished(true);
    Streamlit.setComponentValue({
      completed: true,
      answers: updatedAnswers,
    });
  };

  const goNext = (answer) => {
    const updatedAnswers = [...answers, answer];

    if (currentIndex < items.length - 1) {
      setAnswers(updatedAnswers);
      setCurrentIndex(currentIndex + 1);
      setSelectedValue(null);
      setSwipeDirection(null);
    } else {
      finishAssessment(updatedAnswers);
    }
  };

  const sendSwipeDecision = (direction) => {
    if (finished || !currentItem) return;

    setSwipeDirection(direction);

    const value = direction === "right" ? 5 : 1;

    const answer = {
      id: currentItem.id,
      dimension: currentItem.dimension,
      text: currentItem.text,
      decision: direction,
      value,
      condition: "swipe",
    };

    window.setTimeout(() => {
      goNext(answer);
    }, 180);
  };

  const sendLikertDecision = (value) => {
    if (finished || !currentItem) return;

    setSelectedValue(value);

    const answer = {
      id: currentItem.id,
      dimension: currentItem.dimension,
      text: currentItem.text,
      decision: null,
      value,
      condition: "likert",
    };

    window.setTimeout(() => {
      goNext(answer);
    }, 220);
  };

  if (finished) {
    return (
      <div style={centerMessageStyle}>
        Antworten werden verarbeitet …
      </div>
    );
  }

  if (!currentItem) {
    return (
      <div style={centerMessageStyle}>
        Keine Items vorhanden.
      </div>
    );
  }

  const progressPercent = Math.round(((currentIndex + 1) / items.length) * 100);
  const remaining = items.length - (currentIndex + 1);

  const hintText =
    mode === "swipe"
      ? swipeDirection === "right"
        ? "Zustimmung"
        : swipeDirection === "left"
        ? "keine Zustimmung"
        : remaining <= 3
        ? "Fast geschafft"
        : "Aussage bewerten"
      : remaining <= 3
      ? "Fast geschafft"
      : "Antwort auswählen";

  const cardBackground =
    swipeDirection === "right"
      ? "rgba(59, 130, 246, 0.18)"
      : swipeDirection === "left"
      ? "rgba(148, 163, 184, 0.18)"
      : "linear-gradient(180deg, #1e293b 0%, #0f172a 100%)";

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        padding: isMobile ? "16px" : "24px",
        boxSizing: "border-box",
        background:
          "radial-gradient(circle at top, rgba(59,130,246,0.10), transparent 30%), #0f172a",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: isMobile ? "16px" : "22px",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div
        style={{
          width: cardWidth,
          height: "8px",
          background: "rgba(255,255,255,0.08)",
          borderRadius: "999px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressPercent}%`,
            background: "linear-gradient(90deg, #3b82f6, #60a5fa)",
            borderRadius: "999px",
            transition: "width 0.25s ease",
          }}
        />
      </div>

      <div
        style={{
          width: cardWidth,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          color: "#64748b",
          fontSize: isMobile ? "13px" : "14px",
        }}
      >
        <span>
          Frage {currentIndex + 1} von {items.length}
        </span>
        <span>{hintText}</span>
      </div>

      <div style={{ width: cardWidth, textAlign: "left" }}>
        <span
          style={{
            display: "inline-block",
            background: "rgba(59,130,246,0.18)",
            border: "1px solid rgba(59,130,246,0.35)",
            color: "#e0ecff",
            borderRadius: "999px",
            padding: "6px 12px",
            fontSize: isMobile ? "13px" : "14px",
            fontWeight: 600,
            letterSpacing: "0.02em",
          }}
        >
          {currentItem.dimension}
        </span>
      </div>

      {mode === "likert" ? (
        <LikertAssessment
          item={currentItem}
          cardWidth={cardWidth}
          isMobile={isMobile}
          selectedValue={selectedValue}
          onSelect={sendLikertDecision}
        />
      ) : (
        <SwipeAssessment
          item={currentItem}
          cardWidth={cardWidth}
          cardHeight={cardHeight}
          fontSize={fontSize}
          isMobile={isMobile}
          cardBackground={cardBackground}
          onSwipe={sendSwipeDecision}
        />
      )}
    </div>
  );
}

function SwipeAssessment({
  item,
  cardWidth,
  cardHeight,
  fontSize,
  isMobile,
  cardBackground,
  onSwipe,
}) {
  return (
    <>
      <div
        style={{
          width: cardWidth,
          height: cardHeight + 16,
          position: "relative",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <div
          style={{
            position: "absolute",
            width: cardWidth - 14,
            height: cardHeight - 10,
            borderRadius: "26px",
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.04)",
            transform: "translateY(8px) scale(0.985)",
          }}
        />

        <TinderCard
          key={item.id}
          onSwipe={onSwipe}
          preventSwipe={["up", "down"]}
          swipeRequirementType="position"
          swipeThreshold={isMobile ? 50 : 70}
          flickOnSwipe={true}
        >
          <div
            style={{
              background: cardBackground,
              width: cardWidth,
              height: cardHeight,
              borderRadius: "26px",
              boxShadow: "0 22px 52px rgba(0,0,0,0.36)",
              border: "1px solid rgba(255,255,255,0.06)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              padding: isMobile ? "26px 20px" : "34px 30px",
              fontSize,
              fontWeight: 750,
              lineHeight: 1.5,
              letterSpacing: "-0.01em",
              boxSizing: "border-box",
              color: "#e5e7eb",
              cursor: "grab",
              userSelect: "none",
              WebkitUserSelect: "none",
              touchAction: "none",
              transition: "background 0.18s ease",
            }}
          >
            <div
              style={{
                color: "#93c5fd",
                fontSize: isMobile ? "14px" : "15px",
                marginBottom: isMobile ? "14px" : "16px",
                fontWeight: 600,
                letterSpacing: "0.01em",
              }}
            >
              Arbeitspräferenz
            </div>

            <div>{item.text}</div>
          </div>
        </TinderCard>
      </div>

      <div
        style={{
          display: "flex",
          gap: "12px",
          width: cardWidth,
          justifyContent: "center",
          flexWrap: "wrap",
        }}
      >
        <button onClick={() => onSwipe("left")} style={mainButtonStyle(isMobile)}>
          ← Ablehnung
        </button>

        <button onClick={() => onSwipe("right")} style={mainButtonStyle(isMobile)}>
          Zustimmung →
        </button>
      </div>

      <div
        style={{
          textAlign: "center",
          color: "#94a3b8",
          fontSize: isMobile ? "14px" : "15px",
          lineHeight: 1.45,
          maxWidth: cardWidth,
        }}
      >
        Links = eher keine Zustimmung
        <br />
        Rechts = eher Zustimmung
      </div>
    </>
  );
}

function LikertAssessment({ item, cardWidth, isMobile, selectedValue, onSelect }) {
  return (
    <div
      style={{
        width: cardWidth,
        background: "rgba(15, 23, 42, 0.72)",
        border: "1px solid rgba(255,255,255,0.06)",
        borderRadius: "24px",
        padding: isMobile ? "22px 18px" : "28px 30px",
        boxSizing: "border-box",
        boxShadow: "0 18px 42px rgba(0,0,0,0.26)",
      }}
    >
      <div
        style={{
          background:
            "linear-gradient(180deg, rgba(30,41,59,1) 0%, rgba(15,23,42,1) 100%)",
          border: "1px solid rgba(255,255,255,0.06)",
          borderRadius: "24px",
          padding: isMobile ? "26px 20px" : "34px 30px",
          textAlign: "center",
          color: "#e5e7eb",
          minHeight: isMobile ? "250px" : "280px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          boxShadow: "0 20px 50px rgba(0,0,0,0.35)",
        }}
      >
        <div
          style={{
            color: "#93c5fd",
            fontSize: isMobile ? "14px" : "15px",
            marginBottom: "16px",
            fontWeight: 600,
          }}
        >
          Arbeitspräferenz
        </div>

        <div
          style={{
            fontSize: isMobile ? "22px" : "28px",
            fontWeight: 750,
            lineHeight: 1.5,
            letterSpacing: "-0.01em",
          }}
        >
          {item.text}
        </div>
      </div>

      <div
        style={{
          borderTop: "1px solid rgba(255,255,255,0.08)",
          marginTop: "20px",
          paddingTop: "18px",
          textAlign: "center",
        }}
      >
        <div
          style={{
            color: "#f8fafc",
            fontSize: "16px",
            fontWeight: 700,
            marginBottom: "12px",
          }}
        >
          Bitte wähle deine Antwort:
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(5, 1fr)",
            gap: isMobile ? "8px" : "10px",
            maxWidth: "320px",
            margin: "0 auto",
          }}
        >
          {[1, 2, 3, 4, 5].map((value) => (
            <div key={value} style={{ textAlign: "center" }}>
              <div
                style={{
                  color: "#f8fafc",
                  fontWeight: 800,
                  fontSize: "15px",
                  marginBottom: "6px",
                }}
              >
                {value}
              </div>

              <button
                onClick={() => onSelect(value)}
                style={{
                  width: isMobile ? "38px" : "40px",
                  height: isMobile ? "38px" : "40px",
                  borderRadius: "999px",
                  border:
                    selectedValue === value
                      ? "1px solid #3b82f6"
                      : "1px solid rgba(255,255,255,0.16)",
                  background:
                    selectedValue === value
                      ? "rgba(59,130,246,0.35)"
                      : "#1e293b",
                  color: "#e5e7eb",
                  fontSize: "18px",
                  cursor: "pointer",
                  boxShadow: "0 6px 16px rgba(0,0,0,0.18)",
                  transform: selectedValue === value ? "scale(1.08)" : "scale(1)",
                  transition: "all 0.15s ease",
                }}
              >
                {selectedValue === value ? "●" : "○"}
              </button>
            </div>
          ))}
        </div>

        <div
          style={{
            marginTop: "14px",
            color: "#94a3b8",
            fontSize: isMobile ? "13px" : "14px",
            lineHeight: 1.45,
          }}
        >
          1 = stimme überhaupt nicht zu · 2 = stimme eher nicht zu · 3 =
          teils/teils · 4 = stimme eher zu · 5 = stimme voll zu
        </div>
      </div>
    </div>
  );
}

function mainButtonStyle(isMobile) {
  return {
    minWidth: isMobile ? "132px" : "160px",
    padding: isMobile ? "14px 18px" : "14px 22px",
    borderRadius: "14px",
    border: "1px solid rgba(255,255,255,0.10)",
    background: "#1e293b",
    color: "#e5e7eb",
    fontSize: isMobile ? "16px" : "17px",
    fontWeight: 600,
    cursor: "pointer",
    boxShadow: "0 6px 16px rgba(0,0,0,0.18)",
    transition: "all 0.15s ease",
  };
}

const centerMessageStyle = {
  minHeight: "280px",
  width: "100%",
  background: "#0f172a",
  color: "#e5e7eb",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  textAlign: "center",
  fontFamily: "system-ui, sans-serif",
};

export default withStreamlitConnection(App);