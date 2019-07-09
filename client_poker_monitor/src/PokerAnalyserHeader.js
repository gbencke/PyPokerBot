import React, { Component } from "react";
import { ToastAndroid, Text, View } from "react-native";
import {
  Dialog,
  Toolbar,
  DialogDefaultActions
} from "react-native-material-ui";

export default class PokerAnalyserHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  DialogPressed(x) {
    ToastAndroid.show(`Pressed:${x}`, ToastAndroid.SHORT);
    this.setState({ historyDialog: false, aboutDialog: false});
  }

  MenuPressed(label) {
    if (label.index === 0) {
      console.log("Clicked History");
      this.setState({ historyDialog: true });
    } else {
      console.log("About");
      this.setState({ aboutDialog: true });
    }
  }

  renderHistoryDialog() {
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
              actions={["cancel", "ok"]}
              onActionPress={x => this.DialogPressed(x)}
            />
          </Dialog.Actions>
        </Dialog>
      </View>
    );
  }
  renderAboutDialog() {
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
        {this.state.historyDialog ? this.renderHistoryDialog() : null}
        {this.state.aboutDialog ? this.renderAboutDialog() : null}
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
