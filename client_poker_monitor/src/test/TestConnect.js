import React, { Component } from "react";
import { ToastAndroid, Text, View } from "react-native";
import { Toolbar } from "react-native-material-ui";
import PokerAnalyserConnect from "../PokerAnalyserConnect";

export default class TestConnect extends Component {
  constructor(props) {
    super(props);
    this.state = {
      initialAddress: "http://192.168.0.10:3000",
      connectText: "Enter PokerBot Server URL and press Connect",
      connectState: "disconnected"
    };
    this.pressedConnect = this.pressedConnect.bind(this);
    this.connectStatus = this.connectStatus.bind(this);
  }

  pressedConnect(address) {
    if(this.state.connectState === 'disconnected'){
      console.log(`Connecting to address:${address}`);
    }
  }

  connectStatus() {}

  render() {
    return (
      <View style={styles.fullScreen}>
        <PokerAnalyserConnect
          status={this.state.connectState}
          ConnectTextInfo={this.state.connectText}
          pressConnect={this.pressedConnect}
          connectStatus={this.connectStatus}
          initialAddress={this.state.initialAddress}
        />
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
