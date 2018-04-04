import math
import os.path
import sys


#---------------------------------------------------------------------------#
#	Language name parameters
#---------------------------------------------------------------------------#
keyword = "house" 
NumberOfRows = 25

if len(sys.argv) == 2:
	keyword = sys.argv[1]
 
print   keyword

shortfilename 		= "english-encarta"
outshortfilename 	= "english-encarta"
languagename 		= "english-encarta"

#shortfilename 		= "tomsawyer"
#outshortfilename 	= "tomsawyer"
#languagename 		= "english-tomsawyer"

#shortfilename 		= "browncorpus"
#outshortfilename 	= "browncorpus"
#languagename 		= "english"


#shortfilename 		= "french"
#outshortfilename 	= "french"
#languagename 		= "french"

#shortfilename 		= "dutch"
#outshortfilename 	= "dutch"
#languagename 		= "dutch"



if len(keyword)>0:
	outshortfilename = shortfilename + "_"  + keyword





#---------------------------------------------------------------------------#
#	File names
#---------------------------------------------------------------------------#

datafolder    		= "../../data/"

ngramfolder   		= datafolder + languagename + "/ngrams/"
outfolder     		= datafolder + languagename + "/mutualinformation/"
if not os.path.isdir(ngramfolder):
	os.makedirs(ngramfolder)
if not os.path.isdir(outfolder):
	os.makedirs(outfolder)



infileBigramsname 	= ngramfolder + shortfilename    + "_bigrams.txt" 
infileTrigramsname 	= ngramfolder + shortfilename    + "_trigrams.txt"
infileWordsname 	= ngramfolder   + shortfilename    + "_words.txt" 
outfilenameLatex 	= outfolder     + outshortfilename + "_latex.tex"
 
print "--------------------------------------------------------------"
print "I am looking for: ", infileBigramsname, " and \n\t\t   ", infileTrigramsname
print "I am printing to: ", outfilenameLatex
print "--------------------------------------------------------------" 


unicodeFlag = False

Words = dict()
WordList = list()
Bigrams = dict()
BigramList = list()
FollowingWord = dict()
PrecedingWord = dict()



#---------------------------------------------------------------------------#
#	Open files for reading and writing
#---------------------------------------------------------------------------#

if unicodeFlag:
	trigramfile 		=codecs.open(infileTrigramsname, encoding = FileEncoding)
	wordfile 		=codecs.open(infileWordsname, encoding = FileEncoding)
	if PrintEigenvectorsFlag:
		outfileEigenvectors = codecs.open (outfilename1, "w",encoding = FileEncoding)
	outfileNeighbors	= codecs.open (outfileneighborsname, "w",encoding = FileEncoding)

 
	
else:
	outfileLatex 		= open (outfilenameLatex, "w")

	wordfile		= open(infileWordsname)
	trigramfile 		= open(infileTrigramsname)
	bigramfile 		= open(infileBigramsname)

print "Language is", languagename, ". File name:", shortfilename




#---------------------------------------------------------------------------#
#	Read word file
#---------------------------------------------------------------------------#
totalwordcount = 0
for line in wordfile:
	pieces = line.split()
	if pieces[0] == "#":
		continue
	#print line
	Words[pieces[0]] = int(pieces[1])
	WordList.append(pieces[0])	
	totalwordcount += int(pieces[1])	 
print "1. Word file is ", infileWordsname, " \nWord count: ", totalwordcount		
wordfile.close()

wordlist = sorted(Words,key=Words.__getitem__,reverse=True)

worddict=dict()


for i in range(len(wordlist)):
	worddict[wordlist[i]] = i
 
#---------------------------------------------------------------------------#
#	Read bigram file
#---------------------------------------------------------------------------#

totalbigramcount = 0
if True: 
	print "...Reading in bigram file."
	for line in bigramfile:
		thesewords = line.split()
		if thesewords[0] == "#":
			continue
	  	firstword = thesewords[0]
		secondword= thesewords[1]
		count = int(thesewords[2])
		totalbigramcount += count
		bigram = firstword + " " + secondword
		Bigrams[bigram]=count
		BigramList.append(bigram)
	 	if firstword not in FollowingWord:
			FollowingWord[firstword] = dict()
		FollowingWord[firstword][secondword]= count
 	 	if secondword not in PrecedingWord:
			PrecedingWord[secondword] = dict()
		PrecedingWord[secondword][firstword]= count
 				






#---------------------------------------------------------------------------#
#	Generate latex output.
#---------------------------------------------------------------------------#
 
	#Latex output
print >>outfileLatex, "%",  infileWordsname
print >>outfileLatex, "\\documentclass{article}" 
print >>outfileLatex, "\\usepackage{booktabs}" 
print >>outfileLatex, "\\usepackage{geometry}"
print >>outfileLatex, "\\usepackage[group-separator={,}]{siunitx}" # to put commas in big numbers;
print >>outfileLatex, "\\usepackage{geometry}"
print >>outfileLatex, "\\geometry{lmargin=.5in,rmargin=.5in,tmargin=.55in,bmargin=.55in}"
print >>outfileLatex, "\\begin{document}" 



data = list()  
print ( "  Printing contexts to latex file.")
formatstr = '%20s   %15s %10.3f'
headerformatstr = '%20s  %15s %10.3f %10s'
	

#  Word list

print >>outfileLatex, "{\LARGE Words, sorted by frequency}\n"  
print >>outfileLatex, "\\vspace{1cm}"
print >>outfileLatex 		 
print >>outfileLatex, "\\begin{tabular}{llllll}\\toprule"
print >>outfileLatex, "   rank & word & count & frequency & plog \\\\ \\midrule " 	

for i in range(NumberOfRows):			 
	word = WordList[i]	 
	data.append((i+1, word , Words[word], float(Words[word])/totalwordcount, -1* math.log(  float(Words[word])/totalwordcount,2 )))
for (i, word, count,frequency,plog) in data:
	if word == "&":
		word = "\&" 
	print >>outfileLatex,  "%5d & %10s & %10d & %10.3f & %10.3f  \\\\" % (i, word, count, frequency, plog) 

print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 



#  Bigram MI list


data = list()
print >>outfileLatex, "{\LARGE Word pairs, sorted by bigram frequency}\n"  
print >>outfileLatex, "\\vspace{1cm}" 
print >>outfileLatex  		 	 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog  & MI & weighted MI \\\\ \\midrule "

 
data = list()
for i in range(len(BigramList)):			 
	bigram = BigramList[i]	 
	thesewords = bigram.split()
	word1 = thesewords[0]
	word2 = thesewords[1]
	if word1 not in Words or word2 not in Words: continue 
	freq1 = float(Words[word1]) / totalwordcount
	freq2 = float(Words[word2]) / totalwordcount
	bigram_count = float(Bigrams[bigram])
	bigram_frequency = bigram_count/totalbigramcount
	plog = math.log (totalbigramcount/bigram_count,2)
	MI =    math.log(  float(Bigrams[bigram])/totalbigramcount / (freq1 * freq2)  ,2 )
	WMI = MI * Bigrams[bigram]
	data.append((i+1, bigram , bigram_count, bigram_frequency, plog , MI, WMI ))

for i in range(NumberOfRows):
	(i, bigram, bigram_count,bigram_frequency,plog, MI, WMI) = data[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.3f\\\\ " % (i, bigram, bigram_count, bigram_frequency, plog,MI, WMI) 

print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 
 



 
#  sort by MI
print >>outfileLatex, "{\LARGE Word pairs, sorted by repelling bigram mutual information}\n"  
print >>outfileLatex, "\\vspace{1cm}"
print >>outfileLatex   		 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
data.sort(key = lambda item:item[5]) 
for i in range(NumberOfRows):
	(i, bigram, bigram_count,bigram_frequency,plog, MI, WMI) = data[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %14.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, bigram_count, bigram_frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 
 
#  sort by MI reversed
print >>outfileLatex, "{\Large Word pairs, sorted by attracting bigram mutual information}\n\n" 
print >>outfileLatex, "\\vspace{1cm}"
print >>outfileLatex   					 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
data.sort(key = lambda item:item[5], reverse=True) 
for i in range(NumberOfRows):
	(i, bigram, bigram_count,bigram_frequency,plog, MI, WMI) = data[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %15.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, bigram_count, bigram_frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 
 
#  sort by WMI
print >>outfileLatex, "{\Large Word pairs, sorted by attracting bigram weighted mutual information}\n\n" 
print >>outfileLatex, "\\vspace{1cm}"
print >>outfileLatex   				 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
data.sort(key = lambda item:item[6], reverse=True) 
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = data[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, bigram_count, bigram_frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 
 



#-----------------------------------------------------------------------------------------------------------%


#--------------------------%


sublist = list()
for item in data:
	words = item[1].split()	
	if words[0] == keyword or words[1] == keyword:
		sublist.append(item)
print >>outfileLatex, "{\LARGE Word pairs, sorted by bigram count}\n"  
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex 
print >>outfileLatex, "{\Large with {\em", keyword, "}}"  
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
sublist.sort(key = lambda item:item[2], reverse=True) 
if len(sublist) < NumberOfRows:
	NumberOfRows = len(sublist)
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = sublist[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, count, frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 


print >>outfileLatex, "{\Large Word pairs, with", 		 
print >>outfileLatex, "{\\em ", keyword,"}"  		 
print >>outfileLatex, " sorted by Weighted Mutual Information}\n\n" 		 
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
sublist.sort(key = lambda item:item[6], reverse=True) 
if len(sublist) < NumberOfRows:
	NumberOfRows = len(sublist)
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = sublist[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, count, frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 

 

#  Left only

sublist = list()
for item in data:
	words = item[1].split()	
	if words[0] == keyword:
		sublist.append(item)
print >>outfileLatex, "{\Large Word pairs, with", 		 
print >>outfileLatex, "{\\em ", keyword,"}"  		 
print >>outfileLatex, " on left side, sorted by bigram count}\n\n" 
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex 		 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
sublist.sort(key = lambda item:item[2], reverse=True) 
if len(sublist) < NumberOfRows:
	NumberOfRows = len(sublist)
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = sublist[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, count, frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 
print >>outfileLatex, "{\Large Word pairs, with", 		 
print >>outfileLatex, "{\\em ", keyword,"}"  		 
print >>outfileLatex, " on left side, sorted by Weighted Mutual Information}\n\n" 	
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex 	 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
sublist.sort(key = lambda item:item[6], reverse=True) 
if len(sublist) < NumberOfRows:
	NumberOfRows = len(sublist)
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = sublist[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, count, frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 


#  Right only

sublist = list()
for item in data:
	words = item[1].split()	
	if words[1] == keyword:
		sublist.append(item)
print >>outfileLatex, "{\Large Word pairs, with", 		 
print >>outfileLatex, "{\\em ", keyword,"}"  		 
print >>outfileLatex, " on right side, sorted by bigram count}\n\n" 
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex 		 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
sublist.sort(key = lambda item:item[2], reverse=True) 
if len(sublist) < NumberOfRows:
	NumberOfRows = len(sublist)
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = sublist[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, count, frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 
print >>outfileLatex, "{\Large Word pairs, with", 		 
print >>outfileLatex, "{\\em ", keyword,"}"  		 
print >>outfileLatex, " on right side, sorted by Weighted Mutual Information}\n\n" 	
print >>outfileLatex, "\\vspace{.3cm}"  
print >>outfileLatex 	 
print >>outfileLatex, "\\begin{tabular}{llllllll}\\toprule"
print >>outfileLatex, "   rank & bigram & count & frequency & plog   & MI & weighted MI \\\\ \\midrule "
sublist.sort(key = lambda item:item[6], reverse=True) 
if len(sublist) < NumberOfRows:
	NumberOfRows = len(sublist)
for i in range(NumberOfRows):
	(i, bigram, count,frequency,plog, MI, WMI) = sublist[i]
	print >>outfileLatex,  "%5d & %10s & %10d & %10.6f & %10.3f & %10.3f & %10.1f\\\\ " % (i, bigram, count, frequency, plog,MI, WMI) 
print >>outfileLatex, "\\bottomrule \n \\end{tabular}", "\n\n"
print >>outfileLatex, "\\newpage" 









 









print >>outfileLatex, "\\end{document}" 










