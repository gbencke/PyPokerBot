import React from "react";
import { Platform } from "react-native";
import PokerAnalyserPlayersCards from "./PokerAnalyserCardElements/PokerAnalyserPlayersCards";
import PokerAnalyserHandStatus from "./PokerAnalyserCardElements/PokerAnalyserHandStatus";
import PokerAnalyserCommands from "./PokerAnalyserCardElements/PokerAnalyserCommands";
import PokerAnalyserDecision from "./PokerAnalyserCardElements/PokerAnalyserDecision";
import PokerAnalyserTableType from "./PokerAnalyserCardElements/PokerAnalyserTableType";
import styled from "styled-components/native";

const PokerAnalyserCardView = styled.View`
  width: ${props => props.width}px;
  ${Platform.OS === "ios" ? "margin-top: 30px;" : "margin:0 0 0 0;"}: 
  ${props => (props.noMargin !== true ? "padding-right: 12;" : null)}
  ${props => (props.noMargin !== true ? "padding-left: 12;" : null)}
  ${props => (props.noMargin !== true ? "margin-top: 30;" : null)}
  height: 400;
`;

export default PokerAnalyserCard = props => {
  if (!props.table || props.width < 100 || props.width > 1000) return null;

  return (
    <PokerAnalyserCardView width={props.width} noMargin={props.noMargin}>
      <PokerAnalyserTableType width={props.width} table={props.table} />
      <PokerAnalyserPlayersCards width={props.width} table={props.table} />
      <PokerAnalyserHandStatus width={props.width} table={props.table} />
      <PokerAnalyserCommands width={props.width} table={props.table} />
      <PokerAnalyserDecision width={props.width} table={props.table} />
    </PokerAnalyserCardView>
  );
};
