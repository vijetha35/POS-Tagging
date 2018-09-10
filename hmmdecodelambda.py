import sys,collections
import json,operator

def decode_sentence(sentence):
    backpointer = collections.defaultdict(dict)
    viterbi = collections.defaultdict(dict)
    if not emission.has_key(sentence[0]):
        emission[sentence[0]] = {tag : 1 for tag in tagset}
    for eachstate in emission[sentence[0]]:
        viterbi[0][eachstate] = trans["start"][eachstate] * emission[sentence[0]][eachstate]
        backpointer[0][eachstate] = "start"
    for i in range(1, len(sentence)):
        if not emission.has_key(sentence[i]):
            emission[sentence[i]] = {tag: 1 for tag in tagset}

        for currentTag in emission[sentence[i]]:
            previous_states = viterbi[i - 1].keys()
            maxprev = 0
            for previous_tag in previous_states:
                if previous_tag=="endstate":
                    continue
                val = viterbi[i - 1][previous_tag] * trans[previous_tag][currentTag] * emission[sentence[i]][currentTag]
                if val >=maxprev:
                    maxprev = val
                    backpointer[i][currentTag] = previous_tag
            viterbi[i][currentTag] = maxprev

    last_tag = max(viterbi[len(viterbi) - 1].iteritems(), key=operator.itemgetter(1))[0]
    ans = [last_tag]

    for i in range(len(backpointer) - 1, -1, -1):
        ans.insert(0, backpointer[i][last_tag])
        last_tag = backpointer[i][last_tag]
    return ans[1:]

def  main(argv):


    line =[]
    with open(argv[1],'r') as fileHandle:
         for eachline in fileHandle.readlines():
             eachline = eachline.decode("utf-8")
             line.append(eachline.replace("\n", "").split(" "))

    writeFile = open("hmmoutput.txt","w+")
    for sentence in line:
        ans = decode_sentence(sentence)
        for i in range(0,len(sentence)):
            if(i==len(sentence)-1):
                writeString =sentence[i] + "/"+ ans[i]
                writeString = writeString.encode("utf-8")
                writeFile.write(writeString)
            else:
                writeString = sentence[i] + "/" + ans[i]+ " "
                writeString  =writeString.encode("utf-8")
                writeFile.write(writeString)
        writeFile.write( "\n")
    writeFile.close()

with open("hmmmodel.txt", 'r') as model:
    dumpedlist = json.load(model)
    trans = dumpedlist["transition_probabilities"]
    emission = dumpedlist["emission_probabilities"]
    tagset = dumpedlist["tagset"]
    trans =collections.defaultdict(lambda:dict, trans)
    emission = collections.defaultdict(lambda:dict,emission)


if __name__ == "__main__":
    main(sys.argv)

