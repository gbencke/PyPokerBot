
import React, {Component} from 'react';
import { View, Text, TextInput } from 'react-native';
import { Button, Container, Card } from 'react-native-material-ui';

export default class PokerAnalyserConnect extends Component {

  constructor(props){
    super(props)
    this.ConnectInfoText = "Please Enter your Connection Info to the Poker Client";
    this.pressConnect = this.pressConnect.bind(this);
    this.renderButton = this.renderButton.bind(this);
  }

  pressConnect(){
    console.log("pressConnect");
    this.props.pressConnect(!this.props.connected);
  }

  renderButton(){
    if(this.props.connected){
      return (
        <Button 
          style = { styles.DisconnectButton } 
          raised 
          accent 
          onPress={this.pressConnect}
          text="Disconnect"/>
      );
    }else{
      return (
        <Button 
          style = { styles.ConnectButton } 
          raised 
          primary 
          onPress={this.pressConnect}
          text="Connect"/>
      );
    }
  }

  render(){

    return (
      <View style = {{ }}>
        <View style={styles.LabelView}>
          <Text style={styles.LabelText} >{this.ConnectInfoText}</Text>
        </View>
        <View style={styles.ConnectView}>
          <TextInput style= { styles.ConnectTextField } />
            { this.renderButton() }
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
  },
  DisconnectButton : {
    flex: 1,
  }
}
