
/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, {Component} from 'react';
import { View, Text } from 'react-native';

/* eslint-disable-next-line */
export default class ErrorBoundary extends Component {

  constructor(props){
    super(props);
    this.state = { hasError : false, error : '' };
  }

  componentDidCatch(error, errorInfo){
    this.errorInfo = errorInfo;
  }

  static getDerivedStateFromError(error){
    return { hasError: true, error : error };
  }

  render() {
    if(this.state.hasError){
      return (
        <View>
          <Text>Error on Poker App</Text>
          <Text>{JSON.stringify(this.state.error)}</Text>
        </View>
      );
    }
    //<Text>{JSON.stringify(this.errorInfo ? this.errorInfo : '')}</Text>
    return this.props.children;
  }
}
