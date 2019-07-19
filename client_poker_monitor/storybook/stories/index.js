import React from "react";
import { View } from "react-native";

import { storiesOf } from "@storybook/react-native";
import { withKnobs, number } from "@storybook/addon-knobs";

import TestAnimationCard from "../../src/test/TestAnimationCard";
import TestConnect from "../../src/test/TestConnect";
import TestHeader from "../../src/test/TestHeader";

import {
  getAllTableData,
  getNumTableData,
  getTableData
} from "../../src/test/tableData";
import PokerAnalyserCard from "../../src/ui/PokerAnalyserCard";

const PokerStories = storiesOf("PokerApp", module);

PokerStories.addDecorator(withKnobs);
//PokerStories.addDecorator(getStory => <View>{getStory()}</View>);

PokerStories.add("Show Cards (0)", () => {
  const width = number("width", 410);

  return (
    <PokerAnalyserCard noMargin={true} width={width} table={getTableData(0)} />
  );
});

PokerStories.add("Show Cards (1)", () => (
  <PokerAnalyserCard table={getTableData(getNumTableData() - 1)} />
));

PokerStories.add("TestAnimation", () => <TestAnimationCard />);

PokerStories.add("HeaderTest", () => <TestHeader tables={getAllTableData()} />);

PokerStories.add("ConnectTest", () => <TestConnect />);
