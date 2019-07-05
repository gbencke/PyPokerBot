import React, {Component} from 'react';
import { Dimensions, Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';
import FitImage from 'react-native-fit-image';
import PokerAnalyserPlayersCards from './PokerAnalyserPlayersCards';
import PokerAnalyserHandStatus from './PokerAnalyserHandStatus';
import PokerAnalyserHeroHand from './PokerAnalyserHeroHand';
import PokerAnalyserFlopCards from './PokerAnalyserFlopCards';

const CardTemplate = require('./templates/card2.jpg');
const factor = 15; 

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
