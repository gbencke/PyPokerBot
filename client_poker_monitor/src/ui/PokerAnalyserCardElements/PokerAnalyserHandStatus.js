import React from "react";
import PokerAnalyserHand from "./PokerAnalyserHand";
import styled from "styled-components/native";

const PokerAnalyserCardView = styled.View`
  margin-top: 20;
  flex-direction: row;
  margin-left: 5%;
  margin-right: 5%;
`;

export default PokerAnalyserCard = props => {
  return (
    <PokerAnalyserCardView>
      <PokerAnalyserHand hero table={props.table} width={props.width}/>
      <PokerAnalyserHand flop table={props.table} width={props.width}/>
    </PokerAnalyserCardView>
  );
};
