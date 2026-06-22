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

  if (mode === "closing_questionnaire" || mode === "result_assessment") {
    return;
  }

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

if (mode === "closing_questionnaire") {
  return (
    <ClosingQuestionnaire
      blocks={items}
      isMobile={isMobile}
      isSmallMobile={isSmallMobile}
    />
  );
}

if (mode === "result_assessment") {
  return (
    <ResultAssessment
      isMobile={isMobile}
      isSmallMobile={isSmallMobile}
    />
  );
}

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
  const optionNumberSize = isSmallMobile ? "15px" : isMobile ? "16px" : "22px";

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
          minHeight: isSmallMobile ? "220px" : isMobile ? "245px" : "250px",
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
                  marginBottom: isMobile ? "4px" : "6px",
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

function ClosingQuestionnaire({ blocks, isMobile, isSmallMobile }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [showGiveawayModal, setShowGiveawayModal] = useState(false);
  const [giveawayEmail, setGiveawayEmail] = useState("");
  const [giveawayError, setGiveawayError] = useState("");

  const totalSteps = blocks.length;
  const currentBlock = blocks[currentStep];
  const coverB64 = blocks?.[0]?.cover_b64 || "";

  useEffect(() => {
  Streamlit.setComponentReady();

  const itemCount = currentBlock?.items?.length || 0;

  const frameHeight = isMobile
    ? 470 + itemCount * 110
    : 470 + itemCount * 96;

  Streamlit.setFrameHeight(frameHeight);
}, [currentStep, currentBlock, isMobile]);

  if (submitted) {
    return <div style={centerMessageStyle}>Antworten werden verarbeitet …</div>;
  }

  if (!currentBlock) {
    return <div style={centerMessageStyle}>Keine Fragen vorhanden.</div>;
  }

  const progressPercent = Math.round(((currentStep + 1) / totalSteps) * 100);

  const sectionText = currentBlock.section || `Abschnitt ${currentStep + 1}`;
  const sectionParts = sectionText.includes(". ")
    ? sectionText.split(". ")
    : [`${currentStep + 1}`, sectionText];

  const sectionLetter = sectionParts[0];
  const sectionTitle = sectionParts.slice(1).join(". ");

  const currentKeys = currentBlock.items.map((item) => item[0]);
  const currentComplete = currentKeys.every((key) => answers[key] !== undefined);

  const selectAnswer = (key, value) => {
    setAnswers((previous) => ({
      ...previous,
      [key]: value,
    }));
  };

  const goBack = () => {
    if (currentStep > 0) {
      setCurrentStep((step) => step - 1);
    }
  };

  const goNext = () => {
  if (!currentComplete) return;

  if (currentStep < totalSteps - 1) {
    setCurrentStep((step) => step + 1);
    return;
  }

  setShowGiveawayModal(true);
};

const finishWithoutGiveaway = () => {
  setSubmitted(true);
  Streamlit.setComponentValue({
    completed: true,
    answers,
    giveaway_participation: false,
    giveaway_email: "",
  });
};

const finishWithGiveaway = () => {
  const trimmedEmail = giveawayEmail.trim();
  const emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmedEmail);

  if (!emailIsValid) {
    setGiveawayError("Bitte gib eine gültige E-Mail-Adresse ein.");
    return;
  }

  setSubmitted(true);
  Streamlit.setComponentValue({
    completed: true,
    answers,
    giveaway_participation: true,
    giveaway_email: trimmedEmail,
  });
};

  return (
  <div
    style={{
      width: "100%",
      minHeight: "auto",
      boxSizing: "border-box",
      background: "linear-gradient(180deg, #FAF7F2 0%, #F8F4ED 100%)",
      fontFamily: '"Source Sans Pro", "Source Sans 3", Arial, Helvetica, sans-serif',
      color: colors.text,
      padding: isMobile ? "12px 10px 120px" : "20px 24px 34px",
      display: "flex",
      justifyContent: "flex-start",
      overflow: "visible",
    }}
  >
    <style>
  {`
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800;900&display=swap');

    * {
      font-family: "Source Sans 3", "Source Sans Pro", Arial, Helvetica, sans-serif;
    }
  `}
</style>
      <div
        style={{
          width: "100%",
          maxWidth: isMobile ? "100%" : "860px",
          margin: "0 auto",
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: isMobile ? "10px" : "16px",
          }}
        >
          <div
            style={{
              color: colors.primary,
              fontSize: isMobile ? "28px" : "38px",
              fontWeight: 800,
              letterSpacing: "-0.045em",
              lineHeight: 1.08,
              marginBottom: "8px",
            }}
          >
            Deine Einschätzung
          </div>

          <div
            style={{
              color: colors.muted,
              fontSize: isMobile ? "13px" : "15px",
              fontWeight: 600,
              marginBottom: isMobile ? "9px" : "13px",
            }}
          >
            Abschnitt {currentStep + 1} von {totalSteps}
          </div>

          <div
            style={{
              width: isMobile ? "82%" : "420px",
              height: "7px",
              margin: "0 auto",
              borderRadius: "999px",
              background: "rgba(49,92,99,0.10)",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progressPercent}%`,
                height: "100%",
                borderRadius: "999px",
                background: `linear-gradient(90deg, ${colors.primary}, ${colors.accent})`,
                transition: "width 0.25s ease",
              }}
            />
          </div>
        </div>

        <div
          style={{
            background: colors.card,
            border: `1px solid ${colors.border}`,
            borderRadius: isMobile ? "24px" : "28px",
            boxShadow: "0 18px 42px rgba(49,92,99,0.10)",
            padding: isMobile ? "16px 14px" : "22px 26px",
            marginBottom: isMobile ? "12px" : "16px",
            textAlign: "center",
          }}
        >
          <div
            style={{
              display: "inline-block",
              padding: "5px 10px",
              borderRadius: "999px",
              background: "rgba(49,92,99,0.07)",
              color: colors.primary,
              fontSize: isMobile ? "12px" : "13px",
              fontWeight: 700,
              letterSpacing: "0",
              textTransform: "none",
              marginBottom: "9px",
            }}
        >
  Abschnitt {sectionLetter}
</div>

          <div
            style={{
              color: colors.primary,
              fontSize: isMobile ? "21px" : "25px",
              fontWeight: 800,
              letterSpacing: "-0.035em",
              lineHeight: 1.14,
              marginBottom: "8px",
            }}
          >
            {sectionTitle}
          </div>

          <div
            style={{
              color: colors.text,
              fontSize: isMobile ? "14px" : "16px",
              lineHeight: 1.45,
              marginBottom: isMobile ? "13px" : "18px",
            }}
          >
            {currentBlock.prompt ||
              "Bitte bewerte die folgenden Aussagen danach, wie sehr du ihnen zustimmst."}
          </div>

          <ScaleLegend isMobile={isMobile} />
        </div>

        <div
          style={{
            background: colors.card,
            border: `1px solid ${colors.border}`,
            borderRadius: isMobile ? "24px" : "28px",
            boxShadow: "0 20px 48px rgba(49,92,99,0.11)",
            padding: isMobile ? "8px" : "12px",
          }}
        >
          {currentBlock.items.map(([key, text], index) => (
            <ClosingQuestionItem
              key={key}
              itemKey={key}
              text={text}
              value={answers[key]}
              onSelect={selectAnswer}
              isMobile={isMobile}
              isSmallMobile={isSmallMobile}
              isLast={index === currentBlock.items.length - 1}
            />
          ))}
        </div>

        <div
          style={{
            marginTop: isMobile ? "13px" : "18px",
            display: "grid",
            gridTemplateColumns:
              currentStep > 0 ? "minmax(0, 1fr) minmax(0, 1fr)" : "1fr",
            gap: isMobile ? "10px" : "14px",
            alignItems: "center",
          }}
        >
          {currentStep > 0 && (
            <button
              type="button"
              onClick={goBack}
              style={{
                fontFamily: '"Source Sans Pro", "Source Sans 3", Arial, Helvetica, sans-serif',
                height: isMobile ? "46px" : "50px",
                borderRadius: "999px",
                border: `1.5px solid rgba(49,92,99,0.34)`,
                background: "rgba(255,255,255,0.42)",
                color: colors.primary,
                fontSize: isMobile ? "14px" : "15px",
                fontWeight: 800,
                cursor: "pointer",
                boxShadow: "none",
              }}
            >
              ← Zurück
            </button>
          )}

          <button
            type="button"
            onClick={goNext}
            disabled={!currentComplete}
            style={{
              height: isMobile ? "46px" : "50px",
              borderRadius: "999px",
              border: `1px solid ${colors.primary}`,
              background: currentComplete
                ? colors.primary
                : "rgba(49,92,99,0.32)",
              color: "#FFFFFF",
              fontSize: isMobile ? "14px" : "15px",
              fontWeight: 850,
              cursor: currentComplete ? "pointer" : "not-allowed",
              boxShadow: currentComplete
                ? "0 12px 26px rgba(49,92,99,0.18)"
                : "none",
              transition: "all 0.15s ease",
            }}
          >
            {currentStep < totalSteps - 1 ? "Weiter →" : "Abschließen"}
          </button>
        </div>

        {!currentComplete && (
          <div
            style={{
              fontFamily: '"Source Sans Pro", "Source Sans 3", Arial, Helvetica, sans-serif',
              color: colors.muted,
              textAlign: "center",
              fontSize: isMobile ? "12px" : "14px",
              marginTop: "9px",
              lineHeight: 1.35,
            }}
          >
            Bitte beantworte alle Aussagen, um fortzufahren.
          </div>
        )}
      </div>

      {showGiveawayModal && (
  <GiveawayModal
    isMobile={isMobile}
    coverB64={coverB64}
    email={giveawayEmail}
    setEmail={setGiveawayEmail}
    error={giveawayError}
    setError={setGiveawayError}
    onConfirm={finishWithGiveaway}
    onSkip={finishWithoutGiveaway}
  />
)}

    </div>
  );
}

function GiveawayModal({
  isMobile,
  coverB64,
  email,
  setEmail,
  error,
  setError,
  onConfirm,
  onSkip,
}) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 9999,
        background: "rgba(250,247,242,0.88)",
        backdropFilter: "blur(8px)",
        WebkitBackdropFilter: "blur(8px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: isMobile ? "18px 14px" : "28px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: isMobile ? "390px" : "560px",
          background:
            "radial-gradient(circle at top left, rgba(49,92,99,0.055), transparent 34%), radial-gradient(circle at bottom right, rgba(242,184,114,0.10), transparent 34%), rgba(255,255,255,0.98)",
          border: `1px solid rgba(49,92,99,0.14)`,
          borderRadius: isMobile ? "26px" : "30px",
          boxShadow: "0 24px 60px rgba(49,92,99,0.18)",
          padding: isMobile ? "22px 18px 20px" : "28px 30px 26px",
          boxSizing: "border-box",
          textAlign: "center",
        }}
      >
        {coverB64 && (
          <img
            src={`data:image/png;base64,${coverB64}`}
            alt="Crashkurs People, Culture & Change"
            style={{
              width: isMobile ? "82px" : "96px",
              height: "auto",
              display: "block",
              margin: "0 auto 14px",
              borderRadius: "9px",
              boxShadow: "0 10px 24px rgba(49,92,99,0.16)",
            }}
          />
        )}

        <div
          style={{
            color: colors.primary,
            fontSize: isMobile ? "24px" : "30px",
            lineHeight: 1.08,
            fontWeight: 850,
            letterSpacing: "-0.045em",
            marginBottom: "10px",
          }}
        >
          Möchtest du an der Verlosung teilnehmen?
        </div>

        <div
          style={{
            color: colors.text,
            fontSize: isMobile ? "14px" : "16px",
            lineHeight: 1.48,
            marginBottom: "12px",
          }}
        >
          Als Dankeschön für deine Teilnahme kannst du freiwillig an der Verlosung von einem von fünf Exemplaren von{" "}
          <strong>„Crashkurs People, Culture & Change“</strong> teilnehmen.
        </div>

        <div
          style={{
            color: colors.muted,
            fontSize: isMobile ? "13px" : "14px",
            lineHeight: 1.42,
            marginBottom: "16px",
          }}
        >
          Deine E-Mail-Adresse wird ausschließlich für die Verlosung verwendet und getrennt von deinen Studienantworten gespeichert.
        </div>

        <div
          style={{
            textAlign: "left",
            marginBottom: "12px",
          }}
        >
          <label
            style={{
              display: "block",
              color: colors.primary,
              fontSize: isMobile ? "13px" : "14px",
              fontWeight: 800,
              marginBottom: "7px",
            }}
          >
            E-Mail-Adresse für die Verlosung
          </label>

          <input
            type="email"
            value={email}
            onChange={(event) => {
              setEmail(event.target.value);
              setError("");
            }}
            placeholder="name@example.com"
            style={{
              width: "100%",
              boxSizing: "border-box",
              border: `1px solid ${error ? colors.danger : colors.border}`,
              borderRadius: "16px",
              padding: isMobile ? "12px 13px" : "13px 14px",
              fontSize: isMobile ? "14px" : "15px",
              outline: "none",
              color: colors.text,
              background: "#FFFFFF",
              boxShadow: "0 8px 18px rgba(49,92,99,0.06)",
            }}
          />

          {error && (
            <div
              style={{
                color: colors.danger,
                fontSize: "12px",
                lineHeight: 1.35,
                marginTop: "7px",
                fontWeight: 700,
              }}
            >
              {error}
            </div>
          )}
        </div>

        <button
          type="button"
          onClick={onConfirm}
          style={{
            width: "100%",
            minHeight: isMobile ? "46px" : "50px",
            borderRadius: "999px",
            border: `1px solid ${colors.primary}`,
            background: colors.primary,
            color: "#FFFFFF",
            fontSize: isMobile ? "14px" : "15px",
            fontWeight: 850,
            cursor: "pointer",
            boxShadow: "0 12px 26px rgba(49,92,99,0.18)",
            marginBottom: "10px",
          }}
        >
          Teilnahme speichern & Studie abschließen
        </button>

        <button
          type="button"
          onClick={onSkip}
          style={{
            width: "100%",
            minHeight: isMobile ? "44px" : "48px",
            borderRadius: "999px",
            border: `1.5px solid rgba(49,92,99,0.30)`,
            background: "rgba(255,255,255,0.55)",
            color: colors.primary,
            fontSize: isMobile ? "14px" : "15px",
            fontWeight: 800,
            cursor: "pointer",
            boxShadow: "none",
          }}
        >
          Ohne Teilnahme abschließen
        </button>
      </div>
    </div>
  );
}

function ScaleLegend({ isMobile }) {
  const labels = [
    ["1", "stimme nicht zu"],
    ["2", "stimme eher nicht zu"],
    ["3", "stimme eher zu"],
    ["4", "stimme zu"],
  ];

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
        gap: isMobile ? "7px" : "12px",
      }}
    >
      {labels.map(([number, label]) => (
        <div
          key={number}
          style={{
            background: colors.soft,
            border: `1px solid ${colors.border}`,
            borderRadius: isMobile ? "14px" : "16px",
            padding: isMobile ? "9px 4px" : "12px 8px",
            textAlign: "center",
            minHeight: isMobile ? "58px" : "66px",
            boxSizing: "border-box",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              color: colors.primary,
              fontSize: isMobile ? "14px" : "17px",
              fontWeight: 850,
              lineHeight: 1.1,
              marginBottom: "4px",
            }}
          >
            {number}
          </div>
          <div
            style={{
              color: colors.muted,
              fontSize: isMobile ? "10px" : "12px",
              lineHeight: 1.18,
              fontWeight: 600,
            }}
          >
            {label}
          </div>
        </div>
      ))}
    </div>
  );
}

function ClosingQuestionItem({
  itemKey,
  text,
  value,
  onSelect,
  isMobile,
  isSmallMobile,
  isLast,
}) {
  return (
    <div
      style={{
        display: isMobile ? "grid" : "grid",
        gridTemplateColumns: isMobile ? "1fr auto" : "minmax(0, 1fr) 360px",
        gap: isMobile ? "10px" : "18px",
        alignItems: "center",
        background: "#FFFFFF",
        border: `1px solid rgba(49,92,99,0.08)`,
        borderRadius: isMobile ? "18px" : "20px",
        padding: isMobile ? "14px 10px" : "12px 14px",
        marginBottom: isLast ? 0 : isMobile ? "9px" : "9px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          color: colors.text,
          fontSize: isSmallMobile ? "13px" : isMobile ? "14px" : "16px",
          lineHeight: 1.38,
          fontWeight: 550,
          letterSpacing: "-0.01em",
        }}
      >
        {text}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: isMobile ? "5px" : "0",
          width: isMobile ? "132px" : "100%",
          border: isMobile ? "none" : `1px solid ${colors.border}`,
          borderRadius: isMobile ? "999px" : "12px",
          overflow: "visible",
          background: isMobile ? "transparent" : colors.soft,
        }}
      >
        {[1, 2, 3, 4].map((option) => {
          const selected = value === option;

          return (
            <button
              key={option}
              type="button"
              onClick={() => onSelect(itemKey, option)}
              aria-label={`Antwort ${option}`}
              style={{
                fontFamily: '"Source Sans 3", "Source Sans Pro", Arial, Helvetica, sans-serif',
                width: isMobile ? "31px" : "auto",
                height: isMobile ? "31px" : "38px",
                minWidth: isMobile ? "31px" : "auto",
                borderRadius: isMobile ? "999px" : "0",
                border: isMobile
                  ? selected
                    ? `1px solid ${colors.primary}`
                    : `1px solid ${colors.border}`
                  : "none",
                borderRight:
                  !isMobile && option < 4
                    ? `1px solid ${colors.border}`
                    : "none",
                background: selected ? colors.success : "#FFFFFF",
                color: selected ? "#FFFFFF" : colors.primary,
                fontSize: isMobile ? "12px" : "14px",
                fontWeight: 850,
                cursor: "pointer",
                transition: "all 0.14s ease",
                boxShadow:
                  selected && isMobile
                    ? "0 6px 14px rgba(49,92,99,0.18)"
                    : "none",
              }}
            >
              {option}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function ResultAssessment({ isMobile, isSmallMobile }) {
  const [selectedValue, setSelectedValue] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const options = [
    "Sehr passend",
    "Eher passend",
    "Teils / teils",
    "Eher nicht passend",
    "Gar nicht passend",
  ];

  useEffect(() => {
    Streamlit.setComponentReady();

    const frameHeight = isMobile ? 520 : 350;
    Streamlit.setFrameHeight(frameHeight);
  }, [isMobile]);

  if (submitted) {
    return <div style={centerMessageStyle}>Antwort wird verarbeitet …</div>;
  }

  const submitAssessment = () => {
    if (!selectedValue) return;

    setSubmitted(true);
    Streamlit.setComponentValue({
      completed: true,
      value: selectedValue,
    });
  };

  return (
    <div
      style={{
        width: "100%",
        boxSizing: "border-box",
        background: "transparent",
        fontFamily: '"Source Sans 3", "Source Sans Pro", Arial, Helvetica, sans-serif',
        color: colors.text,
        padding: isMobile ? "8px 10px 32px" : "8px 0 18px",
        overflow: "visible",
      }}
    >
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800;900&display=swap');

          * {
            font-family: "Source Sans 3", "Source Sans Pro", Arial, Helvetica, sans-serif;
          }
        `}
      </style>

      <div
        style={{
          width: "100%",
          maxWidth: isMobile ? "100%" : "860px",
          margin: "0 auto",
          background:
            "radial-gradient(circle at top left, rgba(49,92,99,0.045), transparent 34%), radial-gradient(circle at bottom right, rgba(242,184,114,0.08), transparent 34%), rgba(255,255,255,0.97)",
          border: `1px solid rgba(49,92,99,0.12)`,
          borderRadius: isMobile ? "24px" : "30px",
          boxShadow: "0 20px 48px rgba(49,92,99,0.11)",
          padding: isMobile ? "20px 16px 18px" : "26px 28px 24px",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            color: colors.primary,
            fontSize: isMobile ? "22px" : "32px",
            fontWeight: 800,
            letterSpacing: "-0.04em",
            lineHeight: 1.08,
            marginBottom: "8px",
            textAlign: isMobile ? "center" : "left",
          }}
        >
          Deine erste Einschätzung
        </div>

        <div
          style={{
            color: colors.text,
            fontSize: isMobile ? "12px" : "16px",
            lineHeight: 1.4,
            marginBottom: isMobile ? "16px" : "20px",
            textAlign: isMobile ? "center" : "left",
          }}
        >
          Wie passend erscheint dir das angezeigte Ergebnis?
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: isMobile
              ? "1fr"
              : "repeat(5, minmax(0, 1fr))",
            gap: isMobile ? "6px" : "10px",
            marginBottom: isMobile ? "18px" : "22px",
          }}
        >
          {options.map((option) => {
            const selected = selectedValue === option;

            return (
              <button
                key={option}
                type="button"
                onClick={() => setSelectedValue(option)}
                style={{
                  minHeight: isMobile ? "40px" : "60px",
                  borderRadius: isMobile ? "17px" : "18px",
                  border: selected
                    ? `2px solid ${colors.primary}`
                    : `1px solid ${colors.border}`,
                  background: selected
                    ? "rgba(107,170,117,0.18)"
                    : colors.soft,
                  color: selected ? colors.primary : colors.text,
                  fontSize: isMobile ? "13px" : "15px",
                  fontWeight: selected ? 700 : 600,
                  cursor: "pointer",
                  boxShadow: selected
                    ? "0 10px 22px rgba(49,92,99,0.12)"
                    : "0 6px 14px rgba(49,92,99,0.045)",
                  transition: "all 0.15s ease",
                  padding: isMobile ? "0 10px" : "0 8px",
                  textAlign: "center",
                }}
              >
                {option}
              </button>
            );
          })}
        </div>

        <button
          type="button"
          onClick={submitAssessment}
          disabled={!selectedValue}
          style={{
            width: isMobile ? "100%" : "min(520px, 76%)",
            height: isMobile ? "46px" : "50px",
            display: "block",
            margin: "0 auto",
            borderRadius: "999px",
            border: `1px solid ${colors.primary}`,
            background: selectedValue
            ? colors.primary
            : "rgba(49,92,99,0.32)",
            color: "#FFFFFF",
            fontSize: isMobile ? "14px" : "15px",
            fontWeight: 700,
            cursor: selectedValue ? "pointer" : "not-allowed",
            boxShadow: "none",
            transition: "all 0.15s ease",
          }}
        >
          Zum Abschlussfragebogen
        </button>

        {!selectedValue && (
          <div
            style={{
              color: colors.muted,
              textAlign: "center",
              fontSize: isMobile ? "12px" : "13px",
              lineHeight: 1.35,
              marginTop: "10px",
            }}
          >
            Bitte wähle eine Einschätzung aus, um fortzufahren.
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