export function getPhaseName(phase) {
  if (phase === "FLOP3.0") return "RIVER";
  if (phase === "FLOP4.0") return "TURN";
  return phase;
}

export function getHandEquity(value, suffix) {
  let handEquity = value;
  if (!isNaN(handEquity)) {
    handEquity = handEquity.toFixed(2);
    handEquity = `${handEquity}${suffix}`;
  } else {
    handEquity = "";
  }
  return handEquity;
}
