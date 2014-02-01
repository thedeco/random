import os,sys,optparse
parser = optparse.OptionParser('usage: usage: djb2hashcrack.py -f <djb2 hashlist> -w <wordlist>')
parser.add_option('-f', dest='djfile', type='string', help='specify target djb2 hashlist')
parser.add_option('-w', dest='wordlist', type='string', help='specify a wordlist')
(options, args) = parser.parse_args()
djfile=options.djfile
wordlist=options.wordlist
if (djfile == None) | (wordlist == None):
	print parser.usage
	exit(0)

def djb2(password):
  hash = 5381
  for c in password:
    hash = ((hash * 33) + ord(c)) & (0xffffffff)
  return str(hash)

f=open(djfile,'r')
x=f.readlines()
count = 0
solved=0
for hash in x:
	count=count+1

print 'Running DJB2 Hash Crack version 1.0 against '+str(count)+' DJB2 Hashes'

with open(wordlist,'r') as f:
	for line in f:
		line=line.strip()
		if line.isalnum():
			result=djb2(line)
			result=result.strip()
			for i in x:
				i=i.strip()
				if i == result:
					solved=solved+1
					print '[+]Hash Cracked ('+str(solved)+'/'+str(count)+'): '+result+':'+line
		else:
			pass
