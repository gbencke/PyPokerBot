import React, { Component } from "react";
import { Button } from "react-native-material-ui";
import { Text, View } from "react-native";
import styled from "styled-components/native";
import BlinkView from "react-native-blink-view";
import { getHandEquity } from "./helpers/utils";

const DecisionText = styled.Text`
  font-size: 36;
  font-weight: 800;
`;

const PokerAnalyserDecisionView = styled.View`
  width: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20;
  margin-left: 10;
  margin-right: 10;
`;

export default PokerAnalyserDecision = props => {
  const handEquity = getHandEquity(
    props.table.hand_analisys.result[0][1] * 100,
    `% for a winning hand`
  );

  return (
    <PokerAnalyserDecisionView>
      <DecisionText> {props.table.decision.decision} </DecisionText>
      <Text>{handEquity}</Text>
    </PokerAnalyserDecisionView>
  );
};
