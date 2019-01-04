@echo on
echo Starting virtualenv
call ..\env\Scripts\activate.bat
cd src
echo Starting Table Analisys
echo 1st Table Analisys
echo ------------------
python PyPokerBot.py analyse_table "..\images\Screenshot.20170822112012.190000.Salm.Table.jpg" POKERSTARS 6-SEATS
echo 2nd Table Analisys"
echo ------------------
python PyPokerBot.py analyse_table "..\images\Screenshot.20170822112607.667000.Tiflis II.Table.jpg" POKERSTARS 6-SEATS
echo 3rd Table Analisys
echo ------------------
python PyPokerBot.py analyse_table "\git\PyPokerBotLogs\image\20170323\Screenshot.20170323111434.247000.Menelaus.Table.jpg" POKERSTARS 6-SEATS
echo 4th Table Analisys
echo ------------------
python PyPokerBot.py analyse_table "\git\PyPokerBotLogs\image\20170323\Screenshot.20170323111501.100000.Menelaus.Table.jpg" POKERSTARS 6-SEATS

