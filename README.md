# blogabetAnalyzer

This is a simple tool to help you analyze blogabet.com tipsters picks and stats in order to design a better betting
strategy.

###	Setup
To get it working, open a terminal if you are in Linux/Mac or PowerShell if you are on Windows. Firstly, you need to clone the repository at your local host (you need to have git installed on your system):
```console
>>> git clone  https://github.com/espinosa012/blogabetAnalyzer.git
```
Although it is not strictly necessary, you may want to set a python virtual environment.
```console
>>> virtualenv venv
```
To activate it, if you are in a Linux/Mac terminal:
```console
>>> source venv/bin/activate
```
If you are in PowerShell:
```console
>>> venv/Scripts/activate
```
Now, you need to install requirements:
```console
>>> pip install -r requirements.txt
```
**Note**: You also need Google Chrome on your system

### How does this work?
The program entrypoint is the file 'main.py'.

New version uses an undetectable implementation of chromedriver. You can find it here: https://github.com/ultrafunkamsterdam/undetected-chromedriver

Once you execute main script, you will be asked to type the name of the tipster you want to get stats for. Type it, wait a few
seconds, and you will get a dictionary with tipster's stats.
**Note**: The tipster's name you have to type is the one that appears in his blogabet blog's url. For example, if you want
to get information about the tipster TaIvo, whose blog's url is https://taivotipster.blogabet.com/, the name you need is 
*taivotipster*.

Please, have in consideration that this is an unfinished project. More features will be added soon.
Any comments or suggestions are welcome.

Of course, you are free to make any change in 'main.py' script to get what you need.


