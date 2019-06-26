
import React, {Component} from 'react';
import { View, Text, TextInput } from 'react-native';
import { Button, Container, Card } from 'react-native-material-ui';
import PokerContainer from './PokerContainer';

export default class PokerAnalyserConnect extends Component {

  ConnectInfoText = "Please Enter your Connection Info to the Poker Client";

  render(){

    return (
      <View style = {{ }}>
        <View style={styles.LabelView}>
          <Text style={styles.LabelText} >{this.ConnectInfoText}</Text>
        </View>
        <View style={styles.ConnectView}>
          <TextInput style= { styles.ConnectTextField } />
          <Button style = { styles.ConnectButton } raised primary text="Connect"/>
        </View>
      </View>
    );
  }
}

const styles = {
  LabelView : {
    marginTop: 12,
    marginBottom: 12,
    alignItens: 'center',
    justifyContent: 'center',
  },
  LabelText : {
    fontFamily : 'Arial',
    fontSize: 16,
    textAlign: 'center'
  },
  ConnectView : {
    flexDirection : 'row',
    alignItens: 'space-between',
    justifyContent: 'space-between',
    marginRight: 20,
    marginLeft: 20,
  },
  ConnectTextField : {
    paddingTop: 4,
    paddingBottom: 4,
    flex: 1,
    marginRight: 20,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  ConnectButton : {
    flex: 1,
  }
}
