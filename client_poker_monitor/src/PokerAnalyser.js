import React, {Component} from 'react';
import PokerAnalyserContainer from './PokerAnalyserContainer';
import PokerAnalyserConnect from './PokerAnalyserConnect';
import PokerAnalyserHeader from './PokerAnalyserHeader';
import PokerAnalyserCard from './PokerAnalyserCard';
import getTableData from './test/tableData';

export default class PokerAnalyser extends Component {


  constructor(props){
    super(props); 
    this.state = {
      connected : false
    };
    this.connectionChanged = this.connectionChanged.bind(this);
  }

  connectionChanged(newValue){
    console.log("connectionChanged");
    this.setState({...this.state, connected: newValue});
  }

  render(){
    return (
      <PokerAnalyserContainer>
        <PokerAnalyserHeader/>
        <PokerAnalyserConnect
          connected={this.state.connected}
          pressConnect={this.connectionChanged}
        />
          <PokerAnalyserCard/>
        </PokerAnalyserContainer>
    );
  }
}
