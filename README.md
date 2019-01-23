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
* **Client**: The Client is a command-line application that detects the poker client, captures a screen shot, analyses the image, make a decision and send the command to the poker client. As a command-line tool it has several commands that set its use, for each command it has a particular set of functionalities. 
	* It is important to notice that each command extends the funcionality of other. For a more detailed description of each, please see the [Usage Section](#UsageSection) below.    
	*  **generate_samples**: It is used to capture screen shots of the desktop poker client for use as samples for the PokerBot
	*  **grab_image**: Get a particular region of the image for analysis.
	*  **analyse_image**: Analyze and use computer vision to return a python dictionary with all the data and status of a screen shot of a poker client
	*  **hud**: The poker bot enters in a loop and takes screenshots of the poker table, and advises the player about the correct decision to be made (It doesn't send clicks to the poker table, so it does not play alone).
	*  **play**: In this mode, the poker bot takes screen shots and performs analysis of the playing table, it generates decisions and send the proper clicks to the poker client.


## Requirements and Installation

The Poker Bot has 2 main components, a server web application that servers calculation requests for the poker bot client, and a client that takes screen shots of playing poker tables, analyses them and send clicks.

### Server

The server is a standard python application that uses the flask framework to serve calculation requests, it can be run on any linux distribution that has support for python 2.7. the installation procedure is:

    1) download the source code from git:
        git clone https://github.com/gbencke/PyPokerBot.git
        cd PyPokerBot

    2) Install virtualenv 
        pip install virtualenv
 
    3) Create a virtualenv environment 
        virtualenv -p python2 env

    4) Activate the virtualenv
        source env/bin/activate

    5) Install the required modules and start the server
        pip install -r requirements.server.txt
        sudo ./server.sh
        
After the steps above the server will be accepting  requests on the following URL 

    http://<<server-ip>>:5000/calculator

### Client

The client is simply a python script that detects the poker tables on the Desktop computer, saves screen shots, and then analyze the image and sends clicks. For the Client, it is required:

* **Windows Operating System version 7 or above**
* **Python 2.7**: Downloaded from python.org 
* **Tesseract software**: The tesseract.exe file should be on the PATH.

In order to execute the software it is necessary to:

    1) download and install the required software above.

    2) download the source code from git:
        git clone https://github.com/gbencke/PyPokerBot.git
        cd PyPokerBot

    3) Install virtualenv 
        pip install virtualenv
 
    4) Create a virtualenv environment 
        virtualenv -p python2 env

    5) Activate the virtualenv
        env\Scripts\activate.bat

    6) Install the required modules and start the server
        pip install -r requirements.client.txt
        
After the steps above, we can execute the python client as specified on the Usage parameters below:

## Usage

The Poker Bot is very simple to use, and has several modes to execute.

### Server

The server only provides a simple URL that receives a JSON containing a calculation request as shown below: 

    { "command" : "AsTh:XX" }

and returns the result of these calculation as a python tuple with the probability of such hand being the best hand:

    [(u'AsTh:XX', 0.627141)]

The server after installation is very simple to start, just execute:

    sudo ./server.sh

### Client

The client is a simple python script that keeps taking screen shots from playing tables and sends commands to such poker desktop clients. After the install procedures above are completed, we can use the poker script as follows:

#### generate_samples
 
This Task generates a series of screen shots from the Poker desktop client that is
running on the computer. It saves them as JPEG images for later analysis. Those
samples are saved on the samples_folder key of the settings.py configuration file

Usage:

    python PyPokerBot.py generate_samples

Parameters:

**None**

Return:

**None**

Obs:

The samples are saved on the folder specified on the samples_folder key of the
dictionary returned by settings.py

#### grab_image

This task is used to debug the computer vision process that identifies the objects on the
screenshot taken from the poker table. It crops the image in a specific position and size

Usage:

    python PyPokerBot.py grab_image <Image Source> <Platform> <TableType> <Pos> <size> <FileName>


Parameters:

* **Image Source**: The Screen shot of the poker client to be used as source
* **Platform**: The poker platform from which the screen shot was taken
* **TableType**: The type of table that the screen shot was taken (6-SEAT,9-SEAT,etc...)
* **Pos**: The position to be cropped
* **Size**: The size of the image to be cropped
* **Filename to Save**: The file name for the cropped image

Return:

* **None** (But saves the image as specific in the parameter above)

Obs:

It is important to notice that the position and size specified are defined on the settings.py file.


#### analyse_image

This task analyses a screen shot of a poker table and then returns a dictionary with
the information captured from such image. It analyses the cards on the table, the
hero position and cards and also the commands available to the player.

Usage:

    python PyPokerBot.py analyze_table <Image Source> <Platform> <TableType>


Parameters:

* **Image Source**: The jpg image containing the poker table screen shot to be analyzed.
* **Platform**: The Poker Platform (Client Software) that should be considered in the analysis
* **TableType**: The Type of Table, for example, 6-SEAT, 9-SEAT or others.

Return:
After the analysis is completed, the script prints a friendly representation of the
returned  dictionary with the following values:

* **Number Of Villains**: Number of Players playing against the Hero
* **Flop**: Current The Cards in the Flop (Table)

if player is playing current hand:

* **Pocket Cards**: The Cards that the Hero is holding
* **Position**: Current Hero Position in the table
* **Equity**: The Equity (% of success with current hand)

If there is a decision to be made by the player:

* **Command**: The button to be pressed
* **Decision**: The decision made by the current bot strategy

Obs:

* **Hero** is the term used for the current player
* The python classes to be used for scanning the table and generating the strategy
 are defined in the settings.py file


#### hud

This task starts the PokerBot as a HUD (Head Up Display), so it will open the poker client,
start capturing the images, and parsing the image for the current table information and
also will generate decisions, but it *wont* execute the decisions made (send clicks)

Usage:

    python PyPokerBot.py hud [SleepTimeSec]

Parameters:

* **SleepTimeSec**: The time to sleep before starting to capture screen images. The
time between screen captures is defined in the settings.py file.


Return:

* **None** (But writes to stdout the parse of the screen image capture)


#### play

This tasks stars the PokerBot in Playing mode, so it will capture the screens of the
poker client, parse the image, run the strategy and send the clicks to the poker client.

Usage:

    python PyPokerBot.py play

Parameters:

* **None**

Return:

* **None** (But writes to stdout the parse of the screen image capture)


## Implementation Details

Below, I just highlight some implementation details and remarks:

*All source code has been recently linted and refactored*  

### Server

The server is a very simple webserver using Flask framework, so it is no very scalable and does not uses any modern python technique like asynchronous request processing.

#### Poker Odds Calculation

The Odds calculator uses the MIT library and requires to be compiled from its C source: [pbots_calc](https://github.com/mitpokerbots/pbots_calc), the compilation is quite trivial but there are several other poker libraries required or the build. I have tested the build both on Ubuntu 16 and ArchLinux.

#### REST API

The Rest API is simply a single URL that receives a json on the format required by the Poker Odds Calculation C Library [pbots_calc](https://github.com/mitpokerbots/pbots_calc) and returns a JSON with a python tuple containing the response. 

### Client

The Client is the actual script running on a windows desktop and has a "task" architecture where in the CLI you specify the correct task to be performed by the tool, as we can see on the usage section above.  

#### Screenshot Grab

The Poker Bot script detects the poker tables by its HWND and classname and instantiate a PokerTable class. Such class executes screen shots of the table, saving it for analysis. It is important that the table is placed on a certain location and with a certain size for the analysis to be performed as the regions of the image to be analyzed are in general hard coded.

#### Image Analisys

The image analysis code: *PokerTableScanner* class and its specializations uses OpenCV2 to do a histogram comparison between a certain region of the image and a template, for example if we are trying to detect with card the player has, we will compare the region of the image where the card should be with all the histograms from known cards, the best result will be the selected (detected) card. 

In order to detect the text of the message, we use a command line tool called tesseract that tries to detect the text from the image and returns it as a string.

#### Decision Making

The decision making is a very simple decision tree taking into account the hand equity, our position on the table and the current hand phase, as we can see on the example code below:

        if self.position_button(analisys):
            if hand_equity > 0.77:
                ret = ('RAISE OR CALL', 20)
            if hand_equity > 0.72:
                ret = ('RAISE OR CALL', 10)
            if hand_equity > 0.60:
                ret = ('RAISE OR CALL', 5)
        if self.position_out_position(analisys):
            if hand_equity > 0.77:
                ret = ('RAISE OR CALL', 20)
            if hand_equity > 0.72:
                ret = ('RAISE OR CALL', 5)
        if self.position_bb_check(analisys):
            if hand_equity > 0.77:
                ret = ('RAISE OR CALL', 20)
            if hand_equity > 0.72:
                ret = ('RAISE OR CALL', 20)
            if hand_equity > 0.60:
                ret = ('RAISE OR CALL', 5)
        return ret


## Current Status and Improvements

This is a first attempt to implement a completely functional poker playing bot, but at this moment, it has the following improvement points:

* **AI**: Implement real AI techniques and not simple decision trees.
* **Additional Platforms**: Currently the pot only support Pokerstars, but it can easily be added support for PartyPoker, 888Poker and other platforms.
* **Stealth**: Currently poker platforms have several algorithms that detect if the player is human or a bot, currently there is no implementation to mimic regular human player behavior and it is very easy to detect that it is a automated bot playing due to several reasons like: Python script running, always clicking on the same screen coordenatess and many other playing characteristics.

