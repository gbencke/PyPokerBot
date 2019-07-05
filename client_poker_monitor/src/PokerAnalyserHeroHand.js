
import React, {Component} from 'react';
import { Dimensions, Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';
import FitImage from 'react-native-fit-image';
import PokerAnalyserPlayersCards from './PokerAnalyserPlayersCards';
import PokerAnalyserHandStatus from './PokerAnalyserHandStatus';

const CardTemplate = require('./templates/card2.jpg');
const factor = 15; 

export default class PokerAnalyserHeroHand extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  render(){
    return (
      <View style={{ flexDirection: "column"}}>
        <View style={styles.CardStyle}>
          <Text>CURRENT HAND:</Text>
        </View>
        <View style={styles.CardStyle}>
          <Text style={styles.CardTextFont}>
              { getCardCode(this.table.hero.hero_cards) }
          </Text>
        </View>
      </View>
    );
  }
}

const styles = {
  CardStyle : {
    marginLeft: 10,
    marginRight:10
  },
  CardTextFont: {
    marginTop: 10,
    fontFamily: 'cards',
    fontSize: 48,
    width: '100%',
    textAlign: 'center'
  }
};

