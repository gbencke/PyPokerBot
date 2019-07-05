import React, {Component} from 'react';
import { Dimensions, Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';
import FitImage from 'react-native-fit-image';
import PokerAnalyserPlayersCards from './PokerAnalyserPlayersCards';
import PokerAnalyserHandStatus from './PokerAnalyserHandStatus';

const CardTemplate = require('./templates/card2.jpg');
const factor = 15; 

export default class PokerAnalyserCard extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  render(){
    return (
      <View style={styles.ViewStyle}>
        <Card >
          <PokerAnalyserPlayersCards table={this.table}/>
          <PokerAnalyserHandStatus table={this.table}/>
        </Card>
      </View>
    );
  }
}

const styles = {
  ViewStyle: {
    width: '100%',
    paddingRight: 12,
    paddingLeft: 12,
    marginTop: 30,
    height: 400
  }
};

