import React, { Component } from "react";
import { Text, Dimensions, View } from "react-native";
import { Button, Card } from "react-native-material-ui";
import { getNumTableData, getTableData } from "./tableData";

const currentDimensions = Dimensions.get("window");

export default class TestAnimationCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cardA: <PokerAnalyserCard table={getTableData(0)} />,
      cardB: <PokerAnalyserCard table={getTableData(getNumTableData() - 1)} />,
      animating: false,
      step: 0
    };
    this.testePress = this.testePress.bind(this);
    this.intervalStep = this.intervalStep.bind(this);
  }

  intervalStep() {
    console.log("intervalStep ok...");
    let newState = {};

    width2ndPos = this.calculate2ndCard(
      currentDimensions.width,
      this.state.step
    );
    if (width2ndPos < 11) {
      newState = { ...this.state, animation: false, step: 0 };
      newState.cardA = newState.cardB;
    } else {
      newState = { ...this.state, step: (this.state.step += 32) };
      setTimeout(() => this.intervalStep(), 0);
    }
    this.setState(newState);
  }

  testePress() {
    if (!this.state.animation) {
      setTimeout(() => this.intervalStep(), 0);

      let pressedState = { ...this.state, animation: true };
      this.setState(pressedState);
    } else {
      let pressedState = { ...this.state, animation: false };
      this.setState(pressedState);
    }
  }

  calculate2ndCard(totalWidth, step) {
    return parseInt(totalWidth + 10 - step * 1);
  }

  render() {
    const newStyle = {
      ...styles.MovableCard,
      position: "absolute",
      top: 0,
      left: 0 - this.state.step * 1
    };

    const newCardnewStyle = {
      ...newStyle,
      left: this.calculate2ndCard(currentDimensions.width, this.state.step)
    };

    return (
      <View style={styles.ViewStyle}>
        <Button onPress={this.testePress} raised accent text="Run Animation" />
        <View style={styles.CardStyle}>
          <View style={newStyle}>{this.state.cardA}</View>
          <View style={newCardnewStyle}>{this.state.cardB}</View>
        </View>
      </View>
    );
  }
}

let styles = {
  MovableCard: {},
  ViewStyle: {
    marginTop: 30,
    width: currentDimensions.width,
    justifyContent: "space-between",
    alignItems: "flex-start",
    overflow: "hidden"
  },
  CardStyle: {
    width: currentDimensions.width,
    overflow: "hidden",
    height: "100%"
  }
};
