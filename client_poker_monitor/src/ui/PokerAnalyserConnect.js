import React, { Component } from "react";
import { View } from "react-native";
import { Button } from "react-native-material-ui";
import styled from "styled-components/native";

const LabelView = styled.View`
  margin-top: ${props => parseInt((12 / 410) * props.totalWidth)};
  margin-bottom: ${props => parseInt((12 / 410) * props.totalWidth)};
  margin-right: ${props => parseInt((20 / 410) * props.totalWidth)};
  margin-left: ${props => parseInt((20 / 410) * props.totalWidth)};
  align-items: flex-start;
  justify-content: flex-start;
`;

const LabelText = styled.Text`
  font-family: Arial;
  font-size: ${props => parseInt((16 / 410) * props.totalWidth)};
  text-align: left;
  color: ${props => (props.isError ? "#FF0000" : "#000000")};
`;

const ConnectView = styled.View`
  flex-direction: row;
  justify-content: space-between;
  margin-right: ${props => parseInt((20 / 410) * props.totalWidth)};
  margin-left: ${props => parseInt((20 / 410) * props.totalWidth)};
`;

const ConnectTextField = styled.TextInput`
  padding-top: 4;
  padding-bottom: 4;
  flex: 1;
  margin-right: ${props => parseInt((20 / 410) * props.totalWidth)};
  border-width: 1;
  border-color: #dddddd;
  font-size: ${props => parseInt((16 / 410) * props.totalWidth)};
`;

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
    const styles = {
      ConnectButton: {
        flex: 1,
        container: {
          width: parseInt((120 / 410) * this.props.totalWidth)
        },
        text: {
          fontSize: parseInt((14 / 410) * this.props.totalWidth)
        }
      },
      DisconnectButton: {
        flex: 1,
        container: {
          width: parseInt((120 / 410) * this.props.totalWidth)
        },
        text: {
          fontSize: parseInt((14 / 410) * this.props.totalWidth)
        }
      }
    };

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

  componentWillReceiveProps(props) {
    this.setState({ ...this.state, currentAddress: props.initialAddress });
  }

  render() {
    return (
      <View style={{}}>
        <LabelView totalWidth={this.props.totalWidth}>
          <LabelText
            totalWidth={this.props.totalWidth}
            isError={this.props.status === "error"}
          >
            {this.props.ConnectTextInfo}
          </LabelText>
        </LabelView>
        <ConnectView totalWidth={this.props.totalWidth}>
          <ConnectTextField
            totalWidth={this.props.totalWidth}
            value={this.state.currentAddress}
            onChangeText={this.changeText}
          />
          {this.renderButton()}
        </ConnectView>
      </View>
    );
  }
}
