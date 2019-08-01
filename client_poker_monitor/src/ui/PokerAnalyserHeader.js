import React from "react";
import { View } from "react-native";
import { Toolbar } from "react-native-material-ui";

export default PokerAnalyserHeader = props => {
  MenuPressed = label => {
    if (props.onHistory && label.index === 0) {
      props.onHistory();
    }
    if (props.onAbout && label.index === 1) {
      props.onAbout();
    }
  };

  return (
    <View style={styles.toolbarStyle}>
      <Toolbar
        style={styles.toolbarStyle}
        centerElement="Poker Assistant"
        rightElement={{
          menu: {
            icon: "more-vert",
            labels: ["History", "About"]
          }
        }}
        onRightElementPress={label => this.MenuPressed(label)}
      />
    </View>
  );
};

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
