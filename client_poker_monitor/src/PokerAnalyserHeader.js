import React, { Component } from "react";
import { Text, View } from "react-native";
import {
  Dialog,
  Toolbar,
  DialogDefaultActions
} from "react-native-material-ui";

export default class PokerAnalyserHeader extends Component {
  constructor(props) {
    super(props);
    this.state = { historyDialog: false };
  }

  DialogPressed(x) {
    if (x === "ok") {
    }
    if (x === "cancel") {
    }
    this.setState({ historyDialog: false });
  }

  MenuPressed(label) {
    if (label.index === 0) {
      console.log("Clicked History");
      this.setState({ historyDialog: true });
    } else {
      console.log("About");
    }
  }

  renderDialog() {
    return (
      <View style={styles.dialogStyle}>
        <Dialog>
          <Dialog.Title>
            <Text>Teste History</Text>
          </Dialog.Title>
          <Dialog.Content>
            <Text>Conteudo</Text>
          </Dialog.Content>
          <Dialog.Actions>
            <DialogDefaultActions
              actions={["cancel", "ok"]}
              onActionPress={x => this.DialogPressed(x)}
            />
          </Dialog.Actions>
        </Dialog>
      </View>
    );
  }

  render() {
    return (
      <View style={styles.fullScreen}>
        <View style={styles.toolbarStyle}>
          <Toolbar
            style={styles.toolbarStyle}
            centerElement="Poker Assistant"
            rightElement={{
              menu: {
                icon: "more-vert",
                labels: ["History", "About"]
              }
            }}
            onRightElementPress={label => this.MenuPressed(label)}
          />
        </View>
        {this.state.historyDialog ? this.renderDialog() : null}
      </View>
    );
  }
}

const styles = {
  dialogStyle: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  fullScreen: {
    width: "100%",
    height: "100%",
    flexDirection: "column"
  },
  toolbarStyle: {
    container: {
      height: 60
    },
    width: "100%"
  }
};
