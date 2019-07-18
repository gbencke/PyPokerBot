import React, { Component } from "react";
import { ToastAndroid, Text, View } from "react-native";
import { Toolbar } from "react-native-material-ui";
import PokerAnalyserConnect from "../ui/PokerAnalyserConnect";
import { testConnection } from "../api/PokerBotServerAPI";

export default class TestConnect extends Component {
  constructor(props) {
    super(props);
    this.state = {
      initialAddress: "http://192.168.0.10:5000",
      connectText: "Enter PokerBot Server URL and press Connect",
      connectState: "disconnected"
    };
    this.pressedConnect = this.pressedConnect.bind(this);
    this.connectStatus = this.connectStatus.bind(this);
  }

  pressedConnect(address) {
    if (this.state.connectState !== "connected") {
      console.log(`Connecting to address:${address}`);
      testConnection(
        address,
        () => {
          this.setState({
            ...this.state,
            connectState: "connected",
            connectText: "Successfully Connected..."
          });
        },
        errorMessage => {
          this.setState({
            ...this.state,
            connectState: "error",
            connectText: errorMessage
          });
        }
      );
    } else {
      this.setState({
        ...this.state,
        connectState: "disconnected",
        connectText: "Enter PokerBot Server URL and press Connect"
      });
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
