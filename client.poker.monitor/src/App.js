import React, { Component } from 'react';
import SocketIOClient from 'socket.io-client';

import {
  Text,
  View,
  Platform,
} from 'react-native';

class App extends Component {
  state = {
    table:{}
  }

  componentDidMount() {
    this.socket = SocketIOClient(`http://poker_app.ddns.net:5000`);
    console.log('socket created...');
    this.socket.on('tablestatus', (message) => {
      console.log(`Message:${message} received`);
      this.setState({ table : message});
    })
  }

  render() {

    return (
      <View>
        <Text>{this.state.table}</Text>
      </View>
    );
  }
}

let hotWrapper = () => () => App;
if (Platform.OS === 'web') {
  const { hot } = require('react-hot-loader');
  hotWrapper = hot;
}

export default hotWrapper(module)(App);
