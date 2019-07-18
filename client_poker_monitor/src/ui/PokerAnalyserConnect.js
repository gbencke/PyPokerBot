import React, { Component } from "react";
import { View, Text, TextInput } from "react-native";
import { Button, Container, Card } from "react-native-material-ui";
import styled from "styled-components/native";

const LabelView = styled.View`
  margin-top: 12;
  margin-bottom: 12;
  margin-right: 20;
  margin-left: 20;
  align-items: flex-start;
  justify-content: flex-start;
`;

const LabelText = styled.Text`
  font-family: Arial;
  font-size: 16;
  text-align: left;
  color: ${props => props.isError ? '#FF0000' : '#000000'};
`;

const ConnectView = styled.View`
  flex-direction: row;
  justify-content: space-between;
  margin-right: 20;
  margin-left: 20;
`;

const ConnectTextField = styled.TextInput`
  padding-top: 4;
  padding-bottom: 4;
  flex: 1;
  margin-right: 20;
  border-width: 1;
  border-color: #dddddd;
`;

const styles = {
  ConnectButton: {
    flex: 1
  },
  DisconnectButton: {
    flex: 1
  }
};

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
    if (this.props.status === "connected") {
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
        <LabelView>
          <LabelText isError={this.props.status === "error"}>
            {this.props.ConnectTextInfo}
          </LabelText>
        </LabelView>
        <ConnectView>
          <ConnectTextField
            value={this.state.currentAddress}
            onChangeText={this.changeText}
          />
          {this.renderButton()}
        </ConnectView>
      </View>
    );
  }
}
