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
  let HandMessage = "Error!!";
  let CardsToShow = "";

  console.log(props);

  if (props.hero) {
    HandMessage = `CURRENT HAND:`;
    CardsToShow = getCardCode(props.table.hero.hero_cards);
  }

  if (props.flop) {
    HandMessage = `PHASE:${props.table.hand_analisys.hand_phase}`;
    CardsToShow = getCardCode(props.table.flop.join(""));
  }

  return (
    <PokerAnalyserFlopCardsView>
      <CardStyleView>
        <Text>{HandMessage}</Text>
      </CardStyleView>
      <CardStyleView>
        <CardFontText>{CardsToShow}</CardFontText>
      </CardStyleView>
    </PokerAnalyserFlopCardsView>
  );
};
