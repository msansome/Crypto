# MonoAlph
By Mark Sansome - July 2020

## Monoalphabetic Substitution Ciphers

The main file in this section is the MonoGUI.py application. This is a Pyhon based graphical tool dedicated purely to the decryption (and occasional encryption) of Monoalphabetic substition ciphers - sometimes called "simple substitution ciphers". This will not help with any other form of cipher. A good place to start would be with the "index of coincidence" (see below). If this dopes not indicate that the ciphertext is a substitution cipher then this is not the tool for the job. If it is - read on...

## Dependencies
The MonoGUI app relies on some imported libraries and modules. These are:<br>

### Modules:
* Cryptanalysis.py (V.2.0) (Should be included with this).
* break_simplesub.py (v.3.0) (Should be included with this).
* makeWordPatterns.py and wordPatterns.py (should also be included).

### Dictionaries:

The following dictionaries should be included (although only quadgrams is actually required - others could be used if desired):
* english_monograms.txt
* english_bigrams.txt
* english_trigrams.txt
* english_gradgrams.txt

### Libraries:

The following libraries (all from the standard Python libraries) are required:

* tkinter, os, random, threading, re, copy.

The following external library needs to be installed:
* Matplotlib (Note: this displays a graphical representatiopn of the Frequency Analysis tool. If Matplotlib is not installed you will get a warning and no charts will be displayed, but the figures will still be displayed.)
To install Matplotlib do "pip [or pip3] install matplotlib" (or ask your system administrator.


### Sample Texts:

Three sample ciphertext texts - encrypted with a monoalphabetic substitution cipher are included in order to experiment with:
* Test1Mono.txt, Test2Mono.txt and Test3Mono.txt

# Usage:
## Overview
There are essentially three panes. The top pane is the input section where you type, paste or open a file containing the ciphertext you wish to analyse. The bottom pane is the output area where the plaintext will be displayed. The middle section contains the letter substitution mapping as well as a variety of anaylsis tools.

Having placed some cipertext into the input pane, unless you know already that it is encrypted with a substitution cipher, the first port of call would be the **Index of Coincidence** tool.
## Index of Coincidence
The Index of Coincidence (IC) is a measure of how similar a frequency distribution is to the
           uniform distribution (or how 'spiky' it is. The IC of a piece of text does not
           change if the text is enciphered with a substitution cipher. In other words,
           regular English will have an IC of around 0.066, and so will a piece of
           ciphertext enciphered with a substitution cipher. However, a polyalphabetic
           cipher (e.g. a Vigenere cipher) will have an IC of around 0.038.<br><br>
 Clicking on the Index of Coincidence button will calculate the index of your ciphertext and display it. If it is in the 0.03 - 0.04 range you are out of luck. This is not the tool for you. If it is around 0.066 then it is almost certainly encrypted with a substitution cipher. Go ahead and try dome of the other analsis tools.
 
 ## Pattern Decrypt
 This uses a pattern matching algorithm which compares the order of the letters in  the ciphertext words with similar length words in a dictionary.
 
 This is quite fast, but does not always produce complete results.
 
 Note also: ***This will only work on ciphertext where the spaces between words has been preserved.***   

## Auto Decrypt
This uses a sophisticate Hill-Climbing algorithm which will randomly change letter mappings, check the "score" against known english bigrams, trigrams or quadgrams (the default is english quadgrams) and will repeat this process attempting to improve the score.

This tool may take a long time to run (depending on the speed of your computer, length of the ciphertext etc.) may have to be run more than once, and may not produce an answer at all.

It will open a pop-up window. Once you click the "Start Decrypt" button, it will continue to run until you tell it to stop (by clicking the "Stop" button). It will periodically show you a sample of the best decrypt so far, but it will keep going until you tell it to stop. Once you hit the "Stop" button it will place the resulting decrypted text in the output field.
 
This tool - if it succeeds - generally produces a better result, and has the advantage that it does not need to have the spaces between letters preserved.

## Frequency Analysis
The most commonly occurring letter in English text is "e", followed by "t" and so on. If the encrypted text is English and the cipher is a monoalphabetic substitution cipher, then this relationship will be preserved in the ciphertext.

This tool will allow you to analyse the ciphertext and will show the frequency of the ciphertext letters compared to standard English.

Note: if you have the Matplotlib library installed this will also show the results in the form of a graph.

## Doubles Analysis
As with frequency analysis, the most commonly occurring double letter in English text is "ll", followed by "ee" and so on.

This tool will allow you to analyse the ciphertext and will show the frequency of the repeated (double) ciphertext letters compared to standard English.

Note: if you have the Matplotlib library installed this will also show the results in the form of a graph.
## The Alphabet
Armed with the information from the frequency alaysis tools (or to correct mistakes made by the pattern or auto decrypt tools) you can type letters into the alphabet. As you type each letter the decrypted output will be updated.

## Key Tools
Note: By "key" here I am referring to the letter mapping (i.e. which letter in the ciphertext maps to which letter in the plaintext alphabet).
 
If you know the key with which the cipertext was encrypted you can import it using the "Import Key" tool.
 
Once you have decrypted the ciphertext and worked out the key, you can record the key by using the "Copy Key to Clipboard" button. Once you have clicked on this the key will be in the clipboard buffer and can be pasted into your favourite text editor.

The "Random Key" will produce a random key (duh!). This is useful if you want to create a new ciphertext - just hit the "Encrypt / Decrypt" button and it will encrypt whatever is in your input section with that key.

The  "Invert Key" option will reverse the mapping of the key so that the key used to encrypt can nw be used to decrypt.

The "Reset Key" option will reset the key to all "*" if yo want to start again from scratch.

## Copy to Clipboard
This button will allow you to cop the plaintext. Once you click it, whatever is in the plaintext field will be in the clipboard buffer and can be pasted into your favourite text editor.


