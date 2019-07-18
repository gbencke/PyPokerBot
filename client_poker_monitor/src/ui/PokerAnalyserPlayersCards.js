import React, { Component } from "react";
import { Dimensions, Image, View, Text } from "react-native";
import { Card } from "react-native-material-ui";
import FitImage from "react-native-fit-image";
import styled from "styled-components/native";
import PokerAnalyserRenderCard from "./PokerAnalyserCardElements/PokerAnalyserRenderCard";
import PokerAnalyserRenderNoCard from "./PokerAnalyserCardElements/PokerAnalyserRenderNoCard";

const PlayersCardView = styled.View`
  flex-direction: row;
  justify-content: space-between;
`;

const CardStyle = styled.View`
  margin-left: 10;
  margin-right: 10;
`;

export default PokerAnalyserPlayersCards = props => {
  getHeroPos = () => {
    return props.table.hero.hero_pos;
  };

  getPosDescArray = () => {
    const heroPos = props.table.hero.position;

    switch (heroPos) {
      case "BUTTON":
      default:
        return ["SB", "BB", "MP", "LP", "LP", "BUTTON"];
    }
  };

  posDescs = getPosDescArray();
  heroPos = getHeroPos();

  getPosDesc = pos => {
    return posDescs[pos];
  };

  RenderPlayersCards = () => {
    return props.table.cards.map((item, i) => {
      return item ? (
        <PokerAnalyserRenderCard
          hero={i == heroPos}
          posDesc={getPosDesc(i)}
          pos={i}
          key={i.toString()}
        />
      ) : (
        <PokerAnalyserRenderNoCard
          hero={i == heroPos}
          posDesc={getPosDesc(i)}
          pos={i}
          key={i.toString()}
        />
      );
    });
  };

  return (
    <CardStyle>
      <PlayersCardView>{RenderPlayersCards()}</PlayersCardView>
    </CardStyle>
  );
};
