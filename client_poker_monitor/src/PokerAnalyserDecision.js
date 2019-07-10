import React, { Component } from "react";
import { Button } from "react-native-material-ui";
import { Text, View } from "react-native";
import styled from "styled-components/native";
import BlinkView from "react-native-blink-view";

const DecisionText = styled.Text`
  font-size: 36;
  font-weight: 800;
`;

const PokerAnalyserDecisionView = styled.View`
  width: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 40;
  margin-bottom: 20;
  margin-left: 10;
  margin-right: 10;
`;

export default PokerAnalyserDecision = props => {
  let handEquity = props.table.hand_analisys.result[0][1] * 100;
  if (!isNaN(handEquity)) {
    handEquity = handEquity.toFixed(2);
    handEquity = `${handEquity}% for a winning hand`;
  } else {
    handEquity = "";
  }

  return (
    <PokerAnalyserDecisionView>
      <DecisionText> {props.table.decision.decision} </DecisionText>
      <Text>{handEquity}</Text>
    </PokerAnalyserDecisionView>
  );
};
