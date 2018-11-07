@echo off 
color 03
echo hello
cd C:\Users\PC\PycharmProjects\lab1\Release
set "list=1 2 3 4 5 6 7 8 9 10 20 25 30 35 40 45 50 55 60 70 80 90 100 110 200 300 400 500"
for %%a in (%list%) do ( 
    echo %%a 
    start /wait lab1.exe -n 500 -r %%a -f 1
    start /wait lab1.exe -n 500 -r %%a -f 2
    start /wait lab1.exe -n 500 -r %%a -f 4
)
pause


