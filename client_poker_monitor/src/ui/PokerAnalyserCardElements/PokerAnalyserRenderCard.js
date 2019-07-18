import React, { Component } from "react";
import { Dimensions, Image, View, Text } from "react-native";
import FitImage from "react-native-fit-image";
import styled from "styled-components/native";

const CardTemplate = require("./templates/card2.jpg");
const factor = 15;

const RenderCardView = styled.View`
  flex-direction: column;
  width: 16%;
`;

const WithCardPlayingCardViewStyle = styled.View`
  width: 16%;
  flex-direction: row;
  justify-content: space-between;
`;

const TextPosition = styled.Text`
  width: 100%;
  text-align: center;
  ${ props => props.hero ? 'color:red;' : null}
`;

const styles = {
  WithCardRenderedCardStyle: {
    width: Dimensions.get("window").width / factor,
    height: Dimensions.get("window").height / factor
  }
};

export default PokerAnalyserRenderCard = props => {
  return (
    <RenderCardView>
      <WithCardPlayingCardViewStyle hero={props.hero}>
        <FitImage
          source={CardTemplate}
          style={styles.WithCardRenderedCardStyle}
        />
        <FitImage
          source={CardTemplate}
          style={styles.WithCardRenderedCardStyle}
        />
      </WithCardPlayingCardViewStyle>
      <TextPosition hero={props.hero} >{`${props.posDesc}`}</TextPosition>
    </RenderCardView>
  );
};
