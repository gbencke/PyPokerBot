import React, {Component} from 'react';
import { View } from 'react-native';
import { Card } from 'react-native-material-ui';
import PokerAnalyserPlayersCards from './PokerAnalyserPlayersCards';
import PokerAnalyserHandStatus from './PokerAnalyserHandStatus';

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

