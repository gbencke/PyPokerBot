import React, {Component} from 'react';
import { Button } from 'react-native-material-ui';
import { Text, View } from 'react-native';

export default class PokerAnalyserDecision extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
    this.state = { currentOpacity : 1.0 }
  }

  componentDidMount(){
    this.interval = setInterval(() => {
      nextState = this.state.currentOpacity - 0.1;
      console.log(`nextState:${nextState}`);
      if(nextState < 0.3){
        nextState = 1.0;
      }
      this.setState ({ currentOpacity : nextState });
    }, 100);
  }

  render(){
    
    let currentStyle = {...styles.CommandsView, opacity : this.state.currentOpacity };

    return (
      <View style={currentStyle}>
        <Text style = {styles.DecisionText }> { this.table.decision.decision } </Text>
      </View>
    );
  }
}

let styles = {
  DecisionText : {
    fontSize: 36,
    fontWeight: '800'
  },
  CommandsView : {
    width: '100%',
    flexDirection: "row",
    justifyContent: "center",
    marginTop: 20,
    marginBottom: 20,
    marginLeft: 10,
    marginRight:10
  },
};
