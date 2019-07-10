import React, { Component } from "react";
import PokerAnalyserConnect from "./PokerAnalyserConnect";
import PokerAnalyserHeader from "./PokerAnalyserHeader";
import PokerAnalyserCard from "./PokerAnalyserCard";
import getTableData from "./test/tableData";
import styled from "styled-components/native";

const PokerAnalyserView = styled.View``;

export default class PokerAnalyser extends Component {
  constructor(props) {
    super(props);
    this.state = {
      connected: false
    };
    this.connectionChanged = this.connectionChanged.bind(this);
  }

  connectionChanged(newValue) {
    console.log("connectionChanged");
    this.setState({ ...this.state, connected: newValue });
  }

  render() {
    return (
      <PokerAnalyserView>
        <PokerAnalyserHeader />
        <PokerAnalyserConnect
          connected={this.state.connected}
          pressConnect={this.connectionChanged}
        />
        <PokerAnalyserCard table={getTableData()} />
      </PokerAnalyserView>
    );
  }
}
