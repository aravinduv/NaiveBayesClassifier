import os,math,sys
from collections import Counter

class NBLearn(object):
    def __init__(self):
        self.exten = '.txt'
        self.hamfiles = []
        self.spamfiles = []
        self.pspam_dict = dict()
        self.pham_dict = dict()

        self.ham_tokens = []
        self.spam_tokens = []
        self.master_list = []
        self.priorProb_spam = ""
        self.priorProb_ham = ""
        self.unique_words = ""
        self.hamCount = 0
        self.spamCount = 0

        self.fstr = ""

    def populateLists(self,path):
        for root, dirs, files in os.walk(path):
            for fname in files:
                if fname.endswith(".txt"):
                    fullPath = os.path.dirname(os.path.abspath(os.path.join(root, fname)))
                    if "spam" in fullPath:
                        self.spamfiles.append(os.path.abspath(os.path.join(root, fname)))

        for root, dirs, files in os.walk(path):
            for fname in files:
                if fname.endswith(".txt"):
                    fullPath = os.path.dirname(os.path.abspath(os.path.join(root, fname)))
                    if "ham" in fullPath:
                        self.hamfiles.append(os.path.abspath(os.path.join(root, fname)))

    def tokenize(self,text):
            tokens = text.strip().split(' ')
            return tokens

    def loadFeatures(self):
        for f in self.hamfiles:
            h1 = open(f, "r", encoding="latin1")
            while True:
                strline = h1.readline()
                if not strline:
                    break
                self.ham_tokens.extend(self.tokenize(strline))
            h1.close()

        for f in self.spamfiles:
            h2 = open(f, "r", encoding="latin1")
            while True:
                strline = h2.readline()
                if not strline:
                    break
                self.spam_tokens.extend(self.tokenize(strline))
            h2.close()

    def calculatePriorProb(self):
        #first get the count of each class
        hamCount = len(self.hamfiles)
        spamCount = len(self.spamfiles)
        total = hamCount+spamCount

        #P(Spam) or P(Ham)
        self.priorProb_spam = "{:.9f}".format(spamCount/total)
        self.priorProb_ham = "{:.9f}".format(hamCount/total)

    def computeVocabularySize(self):
        self.master_list.extend(self.ham_tokens)
        self.master_list.extend(self.spam_tokens)

        self.unique_words = set(self.master_list)
        return len(self.unique_words)

    def calculateMsgGivenSpam(self):
        return ''.join('%s #@# %s@###@' % (k, v) for k, v in self.pspam_dict.items())

    def calculateMsgGivenHam(self):
        return ''.join('%s #@# %s@###@' % (k, v) for k, v in self.pham_dict.items())

    def addOneSmoothing(self,vcount):
        #First calculate the counts
        counts_spam_dict = Counter(self.spam_tokens)
        counts_ham_dict = Counter(self.ham_tokens)

        for word in self.unique_words:
            # Calculate P(w|Spam)
            self.pspam_dict[word] = "{:.9f}".format((counts_spam_dict[word] + 1)/(len(self.spam_tokens) + vcount))
            #Calculate P(w|Ham)
            self.pham_dict[word] = "{:.9f}".format((counts_ham_dict[word] + 1) / (len(self.ham_tokens) + vcount))

    def writeModelFile(self):
        fname = "nbmodel.txt"
        f = open(fname,"w",encoding="latin1")

        self.fstr += self.priorProb_spam + "," + self.priorProb_ham + "\n"
        self.fstr += "*****@separator@*****\n"
        self.fstr += self.calculateMsgGivenSpam()
        self.fstr += "*****@separator@*****\n"
        self.fstr += self.calculateMsgGivenHam()

        f.write(self.fstr)
        f.close()

def main():
    nb = NBLearn()
    nb.populateLists(sys.argv[1])
    nb.loadFeatures()
    nb.calculatePriorProb()
    vocabCount = nb.computeVocabularySize()
    nb.addOneSmoothing(vocabCount)
    nb.writeModelFile()

if __name__ == "__main__":
    main()