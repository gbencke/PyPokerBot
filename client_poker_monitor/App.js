/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {Component} from 'react';
import PokerAnalyser from './src/PokerAnalyser'
import StorybookUI from './storybook'

/* ieslint-disable-next-line */
export default class App extends Component {

  constructor(props){
    super(props);
    this.useStoryBook = process.env.REACT_APP_USE_SB;
  }

  render() {
    if(this.useStoryBook){
      return <StorybookUI/>;
    }else{
      return <PokerAnalyser/>;
    }
  }
}
