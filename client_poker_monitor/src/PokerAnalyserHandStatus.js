import React, { Component } from "react";
import { View } from "react-native";
import PokerAnalyserHand from "./PokerAnalyserHand";
import styled from "styled-components/native";

const PokerAnalyserCardView = styled.View`
  margin-top: 20;
  flex-direction: row;
`;

export default PokerAnalyserCard = props => {
  return (
    <PokerAnalyserCardView>
      <PokerAnalyserHand hero table={props.table} />
      <PokerAnalyserHand flop table={props.table} />
    </PokerAnalyserCardView>
  );
};
