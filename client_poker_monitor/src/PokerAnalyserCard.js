import React, {Component} from 'react';
import { Dimensions, Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';
import FitImage from 'react-native-fit-image';

const CardTemplate = require('./templates/card2.jpg');

export default class PokerAnalyserCard extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  getTableType(){
    return  `${this.table.image_platform} (${this.table.image_tabletype})`;
  }

  RenderPlayersCardsView(){
    return (
      <View style={styles.PlayersCardsView}>
          { this.RenderPlayersCards() }
      </View>
    );
  }

  RenderCard(key){

    const factor = 15; 

    const PlayingCardViewStyle = { 
      width : '16%', 
      flexDirection: 'row' ,
      justifyContent: 'space-between'
    };

    const RenderedCardStyle = { 
      width: Dimensions.get('window').width / factor ,
      height: Dimensions.get('window').height / factor 
    };

    return (
      <View key={ key } style={ {flexDirection: 'column', width: '16%' }}>
        <View style= { PlayingCardViewStyle }>
          <FitImage
            source = { CardTemplate }
            style = { RenderedCardStyle } />
          <FitImage
            source = { CardTemplate }
            style = { RenderedCardStyle } />
        </View>
        <Text style={{width:'100%', textAlign:'center'}}>AA</Text>
      </View>
    );
  }

  RenderNoCard(key){
    return (
      <View key={ key } style={{ flex: 1, justifyContent:'flex-end',alignItems:'center'}}>
        <Text>No</Text>
      </View>
    )
  }

  RenderPlayersCards(){
    return this.table.cards.map( (item, i) => {
      return item ? this.RenderCard(i) : this.RenderNoCard(i) 
    });
  }

  render(){
    return (
      <View style={styles.ViewStyle}>
        <Card >
          <View style={styles.CardStyle}>
            <Text style={styles.CardText}>{ this.getTableType() }</Text>
              { this.RenderPlayersCardsView() }
          </View>
        </Card>
      </View>
    );
  }
}

const styles = {
  PlayingCard: {
    flexDirection: 'row',
    justifyContent: 'center'
  },
  ViewStyle: {
    width: '100%',
    paddingRight: 12,
    paddingLeft: 12,
    marginTop: 30,
    height: 400
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
  },
  PlayersCardsView: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  }
};

