
import React, {Component} from 'react';
import { View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';

export default class PokerAnalyserFlopCards extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  render(){
    return (
      <View style={{ flexDirection: "column"}}>
        <View style={styles.CardStyle}>
          <Text>FLOP({`${this.table.hand_analisys.hand_phase}`})</Text>
        </View>
        <View style={styles.CardStyle}>
          <Text style={styles.CardTextFont}>
              { getCardCode(this.table.flop.join('')) }
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

