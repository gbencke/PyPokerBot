import React from "react";
import { getCardCode } from "../../helpers/getCardCode";
import styled from "styled-components/native";

const CardHeaderStyle = styled.Text`
  color: #000000;
  font-size: ${props => parseInt((16 / 410) * props.totalWidth)}px;
`;

const CardSingleView = styled.View``;

const CardTextCode = styled.Text`
  font-size: ${props => parseInt((14 / 410) * props.totalWidth)};
  text-align: center;
  color: #000000;
  font-weight: 900;
`;

const CardStyleView = styled.View`
  margin-left: 10;
  margin-right: 10;
  flex-direction: row;
`;

const CardFontText = styled.Text`
  font-size: ${props => parseInt((48 / 410) * props.totalWidth)};
  margin-top: 10;
  font-family: cards;
  text-align: center;
`;

const PokerAnalyserFlopCardsView = styled.View`
  flex-direction: column;
`;

export default PokerAnalyserFlopCards = props => {
  let HandMessage = "Error!!";
  let CardsToShow = "";

  if (props.hero) {
    HandMessage = `CURRENT HAND:`;
    CardsToShow = getCardCode(props.table.hero.hero_cards);
  } else {
    HandMessage = `PHASE:${props.table.hand_analisys.hand_phase}`;
    CardsToShow = getCardCode(props.table.flop.join(""));
  }

  const CardsStyled = CardsToShow.map((x, i) => {
    return (
      <CardSingleView key={i.toString()} totalWidth={props.width}>
        <CardFontText
          totalWidth={props.width}
          style={{ color: x.color }}
        >
          {x.cardCharCode}
        </CardFontText>
        <CardTextCode totalWidth={props.width}>{x.currentCard}</CardTextCode>
      </CardSingleView>
    );
  });

  return (
    <PokerAnalyserFlopCardsView>
      <CardStyleView>
        <CardHeaderStyle totalWidth={props.width}>
          {HandMessage}
        </CardHeaderStyle>
      </CardStyleView>
      <CardStyleView>{CardsStyled}</CardStyleView>
    </PokerAnalyserFlopCardsView>
  );
};
