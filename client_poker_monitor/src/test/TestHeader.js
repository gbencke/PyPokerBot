import React, { Component } from "react";
import { ToastAndroid, Text, View } from "react-native";
import PokerAnalyserHeader from "../ui/PokerAnalyserHeader";
import HistoryDialog from "../ui/dialog/HistoryDialog";
import AboutDialog from "../ui/dialog/AboutDialog";

export default class TestHeader extends Component {

  constructor(props) {
    super(props);
    this.state = { showHistory: false, showAbout: false };
  }

  HistoryPressed() {
    this.setState({ showHistory: true, showAbout: false });
  }

  AboutPressed() {
    //ToastAndroid.show(`Pressed: About`, ToastAndroid.SHORT);
    this.setState({ showHistory: false, showAbout: true });
  }

  PressedOk() {
    //ToastAndroid.show(`Pressed: OK`, ToastAndroid.SHORT);
    this.setState({ showHistory: false, showAbout: false });
  }

  PressedCancel() {
    //ToastAndroid.show(`Pressed: Cancel`, ToastAndroid.SHORT);
    this.setState({ showHistory: false, showAbout: false });
  }

  render() {
    const { showHistory, showAbout } = this.state;
    let { PressedOk , PressedCancel } = this;

    PressedOk = PressedOk.bind(this);
    PressedCancel = PressedCancel.bind(this);

    return (
      <View style={styles.fullScreen}>
        <PokerAnalyserHeader
          onHistory={() => this.HistoryPressed()}
          onAbout={() => this.AboutPressed()}
        />

        {showHistory ? (
          <HistoryDialog
            onOk={PressedOk}
            onCancel={PressedCancel}
            tables={this.props.tables}
          />
        ) : null}
        {showAbout ? (
          <AboutDialog
            onOk={PressedOk}
            onCancel={PressedCancel}
          />
        ) : null}
      </View>
    );
  }
}
/*
 *
 */

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
