import React, {Component} from 'react';
import PokerAnalyserContainer from './PokerAnalyserContainer';
import PokerAnalyserConnect from './PokerAnalyserConnect';
import PokerAnalyserHeader from './PokerAnalyserHeader';

export default class PokerAnalyser extends Component {

  render(){
    return (
      <PokerAnalyserContainer>
        <PokerAnalyserHeader/>
        <PokerAnalyserConnect/>
      </PokerAnalyserContainer>
    );
  }
}
