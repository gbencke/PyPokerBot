import React, { Component } from "react";
import { Dimensions, Image, View, Text } from "react-native";
import FitImage from "react-native-fit-image";
import styled from "styled-components/native";

const factor = 15;

const NoCardStyle = styled.View`
  flex: 1;
  justify-content: flex-start;
  align-items: center;
`;

const NoRenderedCardStyle = styled.Text`
  width: ${(Dimensions.get("window").width / factor) * 2};
  height: ${Dimensions.get("window").height / factor};
  border-width: 1;
  border-radius: 1;
  border-style: dashed;
  ${props => (props.hero ? "border-color: red;" : "border-color: #000")}
`;

export default PokerAnalyserRenderCard = props => {
  return (
    <NoCardStyle>
      <NoRenderedCardStyle></NoRenderedCardStyle>
      <Text>{`${props.posDesc}`}</Text>
    </NoCardStyle>
  );
};
