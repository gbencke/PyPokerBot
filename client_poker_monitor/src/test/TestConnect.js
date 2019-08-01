import React, { Component } from "react";
import _ from "lodash";
import styled from "styled-components/native";
import { Dimensions } from "react-native";
import PokerAnalyserConnect from "../ui/PokerAnalyserConnect";
import { getCurrentTable, testConnection } from "../api/PokerBotServerAPI";
import { getDefaultURL } from "../helpers/storage";

const PokerConnectWrapper = styled.View`
  flex-direction: column;
  width: ${props => props.totalWidth};
`;
export default class TestConnect extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentTable: null,
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
    this.setNextTable = this.setNextTable.bind(this);
    this.onConnectError = this.onConnectError.bind(this);
    this.onConnectSuccess = this.onConnectSuccess.bind(this);

    this._isMounted = false;
    this._isFetching = false;
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

  setNextTable(table) {
    if (!_.isEqual(this.state.currentTable, table)) {
      console.log(`Got new table:${JSON.stringify(table)}`);
      this.setState({ ...this.state, currentTable: table });
    }
  }

  pollCurrentTable() {
    if (this.state.connectState === "disconnected") {
      this._isFetching = false;
      return;
    }

    if (!this._isFetching) {
      //console.log("polling table..");
      this._isFetching = true;
      getCurrentTable(
        this.state.Address,
        1,
        table => {
          this.setNextTable(table);
          this._isFetching = false;
        },
        error => {
          console.log(error);
          this._isFetching = false;
        }
      );
    }
    setTimeout(() => this.pollCurrentTable(), 1000);
  }

  onConnectSuccess(address) {
    this.setState({
      ...this.state,
      Address: address,
      connectState: "connected",
      connectText: "Successfully Connected..."
    });
    setTimeout(() => this.pollCurrentTable(), 1000);
  }

  onConnectError(address, errorMessage) {
    this.setState({
      ...this.state,
      Address: address,
      connectState: "error",
      connectText: errorMessage
    });
  }

  pressedConnect(address) {
    if (this.state.connectState !== "connected") {
      console.log(`Connecting to address:${address}`);
      testConnection(
        address,
        this.onConnectSuccess,
        this.onConnectError
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
    console.log("render...");
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
