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

const cardHeight =
  mode === "swipe"
    ? isSmallMobile
      ? 430
      : isMobile
      ? 455
      : 500
    : isSmallMobile
    ? 360
    : isMobile
    ? 390
    : 500;

const fontSize = isSmallMobile ? "19px" : isMobile ? "20px" : "28px";

useEffect(() => {
  Streamlit.setComponentReady();

  const frameHeight =
    mode === "swipe"
      ? isSmallMobile
        ? 640
        : isMobile
        ? 675
        : 760
      : isSmallMobile
      ? 595
      : isMobile
      ? 625
      : 760;

  Streamlit.setFrameHeight(frameHeight);
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
          height: cardHeight + 14,
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
            borderRadius: isMobile ? "28px" : "26px",
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
          swipeThreshold={isMobile ? 48 : 70}
          flickOnSwipe={true}
        >
          <div
            style={{
              background: cardBackground,
              width: cardWidth,
              height: cardHeight,
              position: "relative",
              borderRadius: isMobile ? "28px" : "26px",
              boxShadow: "0 22px 52px rgba(49,92,99,0.16)",
              border: `1px solid ${colors.border}`,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              padding: isSmallMobile
                ? "28px 18px 58px"
                : isMobile
                ? "30px 20px 60px"
                : "34px 30px",
              fontSize,
              fontWeight: 750,
              lineHeight: 1.45,
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
                bottom: isMobile ? "22px" : "22px",
                color: colors.primary,
                fontSize: isMobile ? "11px" : "13px",
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
                bottom: isMobile ? "22px" : "22px",
                color: colors.primary,
                fontSize: isMobile ? "11px" : "13px",
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
  const statementFontSize = isSmallMobile ? "18px" : isMobile ? "19px" : "26px";
  const optionNumberSize = isSmallMobile ? "16px" : isMobile ? "17px" : "24px";

  return (
    <div
      style={{
        width: cardWidth,
        background: colors.card,
        border: `1px solid ${colors.border}`,
        borderRadius: isMobile ? "24px" : "24px",
        padding: isSmallMobile ? "16px 13px" : isMobile ? "18px 15px" : "28px 30px",
        boxSizing: "border-box",
        boxShadow: "0 18px 42px rgba(49,92,99,0.13)",
      }}
    >
      <div
        style={{
          background: "linear-gradient(180deg, #FFFFFF 0%, #F8F4ED 100%)",
          border: `1px solid ${colors.border}`,
          borderRadius: isMobile ? "22px" : "24px",
          padding: isSmallMobile ? "30px 16px" : isMobile ? "34px 18px" : "34px 30px",
          textAlign: "center",
          color: colors.text,
          minHeight: isSmallMobile ? "230px" : isMobile ? "255px" : "250px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          boxShadow: "0 18px 42px rgba(49,92,99,0.10)",
        }}
      >
        <div
          style={{
            fontSize: statementFontSize,
            fontWeight: 750,
            lineHeight: 1.45,
            letterSpacing: "-0.01em",
          }}
        >
          {item.text}
        </div>
      </div>

      <div
        style={{
          borderTop: `1px solid ${colors.border}`,
          marginTop: isMobile ? "16px" : "20px",
          paddingTop: isMobile ? "15px" : "18px",
          textAlign: "center",
        }}
      >
        <div
          style={{
            color: colors.primary,
            fontSize: isSmallMobile ? "13px" : isMobile ? "14px" : "16px",
            fontWeight: 750,
            marginBottom: isMobile ? "10px" : "12px",
            lineHeight: 1.3,
          }}
        >
          Wie gut passt die Aussage zu dir?
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(5, 1fr)",
            gap: isSmallMobile ? "4px" : isMobile ? "6px" : "10px",
            maxWidth: isMobile ? "300px" : "320px",
            margin: "0 auto",
          }}
        >
          {[1, 2, 3, 4, 5].map((value) => (
            <div key={value} style={{ textAlign: "center" }}>
              <div
                style={{
                  color: colors.text,
                  fontWeight: 750,
                  fontSize: optionNumberSize,
                  marginBottom: isMobile ? "5px" : "6px",
                  lineHeight: 1.1,
                }}
              >
                {value}
              </div>

              <button
                onClick={() => onSelect(value)}
                aria-label={`Antwort ${value}`}
                style={{
                  width: isSmallMobile ? "32px" : isMobile ? "34px" : "40px",
                  height: isSmallMobile ? "32px" : isMobile ? "34px" : "40px",
                  borderRadius: "999px",
                  border:
                    selectedValue === value
                      ? `2px solid ${colors.primary}`
                      : `1px solid ${colors.border}`,
                  background:
                    selectedValue === value ? colors.primary : colors.soft,
                  color: selectedValue === value ? "#FFFFFF" : colors.primary,
                  fontSize: isMobile ? "15px" : "18px",
                  cursor: "pointer",
                  boxShadow:
                    selectedValue === value
                      ? "0 8px 18px rgba(49,92,99,0.20)"
                      : "0 5px 12px rgba(49,92,99,0.07)",
                  transform:
                    selectedValue === value ? "scale(1.06)" : "scale(1)",
                  transition: "all 0.15s ease",
                }}
              >
                {selectedValue === value ? "●" : "○"}
              </button>
            </div>
          ))}
        </div>

        {!isMobile && (
          <div
            style={{
              marginTop: "14px",
              color: colors.muted,
              fontSize: "14px",
              lineHeight: 1.45,
            }}
          >
            1 = passt gar nicht · 3 = teils/teils · 5 = passt sehr gut
          </div>
        )}
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