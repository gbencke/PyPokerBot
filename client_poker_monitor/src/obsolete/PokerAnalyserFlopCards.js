import React, { Component } from "react";
import { View, Text } from "react-native";
import { Card } from "react-native-material-ui";
import { getCardCode } from "./helpers/getCardCode";
import styled from "styled-components/native";

const CardStyleView = styled.View`
  margin-left: 10;
  margin-right: 10;
`;

const CardFontText = styled.Text`
  margin-top: 10;
  font-family: cards;
  font-size: 48;
  width: 100%;
  text-align: center;
`;

const PokerAnalyserFlopCardsView = styled.View`
  flex-direction: column;
`;

export default PokerAnalyserFlopCards = props => {
  return (
    <PokerAnalyserFlopCardsView>
      <CardStyleView>
        <Text>FLOP({`${props.table.hand_analisys.hand_phase}`})</Text>
      </CardStyleView>
      <CardStyleView>
        <CardFontText>{getCardCode(props.table.flop.join(""))}</CardFontText>
      </CardStyleView>
    </PokerAnalyserFlopCardsView>
  );
};
