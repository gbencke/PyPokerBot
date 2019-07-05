import React, {Component} from 'react';
import { View } from 'react-native';
import PokerAnalyserHeroHand from './PokerAnalyserHeroHand';
import PokerAnalyserFlopCards from './PokerAnalyserFlopCards';

export default class PokerAnalyserCard extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  render(){
    return (
      <View style={{ flexDirection: "row" }}>
        <PokerAnalyserHeroHand table={this.table}/>
        <PokerAnalyserFlopCards table={this.table}/>
      </View>
    );
  }
}

