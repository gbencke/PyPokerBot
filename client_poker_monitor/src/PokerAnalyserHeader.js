import React, {Component} from 'react';
import { View } from 'react-native';
import { Toolbar } from 'react-native-material-ui'

export default class PokerAnalyserHeader extends Component {

  render(){
    return (
      <View>
        <Toolbar centerElement="Poker Assistant"/>
      </View>
    );
  }
}
