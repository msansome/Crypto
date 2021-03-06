# M Sansome
# May 2019
# Version 0.2 Modified in June 2020
# Added Decipher function


class Cryptanalyse:
    '''This Class provides several crypanalysis tools.
    Useage (eg): mystuff = Cryptanalyse(myciphertext)
                letter_frequencies = mystuff.freq()
                print(mystuff.print_freqs()
    '''

    def __init__(self, ciphertext, key="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        self.ctext = ciphertext
        self.counts = {}
        self.freqs = {}
        self.doubles = {}
        self.key = key
        # Default English letter frequencies (from Wikipdia). Can be replaced with
        # user's own frequencis
        #self.std_Eng_freqs={'E': 12.02, 'T': 9.1, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95, 'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88, 'C': 2.71, 'M': 2.61, 'F': 2.3, 'Y': 2.11, 'W': 2.09, 'G': 2.03, 'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11, 'J': 0.1, 'Z': 0.07}
        self.std_Eng_freqs = {'A': 8.497, 'B': 1.492, 'C': 2.202, 'D': 4.253, 'E': 11.162, 'F': 2.228, 'G': 2.015, 'H': 6.094,
                 'I': 7.546, 'J': 0.153, 'K': 1.292, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929,
                 'Q': 0.095, 'R': 7.587, 'S': 6.327, 'T': 9.356, 'U': 2.758, 'V': 0.978, 'W': 2.56, 'X': 0.15,
                 'Y': 1.994, 'Z': 0.077}
        self.std_Eng_doubles =['LL','EE','SS','OO','TT','FF','RR','NN','PP','CC']

        self.make_dictionary_from_key()

    def make_dictionary_from_key(self):
        self.plaintext_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.cipher2plain_dict = {}
        missing_letters = []
        missing_letter_count =0
        for letter in self.plaintext_alphabet:
            if letter not in self.key:
                missing_letters.append(letter)
        for i in range(26):
            if self.key[i] not in self.plaintext_alphabet:
                cletter = missing_letters[missing_letter_count]
                missing_letter_count += 1
                pletter = "*"
            else:
                cletter = self.key[i]
                pletter = self.plaintext_alphabet[i]
            self.cipher2plain_dict[cletter] = pletter
        return self.cipher2plain_dict


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
        
        for ch in self.ctext:
            ch = ch.upper()
            if ch in self.key:
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
        ctext_upper = self.ctext.upper()  # Convert all ciphertext to uppercase to match the alphabet
        for i in range (0, len(ctext_upper)-1):
            if ctext_upper[i].upper() in self.key and ctext_upper[i+1].upper() in self.key and ctext_upper[i] == ctext_upper[i+1]:
                if ctext_upper[i] in self.doubles:
                    self.doubles[ctext_upper[i]] += 1
                else:
                    self.doubles[ctext_upper[i]] = 1
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

    def decipher(self):
        self.plaintext = ""
        for j in range(len(self.ctext)):
            cLetter = self.ctext[j].upper()
            if cLetter in self.plaintext_alphabet:
                pLetter = self.cipher2plain_dict[cLetter]
                if self.ctext[j].islower():
                    pLetter =pLetter.lower()
                self.plaintext += pLetter
            else:
                self.plaintext += self.ctext[j]
        return self.plaintext
        

class ngram_score:
    def __init__(self,ngramfile,sep=' '):
        from math import log10
        ''' load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        with open(ngramfile) as f:
            for line in f:
                key,count = line.split(sep) 
                self.ngrams[key] = int(count)
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

def main():
    ctext = "abccdeeccf"
    test = Cryptanalyse(ctext)
    doubles = test.count_doubles()
    print_doubles = test.print_doubles()
    # newkey = "L*WOAY*IS**MNXPB*CRJTQ****"
    # test =Cryptanalyse()

    #test.make_dictionary_from_key(newkey)
    # ctext='S ilqa, nhramy, ytmm wpxysoaxwa jilj sy lmm op jiasc otjh, sy xpjisxu sr xaumawjao, lxo sy jia farj lcclxuanaxjr lca nloa, lr jiah lca fasxu nloa, ea rilmm bcpqa ptcramqar pxwa lulsx lfma jp oayaxo ptc Srmlxo ipna, jp csoa ptj jia rjpcn py elc, lxo jp ptjmsqa jia naxlwa py jhclxxh, sy xawarrlch ypc halcr, sy xawarrlch lmpxa. Lj lxh clja, jilj sr eilj ea lca upsxu jp jch jp op. Jilj sr jia carpmqa py Isr Nlvarjh’r Upqacxnaxj-aqach nlx py jian. Jilj sr jia esmm py Blcmslnaxj lxo jia xljspx. Jia Fcsjsri Anbsca lxo jia Ycaxwi Cabtfmsw, msxkao jpuajiac sx jiasc wltra lxo sx jiasc xaao, esmm oayaxo jp jia oalji jiasc xljsqa rpsm, lsosxu alwi pjiac mska uppo wpncloar jp jia tjnprj py jiasc rjcaxuji. Aqax jiptui mlcua jclwjr py Atcpba lxo nlxh pmo lxo ylnptr Rjljar ilqa ylmmax pc nlh ylmm sxjp jia ucsb py jia Uarjlbp lxo lmm jia posptr lbblcljtr py Xlzs ctma, ea rilmm xpj ymlu pc ylsm. Ea rilmm up px jp jia axo, ea rilmm ysuij sx Yclxwa, ea rilmm ysuij px jia ralr lxo pwalxr, ea rilmm ysuij esji ucpesxu wpxysoaxwa lxo ucpesxu rjcaxuji sx jia lsc, ea rilmm oayaxo ptc Srmlxo, eiljaqac jia wprj nlh fa, ea rilmm ysuij px jia falwiar, ea rilmm ysuij px jia mlxosxu ucptxor, ea rilmm ysuij sx jia ysamor lxo sx jia rjcaajr, ea rilmm ysuij sx jia ismmr; ea rilmm xaqac rtccaxoac, lxo aqax sy, eiswi S op xpj ypc l npnaxj famsaqa, jisr Srmlxo pc l mlcua blcj py sj eaca rtfvtuljao lxo rjlcqsxu, jiax ptc Anbsca fahpxo jia ralr, lcnao lxo utlcoao fh jia Fcsjsri Ymaaj, eptmo wlcch px jia rjctuuma, txjsm, sx Upo’r uppo jsna, jia Xae Epcmo, esji lmm sjr bpeac lxo nsuij, rjabr ypcji jp jia carwta lxo jia msfacljspx py jia pmo.'
    # key ='LFWOAYUISVKMNXPBDCRJTQEGHZ'
    # plaintext = Cryptanalyse(ctext,key).decipher()
    # print(plaintext)
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
    
if __name__ == "__main__":
    main()
