import React, { Component } from "react";
import { Button } from "react-native-material-ui";
import { Text, View } from "react-native";
import styled from "styled-components/native";

const ButtonCommandsView = styled.View`
  margin-top: 10;
  flex-direction: row;
  justify-content: space-between;
`;

const CommandsView = styled.View`
  flex-direction: column;
  margin-top: 40;
  margin-left: 10;
  margin-right: 10;
`;

export default PokerAnalyserCommands = props => {
  getCommandText = index => {
    let ret = props.table.commands[index][2].trim();
    console.log(ret);
    ret = ret.replace("[1]", "CALL");
    if (ret === "20") {
      return "FOLD";
    }
    return ret;
  };

  const ButtonStyle = {
    container: {
      minWidth: 100
    }
  };

  return (
    <CommandsView>
      <Text>AVAILABLE COMMANDS</Text>
      <ButtonCommandsView>
        <Button style={ButtonStyle} raised accent text={getCommandText(0)} />
        <Button style={ButtonStyle} raised accent text={getCommandText(1)} />
        <Button style={ButtonStyle} raised accent text={getCommandText(2)} />
      </ButtonCommandsView>
    </CommandsView>
  );
};
