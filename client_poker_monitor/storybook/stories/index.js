import React from 'react';
import { Text } from 'react-native';

import { storiesOf } from '@storybook/react-native';
import { action } from '@storybook/addon-actions';
import { linkTo } from '@storybook/addon-links';

import Button from './Button';
import CenterView from './CenterView';
import Welcome from './Welcome';


storiesOf('Welcome', module).add('to Storybook', () => <Welcome showApp={linkTo('Button')} />);

import { getNumTableData, getTableData } from '../../src/test/tableData';
import PokerAnalyserCard from '../../src/PokerAnalyserCard';

storiesOf('PokerApp', module)
  .addDecorator(getStory => <CenterView>{getStory()}</CenterView>)
  .add('Show Cards (0)', () => (
    <PokerAnalyserCard table={getTableData(0)}/>
  ));

storiesOf('PokerApp', module)
  .addDecorator(getStory => <CenterView>{getStory()}</CenterView>)
  .add('Show Cards (1)', () => (
    <PokerAnalyserCard table={getTableData(getNumTableData()-1)}/>
  ));
