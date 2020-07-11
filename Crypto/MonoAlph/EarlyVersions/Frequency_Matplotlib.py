import matplotlib.pyplot as plt
from random import randint

def plot_freqs(ciphertext):
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    letter_counts = [ciphertext.count(l) for l in alphabet]
    letter_colours = plt.cm.hsv([0.8*i/max(letter_counts) for i in letter_counts])

    plt.bar(range(26), letter_counts, color=letter_colours)
    plt.xticks(range(26), alphabet) # letter labels on x-axis
    plt.tick_params(axis="x", bottom=False) # no ticks, only labels on x-axis
    plt.title("Frequency of each letter")
    plt.savefig("output.png")
    print("Done")
    plt.show()

def randText():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    txt = ""
    for n in range(15000):
        txt += alphabet[randint(0,25)]
    return txt
    

ciphertext1 = """
yfdpcpoplhhwdpssbjnsqvtlcpzpxqugtjphvgotuvwxufgoqigxwgkskduooyeuoue
fjlnmsqpgxrmcseeliswdheywseqgcbeothskxdzekgxmmkildjnaqbukprpfaaknsu
qpdwayqaqfxsoapvsgreqydqjnkpjghvrkygtidzibhrqkmocukhcunpjcazzvomtsc
fgycwfltmiegaejwcqrgsnxxcbtcrckufwsdxdhbxgppxcuzapbdhftzmugryfseavv
bssqlxanvmfwwzityziixasivzkmvtfczqmdgkabcnjbyhaoealengfptuedlmvryeb
titbwqkekzdpmbtiphdkwwiduassvbgalxgrfhrjrjplxpujrprqzcpcdqsjorigazt
kwwlnwbjryrzhgcttroyemuwwixwufymnknirzmexyowobvardlqktzajzoijwulomg
ztefdpftjealzapcgipgaaspuzxklvd"""

ciphertext2 = """
swodkdbkfovvobpbywkxkxdsaeovkxngrycksndgyfkcdkxndbexuvoccvoqcypcdyx
ocdkxnsxdronocobdxokbdrowyxdrockxnrkvpcexukcrkddobonfsckqovsocgrycop
bygxkxngbsxuvonvszkxncxoobypmyvnmywwkxndovvdrkdsdccmevzdybgovvdrycoz
kccsyxcbokngrsmriodcebfsfocdkwzonyxdrocovspovoccdrsxqcdrorkxndrkdwym
uondrowkxndrorokbddrkdponkxnyxdrozonocdkvdrocogybnckzzokbwixkwoscyji
wkxnskcusxqypusxqcvyyuyxwigybuciowsqrdikxnnoczksbxydrsxqlocsnobowksx
cbyexndronomkiypdrkdmyvycckvgbomulyexnvocckxnlkbodrovyxokxnvofovckxn
ccdbodmrpkbkgki"""

txt2 = randText()
#plot_freqs(txt2)
plot_freqs(ciphertext1)


