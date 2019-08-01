import React from "react";
import { Text, View, Dimensions } from "react-native";
import { Dialog, DialogDefaultActions } from "react-native-material-ui";
import styled from "styled-components/native";
import { getHandEquity, getPhaseName } from "../../helpers/utils";

const ToolBarHeight = 60;
const DialogFactor = 0.4;
const DialogWidth = Dimensions.get("window").width * 1;
const MaxHeight = Dimensions.get("window").height * DialogFactor;
const DialogTop = Dimensions.get("window").height / 2 - MaxHeight / 2;

const HistoryDialogView = styled.View`
  flex: 1;
  justify-content: center;
  align-items: center;
  max-height: ${MaxHeight};
  min-width: ${DialogWidth};
  top: ${DialogTop - ToolBarHeight};
`;

const TableListView = styled.ScrollView`
  border-width: 1;
  border-color: #000000;
  max-height: ${Dimensions.get("window").height * DialogFactor};
`;

export default HistoryDialog = props => {
  DialogPressed = x => {
    if (props.onOk && x === "OK") {
      props.onOk();
    }
  };

  renderTables = tables => {
    return tables.map((x, i) => {
      let handEquity = "";

      if (x.hand_analisys.result) {
        handEquity = getHandEquity(x.hand_analisys.result[0][1] * 100, `%`);
      }

      return (
        <View
          key={i.toString()}
          style={{
            flexDirection: "row",
            borderTopColor: "#FFFFFF",
            borderStyle: "dotted",
            borderWidth: 1,
            borderColor: "#000",
            borderRadius: 1
          }}
        >
          <Text style={{ width: "20%" }}>{x.hero.hero_cards}</Text>
          <Text style={{ width: "30%" }}>
            {getPhaseName(x.hand_analisys.hand_phase)}
          </Text>
          <Text style={{ width: "30%" }}>{x.hero.position}</Text>
          <Text style={{ width: "40%" }}>{handEquity}</Text>
        </View>
      );
    });
  };

  ShowContent = () => {
    if (props.tables) {
      return (
        <Dialog.Content>
          <Text>Received Tables</Text>
          <TableListView>{renderTables(props.tables)}</TableListView>
          <Text>Tap to open...</Text>
        </Dialog.Content>
      );
    } else {
      return (
        <Dialog.Content>
          <Text>No Tables have been received yet!!!</Text>
        </Dialog.Content>
      );
    }
  };

  return (
    <HistoryDialogView>
      <Dialog>
        <Dialog.Title>
          <Text>Table History</Text>
        </Dialog.Title>
        {ShowContent()}
        <Dialog.Actions>
          <DialogDefaultActions
            actions={["OK"]}
            onActionPress={x => DialogPressed(x)}
          />
        </Dialog.Actions>
      </Dialog>
    </HistoryDialogView>
  );
};
