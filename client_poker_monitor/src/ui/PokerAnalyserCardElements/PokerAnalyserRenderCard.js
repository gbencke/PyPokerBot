import React, { Component } from "react";
import { Dimensions, Image, View, Text } from "react-native";
import FitImage from "react-native-fit-image";
import styled from "styled-components/native";

const CardTemplate = require("./templates/card2.jpg");
const factor = 15;

const RenderCardView = styled.View`
  flex-direction: column;
  margin-left: 2px;
  margin-right: 2px;
  width: ${props => parseInt(props.width / (props.totalCards + 1))}px;
`;

const WithCardPlayingCardViewStyle = styled.View`
  flex-direction: row;
  justify-content: space-between;
  width: ${props => parseInt(props.width / (props.totalCards + 1))}px;
`;

const TextPosition = styled.Text`
  width: 100%;
  text-align: center;
  font-size: ${props => parseInt((12 / 420) * props.width)}px;
  ${props => (props.hero ? "color:red;" : null)}
`;

export default PokerAnalyserRenderCard = props => {
  const styles = {
    WithCardRenderedCardStyle: {
      marginLeft: 2,
      marginRight: 2,
      width: parseInt(props.width / (props.totalCards + 1) / 4),
      height: Dimensions.get("window").height / factor
    }
  };

  console.log(
    `WithCardRenderedCardStyle:${styles.WithCardRenderedCardStyle.width}`
  );

  return (
    <RenderCardView width={props.width} totalCards={props.totalCards}>
      <WithCardPlayingCardViewStyle
        width={props.width}
        totalCards={props.totalCards}
        hero={props.hero}
      >
        <FitImage
          source={CardTemplate}
          style={styles.WithCardRenderedCardStyle}
        />
        <FitImage
          source={CardTemplate}
          style={styles.WithCardRenderedCardStyle}
        />
      </WithCardPlayingCardViewStyle>
      <TextPosition
        width={props.width}
        hero={props.hero}
      >{`${props.posDesc}`}</TextPosition>
    </RenderCardView>
  );
};
