import React, { Component } from "react";
import { View, Text, TextInput } from "react-native";
import { Button, Container, Card } from "react-native-material-ui";

export default class PokerAnalyserConnect extends Component {
  constructor(props) {
    super(props);
    this.state = { currentAddress: props.initialAddress };
    this.props = props;

    this.changeText = this.changeText.bind(this);
    this.pressedConnect = this.pressedConnect.bind(this);
  }

  pressedConnect() {
    this.props.pressConnect(this.state.currentAddress);
  }

  renderButton() {
    if (this.props.status === "Connected") {
      return (
        <Button
          style={styles.DisconnectButton}
          raised
          accent
          onPress={this.pressedConnect}
          text="Disconnect"
        />
      );
    } else {
      return (
        <Button
          style={styles.ConnectButton}
          raised
          primary
          onPress={this.pressedConnect}
          text="Connect"
        />
      );
    }
  }

  changeText(x) {
    this.setState({ ...this.state, currentAddress: x });
  }

  render() {
    return (
      <View style={{}}>
        <View style={styles.LabelView}>
          <Text style={styles.LabelText}>{this.props.ConnectTextInfo}</Text>
        </View>
        <View style={styles.ConnectView}>
          <TextInput
            value={this.state.currentAddress}
            style={styles.ConnectTextField}
            onChangeText={this.changeText}
          />
          {this.renderButton()}
        </View>
      </View>
    );
  }
}

const styles = {
  LabelView: {
    marginTop: 12,
    marginBottom: 12,
    alignItens: "center",
    justifyContent: "center"
  },
  LabelText: {
    fontFamily: "Arial",
    fontSize: 16,
    textAlign: "center"
  },
  ConnectView: {
    flexDirection: "row",
    alignItens: "space-between",
    justifyContent: "space-between",
    marginRight: 20,
    marginLeft: 20
  },
  ConnectTextField: {
    paddingTop: 4,
    paddingBottom: 4,
    flex: 1,
    marginRight: 20,
    borderWidth: 1,
    borderColor: "#ddd"
  },
  ConnectButton: {
    flex: 1
  },
  DisconnectButton: {
    flex: 1
  }
};
