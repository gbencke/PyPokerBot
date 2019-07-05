import React, {Component} from 'react';
import { Button } from 'react-native-material-ui';
import { Text, View } from 'react-native';

export default class PokerAnalyserCommands extends Component {

  constructor(props){
    super(props)
    this.table = props.table;
  }

  getCommandText(index){
    let ret = this.table.commands[index][2].trim();
    console.log(ret);
    ret = ret.replace('[1]','CALL');
    if(ret==='20'){
      return 'FOLD';
    }
    return ret;
  }

  render(){
    return (
      <View style={ styles.CommandsView }>
        <Text>AVAILABLE COMMANDS</Text>
        <View style={ styles.ButtonCommandsView }>
          <Button style= { styles.ButtonStyle } raised accent text={ this.getCommandText(0) }/>
          <Button style= { styles.ButtonStyle } raised accent text={ this.getCommandText(1) }/>
          <Button style= { styles.ButtonStyle } raised accent text={ this.getCommandText(2) }/>
        </View>
      </View>
    );
  }
}

const styles = {
  ButtonStyle : {
    container : {
      minWidth: 100
    }
  },
  CommandsView : {
    flexDirection: "column",
    marginTop: 10,
    marginLeft: 10,
    marginRight:10
  },
  ButtonCommandsView : {
    marginTop:10,
    flexDirection: "row",
    justifyContent: "space-between"
  }
};
