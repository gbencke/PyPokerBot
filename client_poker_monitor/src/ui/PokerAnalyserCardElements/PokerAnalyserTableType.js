import React from "react";
import styled from "styled-components/native";

const PokerAnalyserTableTypeView = styled.View`
  margin-left: 5%;
  margin-right: 5%;
  margin-bottom: 5%;
  margin-top: 5%;
  width: 100%;
  justify-content: center;
  align-items: center;
`;

const TableTypeText = styled.Text`
  font-size: ${props => parseInt((24 / 420) * props.width)}px;
  min-height: 32px;
  color: #000000;
`;

export default PokerAnalyserTableType = props => {
  this.getTableType = () => {
    return `${props.table.image_platform} (${props.table.image_tabletype})`;
  };

  return (
    <PokerAnalyserTableTypeView width={props.width}>
      <TableTypeText width={props.width}>{this.getTableType()}</TableTypeText>
    </PokerAnalyserTableTypeView>
  );
};
