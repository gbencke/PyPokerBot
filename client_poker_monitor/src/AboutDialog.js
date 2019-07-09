import React, { Component } from "react";
import { Text, View } from "react-native";
import { Dialog, DialogDefaultActions } from "react-native-material-ui";

const AboutDialog = props => {
  const DialogPressed = x => {
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
          <Text>Teste About</Text>
        </Dialog.Title>
        <Dialog.Content>
          <Text>Conteudo About</Text>
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

export default AboutDialog;
