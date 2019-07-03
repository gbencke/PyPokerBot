import React, {Component} from 'react';
import { Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';


export default class PokerAnalyserCard extends Component {
  constructor(props){
    super(props)
    this.table = props.table;
    this.tableType = `${this.table.image_platform} (${this.table.image_tabletype})`;
  }

  render(){
    return (
      <View style={styles.ViewStyle}>
        <Card >
          <View style={styles.CardStyle}>
            <Text style={styles.CardText}>{ this.tableType }</Text>
            <Text style={styles.CardTextFont}>{ getCardCode('AsAh') }</Text>
          </View>
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
  },
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

