#from pycipher import SimpleSubstitution as SimpleSub
from CryptanalysisV02 import Cryptanalyse as Crypto
from CryptanalysisV02 import ngram_score
import random
import re

print("Starting...")
fitness = ngram_score('english_quadgrams.txt') # load our quadgram statistics

ctext='pmpafxaikkitprdsikcplifhwceigixkirradfeirdgkipgigudkcekiigpwrpucikceiginasikwduearrxiiqepcceindgmieinpwdfprduppcedoikiqiasafmfddfipfgmdafmfdteiki'
ctext='ftj sy ea ylsm, jiax jia eipma epcmo, sxwmtosxu jia txsjao rjljar, sxwmtosxu lmm jilj ea ilqa kxpex lxo wlcao ypc, esmm rsxk sxjp jia lfhrr py l xae olck lua nloa npca rsxsrjac, lxo bacilbr npca bcpjclwjao, fh jia msuijr py bacqacjao rwsaxwa. maj tr jiacaypca fclwa ptcramqar jp ptc otjsar, lxo rp falc ptcramqar, jilj sy jia fcsjsri anbsca lxo sjr wpnnpxealmji mlrj ypc l jiptrlxo halcr, nax esmm rjsmm rlh, "jisr elr jiasc ysxarj iptc."'
ciphertext='S ilqa, nhramy, ytmm wpxysoaxwa jilj sy lmm op jiasc otjh, sy xpjisxu sr xaumawjao, lxo sy jia farj lcclxuanaxjr lca nloa, lr jiah lca fasxu nloa, ea rilmm bcpqa ptcramqar pxwa lulsx lfma jp oayaxo ptc Srmlxo ipna, jp csoa ptj jia rjpcn py elc, lxo jp ptjmsqa jia naxlwa py jhclxxh, sy xawarrlch ypc halcr, sy xawarrlch lmpxa. Lj lxh clja, jilj sr eilj ea lca upsxu jp jch jp op. Jilj sr jia carpmqa py Isr Nlvarjh’r Upqacxnaxj-aqach nlx py jian. Jilj sr jia esmm py Blcmslnaxj lxo jia xljspx. Jia Fcsjsri Anbsca lxo jia Ycaxwi Cabtfmsw, msxkao jpuajiac sx jiasc wltra lxo sx jiasc xaao, esmm oayaxo jp jia oalji jiasc xljsqa rpsm, lsosxu alwi pjiac mska uppo wpncloar jp jia tjnprj py jiasc rjcaxuji. Aqax jiptui mlcua jclwjr py Atcpba lxo nlxh pmo lxo ylnptr Rjljar ilqa ylmmax pc nlh ylmm sxjp jia ucsb py jia Uarjlbp lxo lmm jia posptr lbblcljtr py Xlzs ctma, ea rilmm xpj ymlu pc ylsm. Ea rilmm up px jp jia axo, ea rilmm ysuij sx Yclxwa, ea rilmm ysuij px jia ralr lxo pwalxr, ea rilmm ysuij esji ucpesxu wpxysoaxwa lxo ucpesxu rjcaxuji sx jia lsc, ea rilmm oayaxo ptc Srmlxo, eiljaqac jia wprj nlh fa, ea rilmm ysuij px jia falwiar, ea rilmm ysuij px jia mlxosxu ucptxor, ea rilmm ysuij sx jia ysamor lxo sx jia rjcaajr, ea rilmm ysuij sx jia ismmr; ea rilmm xaqac rtccaxoac, lxo aqax sy, eiswi S op xpj ypc l npnaxj famsaqa, jisr Srmlxo pc l mlcua blcj py sj eaca rtfvtuljao lxo rjlcqsxu, jiax ptc Anbsca fahpxo jia ralr, lcnao lxo utlcoao fh jia Fcsjsri Ymaaj, eptmo wlcch px jia rjctuuma, txjsm, sx Upo’r uppo jsna, jia Xae Epcmo, esji lmm sjr bpeac lxo nsuij, rjabr ypcji jp jia carwta lxo jia msfacljspx py jia pmo.'
ctext = re.sub('[^A-Z]','',ciphertext.upper())

maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -99e9
parentscore,parentkey = maxscore,maxkey[:]
print ("Substitution Cipher solver, you may have to wait several iterations")
print ("for the correct result. Press ctrl+c to exit program.")
# keep going until we are killed by the user
i = 0
while 1:
    i = i+1
    random.shuffle(parentkey)
    #deciphered = SimpleSub(parentkey).decipher(ctext)
    deciphered = Crypto(ctext, parentkey).decipher()
    parentscore = fitness.score(deciphered)
    count = 0
    while count < 1000:
        a = random.randint(0,25)
        b = random.randint(0,25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        #deciphered = SimpleSub(child).decipher(ctext)
        deciphered = Crypto(ctext, child).decipher()
        score = fitness.score(deciphered)
        # if the child was better, replace the parent with it
        if score > parentscore:
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count+1
    # keep track of best score seen so far
    if parentscore>maxscore:
        maxscore,maxkey = parentscore,parentkey[:]
        print ('\nbest score so far:',maxscore,'on iteration',i)
        #ss = SimpleSub(maxkey)
        plaintext = Crypto(ciphertext, maxkey).decipher()
        print ('    best key: '+''.join(maxkey))
        #print ('    plaintext: '+ss.decipher(ctext))
        print('    plaintext: ' + plaintext)


