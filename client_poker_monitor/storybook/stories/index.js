import React from "react";
import { Dimensions } from "react-native";

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

const currentDimensions = Dimensions.get("window");

const PokerStories = storiesOf("PokerApp", module);

PokerStories.addDecorator(withKnobs);
//PokerStories.addDecorator(getStory => <View>{getStory()}</View>);

const currentWidth = Math.floor(Dimensions.get("window").width / 10) * 10;

const numberOptions = {
  range: true,
  min: 200,
  max: 410,
  step: 10
};

PokerStories.add("Show Cards (0)", () => {
  const width = number("width", currentWidth, numberOptions);

  if (isNaN(width)) return null;

  return (
    <PokerAnalyserCard noMargin={true} width={width} table={getTableData(0)} />
  );
});

PokerStories.add("Show Cards (1)", () => {
  const width = number("width", currentWidth, numberOptions);

  return (
    <PokerAnalyserCard
      noMargin={true}
      width={width}
      table={getTableData(getNumTableData() - 1)}
    />
  );
});

PokerStories.add("TestAnimation", () => <TestAnimationCard />);

PokerStories.add("HeaderTest", () => <TestHeader tables={getAllTableData()} />);

PokerStories.add("ConnectTest", () => <TestConnect />);
