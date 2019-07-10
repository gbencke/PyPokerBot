import React, { Component } from "react";
import { Dimensions, Image, View, Text } from "react-native";
import { Card } from "react-native-material-ui";
import FitImage from "react-native-fit-image";
import styled from "styled-components/native";
import PokerAnalyserRenderCard from "./PokerAnalyserRenderCard";
import PokerAnalyserRenderNoCard from "./PokerAnalyserRenderNoCard";

const PlayersCardView = styled.View`
  flex-direction: row;
  justify-content: space-between;
`;

const CardStyle = styled.View`
  margin-left: 10;
  margin-right: 10;
`;

export default PokerAnalyserPlayersCards = props => {
  RenderPlayersCards = () => {
    return props.table.cards.map((item, i) => {
      return item ? (
        <PokerAnalyserRenderCard pos={i} key={i.toString()} />
      ) : (
        <PokerAnalyserRenderNoCard pos={i} key={i.toString()} />
      );
    });
  };

  return (
    <CardStyle>
      <PlayersCardView>{RenderPlayersCards()}</PlayersCardView>
    </CardStyle>
  );
};
