import React from "react";
import styled from "styled-components/native";
import PokerAnalyserRenderCard from "./PokerAnalyserRenderCard";
import PokerAnalyserRenderNoCard from "./PokerAnalyserRenderNoCard";

const PlayersCardView = styled.View`
  flex-direction: row;
  justify-content: space-between;
`;

const CardStyle = styled.View`
  margin-left: 5%;
  margin-right: 5%;
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

  RenderPlayersCards = (totalCards, width) => {
    return props.table.cards.map((item, i) => {
      return item ? (
        <PokerAnalyserRenderCard
          totalCards={totalCards}
          width={width}
          hero={i == heroPos}
          posDesc={getPosDesc(i)}
          pos={i}
          key={i.toString()}
        />
      ) : (
        <PokerAnalyserRenderNoCard
          totalCards={totalCards}
          width={width}
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
      <PlayersCardView>
        {RenderPlayersCards(props.table.cards.length, props.width)}
      </PlayersCardView>
    </CardStyle>
  );
};
