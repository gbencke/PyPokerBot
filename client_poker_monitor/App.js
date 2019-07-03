/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {Component} from 'react';
import PokerAnalyser from './src/PokerAnalyser'
import ErrorBoundary from './src/ErrorBoundary'
import StorybookUI from './storybook'

/* ieslint-disable-next-line */
export default class App extends Component {

  constructor(props){
    super(props);
    this.useStoryBook = process.env.REACT_APP_USE_SB;
    this.resolveUI.bind(this);
  }

  resolveUI(){
    if(this.useStoryBook){
      return <StorybookUI/>;
    }else{
      return <PokerAnalyser/>;
    }
  }

  render() {
    return <ErrorBoundary>{ this.resolveUI() }</ErrorBoundary>
  }
}
