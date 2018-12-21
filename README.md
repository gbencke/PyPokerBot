# PyPokerBot

As an amateur poker player, I always thought that Online Poker is a very interesting domain for AI Techniques and Third-Party Desktop Application Automation Techniques using computer vision, so I created PyPokerBot which is a project to study the use of OpenCV in order to create a working poker bot that using only Win32 API can interact with PokerStars Poker Client. 

The first implementation only implements a simple decision tree for poker decisions as the focus is object detection and interaction with the poker client.

PokerAI is a very hot topic in machine learning, as it is very difficult to implement a competitive AI. Such AI would have to be very good at dealing with incomplete information, which is the fact that you have to take a decision without having all necessary information at hand. 

*In a game with complete information as chess or go, all players have all the information to make a decision available. In Poker, you have to make a decision based on your own pocket cards (which is available), the estimation of your opponents cards and their decision-making logic* 

As we need to "Learn" the characteristics and decision-making characteristics of the opposing player (which is by far the most important feature), deep learning techniques have being widely used as they employ non-linear decision-making which is more suited for a scenario where the player varies a lot their playing styles.

If you are interested on Poker and PokerAI, I recommend the following books that were very useful for me in order to understand Modern Poker:

* **[The Theory of Poker: A Professional Poker Player Teaches You How To Think Like One](https://www.amazon.com/Theory-Poker-Professional-Player-Teaches/dp/1880685000/ref=sr_1_1?s=books&ie=UTF8&qid=1498340224&sr=1-1&keywords=The+Theory+of+Poker)**: This is the classic Book that although is kind of outdated for most of its examples and poker styles, it contains yet a good analysis of the essence of poker and a firm theory basis that is applied for all kinds of poker from yesterday, today and tomorrow.  

* **[No Limit Hold 'em Theory and Practice (David Sklansky, Ed Miller).pdf](https://www.amazon.com/No-Limit-Hold-Theory-Practice/dp/188068537X/ref=sr_1_1?s=books&ie=UTF8&qid=1498340204&sr=1-1&keywords=No+Limit+Hold+%27em+Theory+and+Practice)**: This is book is a continuation of the above book (Theory of Poker), but focuses then on Texas Hold'em which is the currently most practice poker style both online and live.    

* **[Harrington on Online Cash Games; 6-Max No-Limit Hold’em](https://www.amazon.com/Harrington-Online-Games-6-Max-No-Limit/dp/1880685493/ref=sr_1_1?s=books&ie=UTF8&qid=1498340552&sr=1-1&keywords=Harrington+on+Online+Cash+Games%3B+6-Max+No-Limit+Hold%E2%80%99em)**: Since the beginning of online poker on the late 1990s it has evolved a lot and there is a lot of competing sites and also online poker is the new standard and not live. Harrington give us an analysis on such changes and also the impact on the game. As this is a book written in 2010, in my opinion it underestimates the current level of online poker. Today even very micro-stakes like NL2 (where the bet is 0.02 dollar) show a very good player level and can be quite challenging for the beginners.

* **[Zen and the Art of Poker: Timeless Secrets to Transform Your Game](https://www.amazon.com/Zen-Art-Poker-Timeless-Transform/dp/0452281261/ref=sr_1_1?s=books&ie=UTF8&qid=1498340320&sr=1-1&keywords=Phillips_Zen_and_the_art_of_poker)**: As a Zen Meditation Practitioner, I found this book extremely useful in improving my play. Concepts as Patience, the Action of Non-Action and a deep observation of one self's behavior are key in order to improve your play and also optimize the win-loss ration of a poker session.  If you practice meditation and values Zen Philosophy this is a must-read book.

There is a lot of academic papers and research regarding poker AI, the sources that I recommend are:

* **[University of Alberta Computer Poker Research Group](http://poker.cs.ualberta.ca/)**: This is a computer science group specialized on poker analytics. Using Deep Learning they are today the State-of-Art on PokerAI
* **[MIT Poker Bots](http://mitpokerbots.com/)** Annual Competition on MIT for pokerbots, this is a reference competition for PokerAI.

## Architecture

The current software architecture uses 2 layers, one on Linux that calculate poker hand odds, and the other on Windows that interacts with the poker client.

* **Server**: The Server calculates hands equities, which are the probabilities that a certain set of cards will win the hand. 
	* For that it uses a C library called [pbots_calc](https://github.com/mitpokerbots/pbots_calc) from the mitpokerbot competition. 
	* It implements a REST API using [Flask MicroFramework](http://flask.pocoo.org/) that exposes the C library functions to be consumed by the client application.
* **Client**: The Client is a command-line application that detects the poker client, captures a screenshot, analyses the image, make a decision and send the command to the poker client. As a command-line tool it has several commands that set its use, for each command it has a particular set of functionalities. 
	* It is important to notice that each command extends the funcionality of other. For a more detailed description of each, please see the [Usage Section](#UsageSection) below.    
	*  **generate_samples**: 
	*  **grab_image**:
	*  **analyse_image**:
	*  **hud**:
	*  **play**:





## Requirements and Installation

### Server

### Client

## Usage

### Server

### Client

#### generate_samples
 
#### grab_image

#### analyse_image

#### hud

#### play


## Implementation Details

### Server

#### Poker Odds Calculation

#### REST API

### Client

#### Screenshot Grab

#### Image Analisys

#### Decision Making

## Current Status and Improvements

