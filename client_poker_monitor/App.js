/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, { Component } from "react";
import { Platform } from "react-native";
import PokerAnalyser from "./src/ui/PokerAnalyser";
import ErrorBoundary from "./src/ui/ErrorBoundary";
import StorybookUI from "./storybook";

/* eslint-disable-next-line */
export default class App extends Component {
  constructor(props) {
    super(props);
    if (Platform.OS === "ios") {
      this.useStoryBook = true;
    } else {
      this.useStoryBook = (process.env.REACT_APP_USE_SB == "true");
    }
    this.resolveUI.bind(this);
  }

  resolveUI() {
    if (this.useStoryBook) {
      return <StorybookUI />;
    } else {
      return <PokerAnalyser />;
    }
  }

  render() {
    console.disableYellowBox = true;
    return <ErrorBoundary>{this.resolveUI()}</ErrorBoundary>;
  }
}
