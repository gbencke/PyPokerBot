import React from "react";
import { Button } from "react-native-material-ui";
import styled from "styled-components/native";

const AvailableCommandsText = styled.Text`
  font-size: ${ props => parseInt((20 / 410) * props.totalWidth)};
`;

const ButtonCommandsView = styled.View`
  margin-top: 10;
  flex-direction: row;
  justify-content: space-between;
`;

const CommandsView = styled.View`
  flex-direction: column;
  margin-top: 40;
  margin-left: 5%;
  margin-right: 5%;
`;

export default PokerAnalyserCommands = props => {
  getCommandText = index => {
    let ret = props.table.commands[index][2].trim();
    ret = ret.replace("[1]", "CALL");
    if (ret === "20") {
      return "FOLD";
    }
    return ret;
  };

  const ButtonStyle = {
    container: {
      minWidth: parseInt((100 / 410) * props.width)
    },
    text: {
      fontSize: parseInt((12 / 410) * props.width)
    }
  };

  return (
    <CommandsView>
      <AvailableCommandsText totalWidth={props.width}>
        AVAILABLE COMMANDS
      </AvailableCommandsText>
      <ButtonCommandsView>
        <Button style={ButtonStyle} raised accent text={getCommandText(0)} />
        <Button style={ButtonStyle} raised accent text={getCommandText(1)} />
        <Button style={ButtonStyle} raised accent text={getCommandText(2)} />
      </ButtonCommandsView>
    </CommandsView>
  );
};
