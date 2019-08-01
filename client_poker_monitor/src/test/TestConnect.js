import React, { Component } from "react";
import styled from "styled-components/native";
import { Dimensions } from "react-native";
import PokerAnalyserConnect from "../ui/PokerAnalyserConnect";
import { testConnection } from "../api/PokerBotServerAPI";
import { getDefaultURL } from "../helpers/storage";

const PokerConnectWrapper = styled.View`
  flex-direction: column;
  width: ${props => props.totalWidth};
`;
export default class TestConnect extends Component {
  constructor(props) {
    super(props);
    this.state = {
      totalWidth: props.totalWidth || Dimensions.get("window").width,
      Address: props.initialAddress || "",
      connectText:
        props.connectText || "Enter PokerBot Server URL and press Connect",
      connectState: "disconnected"
    };

    this.pressedConnect = this.pressedConnect.bind(this);
    this.connectStatus = this.connectStatus.bind(this);
    this.pollCurrentTable = this.pollCurrentTable.bind(this);
    this.setDefaultURL = this.setDefaultURL.bind(this);
    this._isMounted = false;
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  setDefaultURL(x) {
    if (this._isMounted) {
      this.setState({ ...this.state, Address: x });
    }
  }

  componentDidMount() {
    this._isMounted = true;
    getDefaultURL().then(x => this.setDefaultURL(x));
  }

  pollCurrentTable() {
    console.log("polling table..");
    setTimeout(() => this.pollCurrentTable(), 200);
  }

  pressedConnect(address) {
    if (this.state.connectState !== "connected") {
      console.log(`Connecting to address:${address}`);
      testConnection(
        address,
        () => {
          this.setState({
            ...this.state,
            Address: address,
            connectState: "connected",
            connectText: "Successfully Connected..."
          });
        },
        errorMessage => {
          this.setState({
            ...this.state,
            Address: address,
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
      <PokerConnectWrapper totalWidth={this.props.totalWidth}>
        <PokerAnalyserConnect
          totalWidth={this.props.totalWidth}
          status={this.state.connectState}
          ConnectTextInfo={this.state.connectText}
          pressConnect={this.pressedConnect}
          connectStatus={this.connectStatus}
          initialAddress={this.state.Address}
        />
      </PokerConnectWrapper>
    );
  }
}

const styles = {
  dialogStyle: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center"
  },
  toolbarStyle: {
    container: {
      height: 60
    },
    width: "100%"
  }
};
