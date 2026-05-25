import React, { useEffect, useMemo, useState } from "react";
import TinderCard from "react-tinder-card";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

const colors = {
  bg: "#FAF7F2",
  card: "#FFFFFF",
  primary: "#315C63",
  primaryDark: "#1F3A5F",
  accent: "#F2B872",
  text: "#303030",
  muted: "#667085",
  border: "#E5E1DA",
  soft: "#F8F4ED",
  success: "#6BAA75",
  danger: "#D98282",
};

function App({ args }) {
  const items = args?.items || [];
  const mode = args?.mode || "swipe";

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [swipeDirection, setSwipeDirection] = useState(null);
  const [selectedValue, setSelectedValue] = useState(null);
  const [finished, setFinished] = useState(false);

  const isMobile = typeof window !== "undefined" && window.innerWidth < 700;
  const isSmallMobile = typeof window !== "undefined" && window.innerWidth < 390;
  const currentItem = items[currentIndex];

  const cardWidth = useMemo(() => {
  if (typeof window === "undefined") return 340;

  const sidePadding = window.innerWidth < 390 ? 22 : 32;
  const maxWidth = isMobile ? window.innerWidth - sidePadding : 440;

  return Math.min(Math.max(maxWidth, 286), 440);
}, [isMobile]);

const cardHeight = isSmallMobile ? 370 : isMobile ? 400 : 500;
const fontSize = isSmallMobile ? "19px" : isMobile ? "21px" : "28px";

  useEffect(() => {
  Streamlit.setComponentReady();
  Streamlit.setFrameHeight(isSmallMobile ? 620 : isMobile ? 660 : 760);
}, [isMobile, isSmallMobile, mode, currentIndex]);

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
    return <div style={centerMessageStyle}>Antworten werden verarbeitet …</div>;
  }

  if (!currentItem) {
    return <div style={centerMessageStyle}>Keine Items vorhanden.</div>;
  }

  const progressPercent = Math.round(((currentIndex + 1) / items.length) * 100);
  const remaining = items.length - (currentIndex + 1);

  const hintText =
    mode === "swipe"
      ? swipeDirection === "right"
        ? "Passt eher"
        : swipeDirection === "left"
        ? "Passt eher nicht"
        : remaining <= 3
        ? "Fast geschafft"
        : "Aussage bewerten"
      : remaining <= 3
      ? "Fast geschafft"
      : "Wert auswählen";

  const cardBackground =
    swipeDirection === "right"
      ? "linear-gradient(180deg, rgba(107,170,117,0.20), #FFFFFF 70%)"
      : swipeDirection === "left"
      ? "linear-gradient(180deg, rgba(217,130,130,0.20), #FFFFFF 70%)"
      : "linear-gradient(180deg, #FFFFFF 0%, #F8F4ED 100%)";

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        padding: isSmallMobile ? "8px 10px 12px" : isMobile ? "10px 12px 14px" : "10px 24px 18px",
        boxSizing: "border-box",
        background:
            "linear-gradient(180deg, #FAF7F2 0%, #F8F4ED 100%)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-start",
        alignItems: "center",
        gap: isSmallMobile ? "8px" : isMobile ? "10px" : "14px",
        fontFamily: "Arial, system-ui, sans-serif",
      }}
    >
      <div
        style={{
          width: cardWidth,
          height: "8px",
          background: colors.border,
          borderRadius: "999px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressPercent}%`,
            background: `linear-gradient(90deg, ${colors.primary}, ${colors.accent})`,
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
          color: colors.muted,
          fontSize: isMobile ? "13px" : "14px",
        }}
      >
        <span>
          Frage {currentIndex + 1} von {items.length}
        </span>
        <span>{hintText}</span>
      </div>

      {mode === "likert" ? (
        <LikertAssessment
          item={currentItem}
          cardWidth={cardWidth}
          isMobile={isMobile}
          isSmallMobile={isSmallMobile}
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
  isSmallMobile={isSmallMobile}
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
  isSmallMobile,
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
            background: "#F3EEE7",
            border: `1px solid ${colors.border}`,
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
              position: "relative",
              borderRadius: "26px",
              boxShadow: "0 22px 52px rgba(49,92,99,0.16)",
              border: `1px solid ${colors.border}`,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              padding: isSmallMobile ? "24px 16px 44px" : isMobile ? "26px 18px 46px" : "34px 30px",
              fontSize,
              fontWeight: 750,
              lineHeight: 1.5,
              letterSpacing: "-0.01em",
              boxSizing: "border-box",
              color: colors.text,
              cursor: "grab",
              userSelect: "none",
              WebkitUserSelect: "none",
              touchAction: "none",
              transition: "background 0.18s ease",
            }}
          >

            <div
  style={{
    position: "absolute",
    left: isMobile ? "18px" : "24px",
    bottom: isMobile ? "18px" : "22px",
    color: colors.primary,
    fontSize: isMobile ? "12px" : "13px",
    fontWeight: 750,
    opacity: 0.78,
  }}
>
  Passt eher nicht
</div>

<div
  style={{
    position: "absolute",
    right: isMobile ? "18px" : "24px",
    bottom: isMobile ? "18px" : "22px",
    color: colors.primary,
    fontSize: isMobile ? "12px" : "13px",
    fontWeight: 750,
    opacity: 0.78,
  }}
>
  Passt eher
</div>

<div>{item.text}</div>
          </div>
        </TinderCard>
      </div>

    </>
  );
}

function LikertAssessment({
  item,
  cardWidth,
  isMobile,
  isSmallMobile,
  selectedValue,
  onSelect,
}) {
  return (
    <div
      style={{
        width: cardWidth,
        background: colors.card,
        border: `1px solid ${colors.border}`,
        borderRadius: "24px",
        padding: isSmallMobile ? "18px 14px" : isMobile ? "20px 16px" : "28px 30px",
        boxSizing: "border-box",
        boxShadow: "0 18px 42px rgba(49,92,99,0.13)",
      }}
    >
      <div
        style={{
          background: "linear-gradient(180deg, #FFFFFF 0%, #F8F4ED 100%)",
          border: `1px solid ${colors.border}`,
          borderRadius: "24px",
          padding: isSmallMobile ? "24px 16px" : isMobile ? "26px 18px" : "34px 30px",
          textAlign: "center",
          color: colors.text,
          minHeight: isSmallMobile ? "190px" : isMobile ? "215px" : "250px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          boxShadow: "0 20px 50px rgba(49,92,99,0.12)",
        }}
      >

        <div
          style={{
            fontSize: isSmallMobile ? "18px" : isMobile ? "20px" : "26px",
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
          borderTop: `1px solid ${colors.border}`,
          marginTop: "20px",
          paddingTop: "18px",
          textAlign: "center",
        }}
      >
        <div
          style={{
            color: colors.primary,
            fontSize: "16px",
            fontWeight: 750,
            marginBottom: "12px",
          }}
        >
          Wie gut passt die Aussage zu dir?
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(5, 1fr)",
            gap: isSmallMobile ? "5px" : isMobile ? "8px" : "10px",
            maxWidth: "320px",
            margin: "0 auto",
          }}
        >
          {[1, 2, 3, 4, 5].map((value) => (
            <div key={value} style={{ textAlign: "center" }}>
              <div
                style={{
                  color: colors.text,
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
                  width: isSmallMobile ? "34px" : isMobile ? "38px" : "40px",
                  height: isSmallMobile ? "34px" : isMobile ? "38px" : "40px",
                  borderRadius: "999px",
                  border:
                    selectedValue === value
                      ? `1px solid ${colors.primary}`
                      : `1px solid ${colors.border}`,
                  background:
                    selectedValue === value ? colors.primary : colors.soft,
                  color: selectedValue === value ? "#FFFFFF" : colors.primary,
                  fontSize: "18px",
                  cursor: "pointer",
                  boxShadow:
                    selectedValue === value
                      ? "0 8px 20px rgba(49,92,99,0.22)"
                      : "0 6px 16px rgba(49,92,99,0.08)",
                  transform:
                    selectedValue === value ? "scale(1.08)" : "scale(1)",
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
            color: colors.muted,
            fontSize: isMobile ? "13px" : "14px",
            lineHeight: 1.45,
          }}
        >
          1 = passt gar nicht · 3 = teils/teils · 5 = passt sehr gut
        </div>
      </div>
    </div>
  );
}

const centerMessageStyle = {
  minHeight: "280px",
  width: "100%",
  background: "#FAF7F2",
  color: "#303030",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  textAlign: "center",
  fontFamily: "Arial, system-ui, sans-serif",
};

export default withStreamlitConnection(App);