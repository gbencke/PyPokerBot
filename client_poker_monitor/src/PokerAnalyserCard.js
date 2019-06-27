import React, {Component} from 'react';
import { View, Text, TextInput } from 'react-native';
import { Card } from 'react-native-material-ui';

export default class PokerAnalyserCard extends Component {
  constructor(props){
    super(props)
  }

  render(){
    return (
      <View style={styles.ViewStyle}>
        <Card style={styles.CardStyle}>
          <Text>Texto da questao...</Text>
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
    //marginRight: 20,
    //marginLeft: 20,
  },
  CardStyle : {
  }
};

