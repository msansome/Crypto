# M Sansome
# May 2019


class Cryptanalise:
    '''This Class provides several crypanalysis tools.
    Useage (eg): mystuff = Cryptanalise(myciphertext)
                letter_frequencies = mystuff.freq()
                print(mystuff.print_freqs()
    '''

    def __init__(self, ciphertext, alphabet=""):
        self.text = ciphertext
        self.counts = {}
        self.freqs = {}
        self.doubles = {}
        if alphabet == "":
            self.alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        else:
            self.alph = alphabet
        # Default English letter frequencies (from Wikipdia). Can be replaced with
        # user's own frequencis
        self.std_Eng_freqs={'E': 12.02, 'T': 9.1, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61, 'F': 2.3, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.1, 'Z': 0.07}
        

    def count_letters(self):
        ''' This method returns a dictionary populated with a count of all the
            occurrences of each character in the ciphertext.This method will work
            through a string (or list) and calculate the frequency of the occurrence
            of alphabetic characters in the string.
            It will store these in a dictionary which will then be used to calculate
            the relative percentage of each letter.By default it counts
            A-Z characters only, but you can supply your own list of characters to
            check against by passing in a string as the 'alphabet' argument
            in the constructor.''' 
        
        for ch in self.text:
            ch = ch.upper()
            if ch in self.alph:
                # we only want to count A-Z letters (ignore other characters).
                if ch in self.counts:
                    self.counts[ch]+= 1
                    # If we've seen this letter before, increment its frequency count.
                else:
                    # if we haven't seen this letter before, add it to the dictionary. 
                    self.counts[ch] = 1
        total = sum(self.counts.values())
        return self.counts

    def frequencies(self):
        ''' This method will take the count of the characters produced by 'count_letters'
            and calculate the percentage frequency.
            It will return the frequencies in a dictionary'''
        
        if len(self.counts) == 0: # If letter_count hasn't been run, run it!
            self.count_letters()
        total = sum(self.counts.values())
        for key, value in self.counts.items():
            self.freqs[key] = value / total * 100

        return self.freqs

    
    def print_freqs(self, std_freqs=""):
        ''' This will print out the letter frequency table and ciphertext frequency
            table side by side.
            User can (optionally) suuply own frequencies via the 'std_freqs' param.
            '''
        if std_freqs == "":
            std_freqs = self.std_Eng_freqs
        if len(self.freqs) == 0:
            self.frequencies()
            
        cipher_freqs = sorted(self.freqs, key=self.freqs.get, reverse=True)
        letter_freqs = sorted(std_freqs, key=std_freqs.get, reverse=True)

        print("English Frequency\tCipher Frequency")
        print("=================\t================")
    
        for i in range(0, len(cipher_freqs)):
            print(f' {letter_freqs[i]}\t{std_freqs[letter_freqs[i]]:9.2f} \t {cipher_freqs[i]}\t{self.freqs[cipher_freqs[i]]:9.2f}')
        for i in range(len(cipher_freqs),len(letter_freqs)):
            print(f' {letter_freqs[i]}\t{std_freqs[letter_freqs[i]]:9.2f}')
        return

    def count_doubles(self):
        for i in range (0, len(self.text)-1):
            if self.text[i] in self.alph and self.text[i+1] in self.alph and self.text[i] == self.text[i+1]:
                if self.text[i] in self.doubles:
                    self.doubles[self.text[i]] += 1
                else:
                    self.doubles[self.text[i]] = 1
        return self.doubles

    def print_doubles(self):
        if len(self.doubles)==0:
            self.count_doubles()
        print()
        print("Double Letters")
        print("==============")
        for key,value in self.doubles.items():
            print(f' {key}\t{value}')

    def ic(self):
        '''This method will return the 'Index of Coincidence' (IC).
           This is a measure of how similar a frequency distribution is to the
           uniform distribution (or how 'spiky' it is. The I.C. of a piece of text does not
           change if the text is enciphered with a substitution cipher. In other words,
           regular English will have an IC of around 0.066, and so will a piece of
           ciphertext enenciphered with a substitution cipher. Hovever, a polyalphabetic
           cipher (e.g. a Vigenere cipher) will have an IC of around 0.038.
           See : http://practicalcryptography.com/cryptanalysis/text-characterisation/index-coincidence/'''
        
        if len(self.counts) == 0: # Run the frequency counts
            self.count_letters()
        N = sum(self.counts.values())
        total = 0
        for key, value in self.counts.items():
            subtotal = value * (value - 1)
            total += subtotal
        ic = total / (N * (N-1))
        return ic


class ngram_score:
    def __init__(self,ngramfile,sep=' '):
        from math import log10
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        with open(ngramfile) as f:
            for line in f:
                key,count = line.split(sep) 
                self.ngrams[key] = int(count)
            #print(self.ngrams)
            self.L = len(key)
            self.N = sum(self.ngrams.values())
            
            #calculate log probabilities
            for key in self.ngrams.keys():
                self.ngrams[key] = log10(self.ngrams[key]/self.N)
            self.floor = log10(0.01/self.N)

    def score(self,text):
        ''' compute the score of text '''
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1): 
            if text[i:i+self.L] in self.ngrams:
                score += ngrams(text[i:i+self.L])
            else: score += self.floor          
        return score

testcount = Cryptanalise("The cat sat on the mat")
#dic = testcount.count_letters()
#print(dic)
#print (testcount.print_freqs(dic))
#frqs = testcount.frequencies()
#testcount.print_freqs()

##letter_freqL=['e','t','a','o','i','n','s','r','h','d','l','u','c','m','f','y','w','g','p','b','v','k','x','q','j','z']
##letter_freqP=[12.2,9.10,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88,2.71,2.61,2.30,2.11,2.09,2.03,1.82,1.49,1.11,0.69,0.17,0.11,0.10,0.07]
##
##newfreqs={}
##for i in range(0,len(letter_freqL)):
##    L = letter_freqL[i].upper()
##    newfreqs[L] = letter_freqP[i]
###print(newfreqs)
#print(sum(newfreqs.values()))
#testcount.print_freqs(newfreqs)
#frqs = testcount.frequencies()
#print(frqs)
    

