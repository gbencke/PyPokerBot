import React, {Component} from 'react';
import { Text,Dimensions, View } from 'react-native';
import { Button, Card } from 'react-native-material-ui';

const currentDimensions = Dimensions.get('window');

export default class TestAnimationCard extends Component {

  constructor(props){
    super(props)
    this.state = { cardA:'A', cardB: 'B', animating : false, step : 0 }
    this.testePress = this.testePress.bind(this);
    this.intervalStep = this.intervalStep.bind(this);
  }

  intervalStep(){
    let newState = {};

    width2ndPos = this.calculate2ndCard( currentDimensions.width, this.state.step);
    console.log(width2ndPos);
    if ( width2ndPos < 11 ) {
      newState = {...this.state, animation : false, step : 0 };
      newState.cardA = newState.cardB;
      clearInterval(this.state.timer);
    }else{
      newState = {...this.state, step: this.state.step+=16 };
    }
    this.setState(newState);
  }

  testePress(){

    let Animate = setInterval( () => this.intervalStep(), 1);

    let pressedState = {...this.state, animation: true, timer : Animate}
    this.setState(pressedState);

  }

  calculate2ndCard(totalWidth, step){
    return parseInt(((totalWidth * 0.8 * 0.9) + 10 ) - (step * 1));
  }

  render(){

    const newStyle = {
      ...styles.MovableCard, 
      width:currentDimensions.width / 10, 
      height: currentDimensions.height / 20,
      position: 'absolute',
      top: 10,
      left: 10 - (this.state.step * 1)
    };

    const newCardnewStyle = {
      ...newStyle,
      left: this.calculate2ndCard(
        currentDimensions.width, 
        this.state.step)
    };

    return (
      <View style={styles.ViewStyle}>
        <View style={styles.CardStyle}>
          <View style={newStyle}>
            <Text>{this.state.cardA}</Text>
          </View>
          <View style={newCardnewStyle}>
            <Text>{this.state.cardB}</Text>
          </View>
        </View>
        <Button onPress={ this.testePress } raised accent text="Run Animation"/>
      </View>
    );
  }
}

let styles = {
  MovableCard: {
    borderWidth: 2,
    borderColor: '$000',
  },
  ViewStyle:{
    backgoundColor: '#FFF',
    width: '90%',
    paddingRight: 12,
    paddingLeft: 12,
    marginTop: 30,
    marginLeft: 30,
    marginRight: 30,
    borderWidth: 2,
    borderColor: '$FFF',
    height: '70%',
    justifyContent: 'space-between',
    alignItems: 'center',
    overflow:'hidden'
  },
  CardStyle: {
    backgoundColor: '#FFF',
    width: '90%',
    paddingRight: 12,
    paddingLeft: 12,
    marginTop: 30,
    marginLeft: 30,
    marginRight: 30,
    borderWidth: 2,
    borderColor: '$FFF',
    height: '70%',
    overflow:'hidden'
  }
};

