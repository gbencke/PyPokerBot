import { View, StyleSheet } from 'react-native';
import React, { Component } from 'react';
import { PropTypes } from 'prop-types';

const propTypes = {
  children: PropTypes.node.isRequired,
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row'
  },
});

class PokerContainer extends Component {
  render() {
    return (
      <View style={styles.container}>
          {this.props.children}
      </View>
    );
  }
}

PokerContainer.propTypes = propTypes;

export default PokerContainer;
