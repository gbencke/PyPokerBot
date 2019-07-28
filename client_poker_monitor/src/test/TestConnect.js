import React, { Component } from "react";
import { View, Dimensions } from "react-native";
import PokerAnalyserConnect from "../ui/PokerAnalyserConnect";
import { testConnection } from "../api/PokerBotServerAPI";
import { getDefaultURL } from "../helpers/storage";

export default class TestConnect extends Component {
  constructor(props) {
    super(props);
    this.state = {
      totalWidth: props.totalWidth || Dimensions.get("window").width,
      initialAddress: props.initialAddress || "",
      connectText:
        props.connectText || "Enter PokerBot Server URL and press Connect",
      connectState: "disconnected"
    };
    this.pressedConnect = this.pressedConnect.bind(this);
    this.connectStatus = this.connectStatus.bind(this);
    this._isMounted = false;
    this.setDefaultURL = this.setDefaultURL.bind(this);
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  setDefaultURL(x) {
    if (this._isMounted) {
      this.setState({ ...this.state, initialAddress: x });
    }
  }

  componentDidMount() {
    this._isMounted = true;
    getDefaultURL().then(x => this.setDefaultURL(x));
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
          totalWidth={this.state.totalWidth}
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
