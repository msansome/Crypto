# Crypto

Mark Sansome June 2020
##Some cryptographic tools

These files contain several cryptographic tools - most of which I have developed myself, and some of which are modified versions of the (Python2) tools to be found in http://practicalcryptography.com or adapted versions of the programs found in Al Sweigart's book "Cracking Codes with Python".

###The Sections
There are currently four sections. These are:
* Caesar
* Monoalph
* Ployalph; and 
* CryptoBook

##Caesar
This contains a text-based tool for decrypting Caesar ciphers (CaesarText.py) and a graphical version (CaesarGUI.py) which does the same thing but in a GUI. In addition, there is a text file (caesartext.txt) containing a message encrypted with a Caesar Cipher in order to test the tool. There is also a simple program (CaesarGUIenc.py) to create (and decrypt) Caesar ciphers.

See the README file in the Caesar directory for more information.

##MonoAlph
This is a tool dedicated to breaking Monoalphabetic Substitution Ciphers (Sometimes called Simple Substitution Ciphers).

The main program here is MonoGUI.py.

The rest of the files are modules (or dictionaries required by the progrram). 

There are also three test files to try it out with (Test1Mono.txt -> Test3Mono.txt)

See the README file in the MonoAlph directory for more information.

##PolyAlph
This is a tool dedicated to breaking Ployalphabetic Substitution Ciphers (Such as the Vigenere Cipher).

This is currently under development
##CryptoBook
The files from Al Swigart's book "Cracking Codes with Python"



