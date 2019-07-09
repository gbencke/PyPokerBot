import React, { Component } from "react";
import { Text, View } from "react-native";
import { Dialog, DialogDefaultActions } from "react-native-material-ui";

export default HistoryDialog = props => {
  DialogPressed = x => {
    if (props.onOk && x === "OK") {
      props.onOk();
    }
    if (props.onCancel && x === "CANCEL") {
      props.onCancel();
    }
  };

  return (
    <View style={styles.dialogStyle}>
      <Dialog>
        <Dialog.Title>
          <Text>Teste History</Text>
        </Dialog.Title>
        <Dialog.Content>
          <Text>Conteudo History</Text>
        </Dialog.Content>
        <Dialog.Actions>
          <DialogDefaultActions
            actions={["OK", "CANCEL"]}
            onActionPress={x => this.DialogPressed(x)}
          />
        </Dialog.Actions>
      </Dialog>
    </View>
  );
};

const styles = {
  dialogStyle: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  }
};
