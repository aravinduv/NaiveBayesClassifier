import sys,os
import math

class NBClassify(object):
    def __init__(self):
        self.exten = '.txt'
        self.filelist = []
        #self.token_list = []
        self.sdict = dict()
        self.hdict = dict()
        self.pspam = 0.0
        self.pham = 0.0

        self.posteriorSpam = 0.0
        self.posteriorHam = 0.0

        self.isSpam = False
        self.hamfiles = []
        self.spamfiles = []

        self.hamCount = 0
        self.spamCount = 0
        self.correctSpam = 0
        self.correctHam = 0

        self.countSpamFiles = 0
        self.countHamFiles = 0

        self.predict = dict()
        self.recalldict = dict()
        self.fscoredict = dict()

        self.strToWrite = ""
        self.str1 = ""
        self.str2 = ""

    def getAllFiles(self,path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith(".txt"):
                    self.filelist.append(os.path.abspath(os.path.join(root,f)))

    def tokenize(self, text):
        tokens = text.strip().split(' ')
        return tokens

    def loadFeatures(self,list1):
        for f in list1:
            token_list = []
            h = open(f, "r", encoding="latin1")
            while True:
                strline = h.readline()
                if not strline:
                    break
                token_list.extend(self.tokenize(strline))
            h.close()
            self.computePosteriorProb(token_list,f)

    def readModelParameters(self):
        with open("nbmodel.txt", 'r', encoding="latin1") as myfile:
            data = myfile.read().replace('\n', '')
        return data

    def processModelParams(self,mparams):
        plist = mparams.split("*****@separator@*****",2)
        self.pspam = float(plist[0].split(",")[0])
        self.pham = float(plist[0].split(",")[1])

        tempList1 = plist[1].split("@###@")
        for s in tempList1:
            if (s.split(" #@# ")[-1] != ""):
                self.sdict[s.split(" #@# ")[0]] = float(s.split(" #@# ")[1])

        tempList2 = plist[2].split("@###@")
        for s in tempList2:
            if(s.split(" #@# ")[-1] != ""):
                self.hdict[s.split(" #@# ")[0]] = float(s.split(" #@# ")[1])

    def writeOutputFile(self, strToWrite):
        h = open("nboutput.txt", "w")
        h.write(strToWrite)
        h.close()

    def computePosteriorProb(self,tokenlist,fname):
        probGivenSpam = 0.0
        probGivenHam = 0.0
        for word in tokenlist:
            #First compute P(w|Spam)
            if word in self.sdict:
                probGivenSpam += math.log10(self.sdict[word])

        #First compute P(w|Ham)
        for word in tokenlist:
            if word in self.hdict:
                probGivenHam += math.log10(self.hdict[word])

        #Compute posterior
        self.posteriorSpam = math.log10(self.pspam) + probGivenSpam
        self.posteriorHam = math.log10(self.pham) + probGivenHam

        if(self.posteriorSpam > self.posteriorHam):
            self.isSpam = True
            self.strToWrite += "spam" + " " + fname + "\n"
        else:
            self.isSpam = False
            self.strToWrite += "ham" + " " + fname + "\n"

def main():
    nb = NBClassify()

    nb.getAllFiles(sys.argv[1])
    mparams = nb.readModelParameters()
    nb.processModelParams(mparams)
    nb.loadFeatures(nb.filelist)

    nb.writeOutputFile(nb.strToWrite)

if __name__ == "__main__":
    main()
