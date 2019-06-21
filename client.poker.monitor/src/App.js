import axios from 'axios';
import React, { Component } from 'react';
import SocketIOClient from 'socket.io-client';

import {
  Text,
  View,
  Platform,
} from 'react-native';

class App extends Component {
  state = {
    table:{},
    equity:""
  }

  componentDidMount() {
    const URL = Platform.OS === 'web' ? 'http://poker_app.ddns.net:5000' : 'http://192.168.0.10:5000'

    this.setState({...this.state, "URL": URL});
    this.socket = SocketIOClient(URL);
    console.log('socket created...');
    this.socket.on('tablestatus', (message) => {
      console.log(`Message:${message} received`);
      this.setState({ table : message});
    })
    axios.get('http://192.168.0.10:5000/ping')
      .then( (r) => {
        this.setState({...this.state, equity: JSON.stringify(r) });
      })
      .catch( (r) => {
        this.setState({...this.state, equity: JSON.stringify(r) });
      });
  }

  render() {

    return (
      <View>
        <Text>{JSON.stringify(this.state.table)}</Text>
        <Text>{this.state.URL}</Text>
        <Text>{this.state.equity}</Text>
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
