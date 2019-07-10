import React, { Component } from "react";
import { Dimensions, Image, View, Text } from "react-native";
import { Card } from "react-native-material-ui";
import styled from "styled-components/native";

const PokerAnalyserTableTypeView = styled.View`
    margin-left: 10;
    margin-right: 10;
    margin-bottom: 20;
    width: 100%;
    justify-content: center;
    align-items: center;
`;

const TableTypeText = styled.Text`
    font-size: 24;
`;

export default PokerAnalyserTableType = props => {
  this.getTableType = () => {
    return `${props.table.image_platform} (${props.table.image_tabletype})`;
  };

  return (
    <PokerAnalyserTableTypeView>
      <TableTypeText>{this.getTableType()}</TableTypeText>
    </PokerAnalyserTableTypeView>
  );
};


