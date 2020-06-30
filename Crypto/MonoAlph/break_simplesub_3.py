#from pycipher import SimpleSubstitution as SimpleSub
from CryptanalysisV02 import Cryptanalyse as Crypto
from CryptanalysisV02 import ngram_score
import random
import re

class Mono_break:
    def __init__(self, ciphertext):
        print("Starting...")
        self.fitness = ngram_score('english_quadgrams.txt') # load our quadgram statistics
        self.ciphertext = ciphertext
        self.ctext = re.sub('[^A-Z]','',self.ciphertext.upper())
        
        self.maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.maxscore = -99e9
        self.parentscore,self.parentkey = self.maxscore,self.maxkey[:]
        print ("Substitution Cipher solver, you may have to wait several iterations")
        print ("for the correct result. Press ctrl+c to exit program.")
        self.stopped = False
        self.do_break()

    def do_break(self):
        # keep going until we are killed by the user
        i = 0
        while not self.stopped:
            i = i+1
            random.shuffle(self.parentkey)
            deciphered = Crypto(self.ctext, self.parentkey).decipher()
            self.parentscore = self.fitness.score(deciphered)
            count = 0
            while count < 1000 and not self.stopped:
                a = random.randint(0,25)
                b = random.randint(0,25)
                child = self.parentkey[:]
                # swap two characters in the child
                child[a],child[b] = child[b],child[a]
                #deciphered = SimpleSub(child).decipher(self.ctext)
                deciphered = Crypto(self.ctext, child).decipher()
                score = self.fitness.score(deciphered)
                # if the child was better, replace the parent with it
                if score > self.parentscore:
                    self.parentscore = score
                    self.parentkey = child[:]
                    count = 0
                count = count+1
            # keep track of best score seen so far
            if self.parentscore>self.maxscore:
                self.maxscore,self.maxkey = self.parentscore,self.parentkey[:]
                print ('\nbest score so far:',self.maxscore,'on iteration',i)
                plaintext = Crypto(self.ciphertext, self.maxkey).decipher()
                self.bestkey = ''.join(self.maxkey)
                print ('    best key: '+ self.bestkey)
                print('    plaintext: ' + plaintext)
                if self.maxscore > -6000:
                    self.stopped = True


def main():
    ctext = 'S ilqa, nhramy, ytmm wpxysoaxwa jilj sy lmm op jiasc otjh, sy xpjisxu sr xaumawjao, lxo sy jia farj lcclxuanaxjr lca nloa, lr jiah lca fasxu nloa, ea rilmm bcpqa ptcramqar pxwa lulsx lfma jp oayaxo ptc Srmlxo ipna, jp csoa ptj jia rjpcn py elc, lxo jp ptjmsqa jia naxlwa py jhclxxh, sy xawarrlch ypc halcr, sy xawarrlch lmpxa. Lj lxh clja, jilj sr eilj ea lca upsxu jp jch jp op. Jilj sr jia carpmqa py Isr Nlvarjh’r Upqacxnaxj-aqach nlx py jian. Jilj sr jia esmm py Blcmslnaxj lxo jia xljspx. Jia Fcsjsri Anbsca lxo jia Ycaxwi Cabtfmsw, msxkao jpuajiac sx jiasc wltra lxo sx jiasc xaao, esmm oayaxo jp jia oalji jiasc xljsqa rpsm, lsosxu alwi pjiac mska uppo wpncloar jp jia tjnprj py jiasc rjcaxuji. Aqax jiptui mlcua jclwjr py Atcpba lxo nlxh pmo lxo ylnptr Rjljar ilqa ylmmax pc nlh ylmm sxjp jia ucsb py jia Uarjlbp lxo lmm jia posptr lbblcljtr py Xlzs ctma, ea rilmm xpj ymlu pc ylsm. Ea rilmm up px jp jia axo, ea rilmm ysuij sx Yclxwa, ea rilmm ysuij px jia ralr lxo pwalxr, ea rilmm ysuij esji ucpesxu wpxysoaxwa lxo ucpesxu rjcaxuji sx jia lsc, ea rilmm oayaxo ptc Srmlxo, eiljaqac jia wprj nlh fa, ea rilmm ysuij px jia falwiar, ea rilmm ysuij px jia mlxosxu ucptxor, ea rilmm ysuij sx jia ysamor lxo sx jia rjcaajr, ea rilmm ysuij sx jia ismmr; ea rilmm xaqac rtccaxoac, lxo aqax sy, eiswi S op xpj ypc l npnaxj famsaqa, jisr Srmlxo pc l mlcua blcj py sj eaca rtfvtuljao lxo rjlcqsxu, jiax ptc Anbsca fahpxo jia ralr, lcnao lxo utlcoao fh jia Fcsjsri Ymaaj, eptmo wlcch px jia rjctuuma, txjsm, sx Upo’r uppo jsna, jia Xae Epcmo, esji lmm sjr bpeac lxo nsuij, rjabr ypcji jp jia carwta lxo jia msfacljspx py jia pmo.'
    Mono_break(ctext)

if __name__ == "__main__":
    main()