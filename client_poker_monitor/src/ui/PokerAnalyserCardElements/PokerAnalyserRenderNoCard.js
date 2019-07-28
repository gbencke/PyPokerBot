import React from "react";
import { Dimensions } from "react-native";
import styled from "styled-components/native";

const factor = 15;

const NoCardStyle = styled.View`
  flex: 1;
  justify-content: flex-start;
  align-items: center;
`;

const NoRenderedCardStyle = styled.Text`
  height: ${Dimensions.get("window").height / factor};
  width: ${props => parseInt(props.width / (props.totalCards + 1))}px;
  border-width: 1;
  border-radius: 1;
  border-style: dashed;
  ${props => (props.hero ? "border-color: red;" : "border-color: #000")}
`;

const TextPosition = styled.Text`
  width: 100%;
  text-align: center;
  font-size: ${props => parseInt((12 / 420) * props.width)}px;
  ${props => (props.hero ? "color:red;" : null)}
`;

export default PokerAnalyserRenderCard = props => {
  return (
    <NoCardStyle>
      <NoRenderedCardStyle
        width={props.width}
        totalCards={props.totalCards}
      ></NoRenderedCardStyle>
      <TextPosition width={props.width}>{`${props.posDesc}`}</TextPosition>
    </NoCardStyle>
  );
};
