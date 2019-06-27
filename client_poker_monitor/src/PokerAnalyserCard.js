import React, {Component} from 'react';
import { Image, View, Text } from 'react-native';
import { Card } from 'react-native-material-ui';
import { getImagesTemplates } from './ImageTemplates';


export default class PokerAnalyserCard extends Component {
  constructor(props){
    super(props)
    this.table = props.table;
    this.tableType = `${this.table.image_platform} (${this.table.image_tabletype})`;
    this.imagesTemplates = getImagesTemplates();
  }

  render(){
    return (
      <View style={styles.ViewStyle}>
        <Card style={styles.CardStyle}>
          <Text>{ this.tableType }</Text>
          <Image 
            source={ this.imagesTemplates['Ah'] }
            style={{width:60, height:50}}
          />
          <Image 
            source={ this.imagesTemplates['As'] }
            style={{width:60, height:50}}
          />
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

