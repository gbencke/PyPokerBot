import React, { Component } from "react";
import { Dimensions,View } from "react-native";
import { Card } from "react-native-material-ui";
import PokerAnalyserPlayersCards from "./PokerAnalyserPlayersCards";
import PokerAnalyserHandStatus from "./PokerAnalyserHandStatus";
import PokerAnalyserCommands from "./PokerAnalyserCommands";
import PokerAnalyserDecision from "./PokerAnalyserDecision";
import PokerAnalyserTableType from "./PokerAnalyserTableType";
import styled from "styled-components/native";

const PokerAnalyserCardView = styled.View`
  width: ${Dimensions.get('window').width};
  ${ props => props.noMargin !== true ? 'padding-right: 12;' : null }
  ${ props => props.noMargin !== true ? 'padding-left: 12;' : null }
  ${ props => props.noMargin !== true ? 'margin-top: 30;' : null }
  height: 400;
`;

export default PokerAnalyserCard = props => {

  return (
    <PokerAnalyserCardView noMargin={props.noMargin}>
      <Card>
        <PokerAnalyserTableType table={props.table} />
        <PokerAnalyserPlayersCards table={props.table} />
        <PokerAnalyserHandStatus table={props.table} />
        <PokerAnalyserCommands table={props.table} />
        <PokerAnalyserDecision table={props.table} />
      </Card>
    </PokerAnalyserCardView>
  );
};
