import React, {Component} from 'react';
import { Dimensions, Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getCardCode } from './helpers/getCardCode';
import FitImage from 'react-native-fit-image';

const CardTemplate = require('./templates/card2.jpg');
const factor = 15; 

export default class PokerAnalyserPlayersCards extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  RenderCard(key){
    return (
      <View key={ key } style={ {flexDirection: 'column', width: '16%' }}>
        <View style= { styles.WithCardPlayingCardViewStyle }>
          <FitImage
            source = { CardTemplate }
            style = { styles.WithCardRenderedCardStyle } />
          <FitImage
            source = { CardTemplate }
            style = { styles.WithCardRenderedCardStyle } />
        </View>
        <Text style={{width:'100%', textAlign:'center'}}>{`AA - ${key}`}</Text>
      </View>
    );
  }

  RenderNoCard(key){
    return (
      <View key={ key } style={styles.NoCardStyle}>
        <Text style= { styles.NoCardRenderedCardStyle }></Text>
        <Text>{`No - ${key}`}</Text>
      </View>
    );
  }

  RenderPlayersCards(){
    return this.table.cards.map( (item, i) => {
      return item ? this.RenderCard(i) : this.RenderNoCard(i) 
    });
  }

  RenderPlayersCardsView(){
    return (
      <View style={styles.PlayersCardsView}>
          { this.RenderPlayersCards() }
      </View>
    );
  }

  getTableType(){
    return  `${this.table.image_platform} (${this.table.image_tabletype})`;
  }

  render(){
    console.log(`PlayersCard:${JSON.stringify(styles.WithCardRenderedCardStyle)}`);
    return (
      <View style={styles.CardStyle}>
        <Text style={styles.CardText}>{ this.getTableType() }</Text>
          { this.RenderPlayersCardsView() }
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
    marginTop: 30
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
  },
  WithCardPlayingCardViewStyle : { 
    width : '16%', 
    flexDirection: 'row' ,
    justifyContent: 'space-between'
  },
  WithCardRenderedCardStyle : { 
    width: Dimensions.get('window').width / factor ,
    height: Dimensions.get('window').height / factor 
  },
  NoCardStyle : { 
    flex: 1, 
    justifyContent:'flex-end',
    alignItems:'center',
  },
  NoCardRenderedCardStyle : { 
    width: Dimensions.get('window').width / factor * 2,
    height: Dimensions.get('window').height / factor ,
    borderWidth: 1,
    borderRadius : 1,
    borderStyle: 'dashed',
    borderColor: '#000'
  }
};


