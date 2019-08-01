import _ from "lodash";
import React, { Component } from "react";
import PokerAnalyserConnect from "./PokerAnalyserConnect";
import PokerAnalyserHeader from "./PokerAnalyserHeader";
import styled from "styled-components/native";
import { View, Dimensions } from "react-native";
import HistoryDialog from "./dialog/HistoryDialog";
import AboutDialog from "./dialog/AboutDialog";
import { getCurrentTable, testConnection } from "../api/PokerBotServerAPI";
import { getDefaultURL } from "../helpers/storage";

const PokerAnalyserView = styled.View`
  width: 100%;
  height: 100%;
  flex-direction: column;
`;

const DialogView = styled.View`
  width: 100%;
  flex: 1;
  margin-top: -80px;
`;

export default class PokerAnalyser extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentTable: null,
      totalWidth:
        props.totalWidth || parseInt(Dimensions.get("window").width / 10) * 10,
      Address: props.initialAddress || "",
      connectText:
        props.connectText || "Enter PokerBot Server URL and press Connect",
      connectState: "disconnected",
      showHistory: false,
      showAbout: false,
      tableHistory: [],
      table: null
    };

    this.pressedConnect = this.pressedConnect.bind(this);
    this.connectStatus = this.connectStatus.bind(this);
    this.pollCurrentTable = this.pollCurrentTable.bind(this);
    this.setDefaultURL = this.setDefaultURL.bind(this);
    this.setNextTable = this.setNextTable.bind(this);
    this.onConnectError = this.onConnectError.bind(this);
    this.onConnectSuccess = this.onConnectSuccess.bind(this);
    this.PressedOk = this.PressedOk.bind(this);
    this.PressedCancel = this.PressedCancel.bind(this);

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
      testConnection(address, this.onConnectSuccess, this.onConnectError);
    } else {
      this.setState({
        ...this.state,
        connectState: "disconnected",
        connectText: "Enter PokerBot Server URL and press Connect"
      });
    }
  }

  connectStatus() {}

  HistoryPressed() {
    this.setState({ showHistory: true, showAbout: false });
  }

  AboutPressed() {
    this.setState({ showHistory: false, showAbout: true });
  }

  PressedOk() {
    this.setState({ showHistory: false, showAbout: false });
  }

  PressedCancel() {
    this.setState({ showHistory: false, showAbout: false });
  }

  render() {
    const { showHistory, showAbout } = this.state;
    let { PressedOk, PressedCancel } = this;

    return (
      <PokerAnalyserView>
        <PokerAnalyserHeader
          onHistory={() => this.HistoryPressed()}
          onAbout={() => this.AboutPressed()}
        />
        <PokerAnalyserConnect
          totalWidth={this.state.totalWidth}
          status={this.state.connectState}
          ConnectTextInfo={this.state.connectText}
          pressConnect={this.pressedConnect}
          connectStatus={this.connectStatus}
          initialAddress={this.state.Address}
        />
        <DialogView>
          {showHistory ? (
            <HistoryDialog
              onOk={PressedOk}
              onCancel={PressedCancel}
              tables={this.state.tableHistory}
            />
          ) : null}
          {showAbout ? (
            <AboutDialog onOk={PressedOk} onCancel={PressedCancel} />
          ) : null}
        </DialogView>
      </PokerAnalyserView>
    );
  }
}
