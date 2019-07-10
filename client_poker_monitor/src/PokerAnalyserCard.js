import React, { Component } from "react";
import { View } from "react-native";
import { Card } from "react-native-material-ui";
import PokerAnalyserPlayersCards from "./PokerAnalyserPlayersCards";
import PokerAnalyserHandStatus from "./PokerAnalyserHandStatus";
import PokerAnalyserCommands from "./PokerAnalyserCommands";
import PokerAnalyserDecision from "./PokerAnalyserDecision";
import styled from "styled-components/native";

const PokerAnalyserCardView = styled.View`
  width: 100%;
  padding-right: 12;
  padding-left: 12;
  margin-top: 30;
  height: 400;
`;

export default PokerAnalyserCard = props => {
  return (
    <PokerAnalyserCardView>
      <Card>
        <PokerAnalyserPlayersCards table={props.table} />
        <PokerAnalyserHandStatus table={props.table} />
        <PokerAnalyserCommands table={props.table} />
        <PokerAnalyserDecision table={props.table} />
      </Card>
    </PokerAnalyserCardView>
  );
};
