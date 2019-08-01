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
          <Text>About Poker Analyser</Text>
        </Dialog.Title>
        <Dialog.Content>
          <Text style={{ textAlign: "justify" }}>
            This is a Mobile App to be used to control the PyPokerBot
            application, which controls remotely poker tables and calculates
            winning odds and table equities for playing hands
          </Text>
          <Text style={{ textAlign: "justify", marginTop: 20 }}>
            MIT Licensed
          </Text>
          <Text>Guilherme Bencke, 2019</Text>
        </Dialog.Content>
        <Dialog.Actions>
          <DialogDefaultActions
            actions={["OK"]}
            onActionPress={x => DialogPressed(x)}
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
