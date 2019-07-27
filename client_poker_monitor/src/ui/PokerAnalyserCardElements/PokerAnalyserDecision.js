import React from "react";
import styled from "styled-components/native";
import { getHandEquity } from "../../helpers/utils";

const HandEquityText = styled.Text`
  font-size: ${props => parseInt((18 / 410) * props.totalWidth)};
  text-align: center;
  color: #000000;
`;

const DecisionText = styled.Text`
  font-size: ${props => parseInt((36 / 410) * props.totalWidth)};
  font-weight: 800;
  text-align: center;
  color: #000000;
`;

const PokerAnalyserDecisionView = styled.View`
  width: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20;
`;

export default PokerAnalyserDecision = props => {
  const handEquity = getHandEquity(
    props.table.hand_analisys.result[0][1] * 100,
    `% for a winning hand`
  );

  return (
    <PokerAnalyserDecisionView>
      <DecisionText totalWidth={props.width}>{props.table.decision.decision}</DecisionText>
      <HandEquityText totalWidth={props.width}>{handEquity}</HandEquityText>
    </PokerAnalyserDecisionView>
  );
};
