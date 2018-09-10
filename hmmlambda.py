from __future__ import division
import sys
import collections
import json,time


def  main(argv):

    line =[]

    with open(argv[1]) as fileHandle:
         for eachline in fileHandle.readlines():
             eachline =eachline.decode(encoding ="utf-8")
             line.append(eachline.replace("\n", "" ).split(" "))
    taggedword =[]
    for everyLine in line:
        linelist = []
        for wordtagpair in everyLine:
            index =wordtagpair.rindex("/")
            pair = [ wordtagpair[:index] ,wordtagpair[index+1:]]
            pair = tuple(pair)
            linelist.append(pair)
        if linelist:
            taggedword.append(linelist)

    tagset = set(i[1] for e in taggedword for i in e )
    tagset =list(tagset)

    trans = collections.defaultdict(dict)
    count_tag ={}

    for i in range(0,len(taggedword)):
        for j in range(1,len(taggedword[i])):
            taggedword[i][j][1]

            curTag = taggedword[i][j][1]
            prevTag =taggedword[i][j-1][1]
            if(trans[prevTag].has_key(curTag)):
                trans[prevTag][curTag] = trans[prevTag][curTag]+1
            else:
                trans[prevTag][curTag]=1
            if (count_tag.has_key(prevTag)):
                count_tag[prevTag] = count_tag[prevTag] + 1
            else:
                count_tag[prevTag] = 1
    count_start_word={}
    count_end_word={}
    emission =collections.defaultdict(dict)
    count_tag_em={}
    for i in range(0,len(taggedword)):
        for j in range(0,len(taggedword[i])):

            curWord = taggedword[i][j][0]
            curWordTag = taggedword[i][j][1]
            if (j == 0):
                if count_start_word.has_key(curWordTag):
                    count_start_word[curWordTag] =count_start_word[curWordTag]+1
                else:
                    count_start_word[curWordTag]=1
                if trans["start"].has_key(curWordTag):
                    trans["start"][curWordTag] = trans["start"][curWordTag]+1
                else:
                    trans["start"][curWordTag]=1
            if(j==len(taggedword[i])-1):
                if count_end_word.has_key(curWordTag):
                    count_end_word[curWordTag] =count_end_word[curWordTag]+1
                else:
                    count_end_word[curWordTag]=1
                if trans[curWordTag].has_key("endstate"):
                    trans[curWordTag] ["endstate"] = trans[curWordTag] ["endstate"]+1
                else:
                    trans[curWordTag]["endstate"]=1
            if (count_tag_em.has_key(curWordTag)):
                count_tag_em[curWordTag] = count_tag_em[curWordTag] + 1
            else:
                count_tag_em[curWordTag] = 1
            if(emission[curWord].has_key(curWordTag)):
                emission[curWord][curWordTag] = emission[curWord][curWordTag] + 1
            else:
                emission[curWord][curWordTag] = 1
    tagset.append("endstate")
    number_of_tags = len(tagset)
    number_of_keys_in_trans = len(trans)
    unseen_transitions = 0
    for eachTag in trans.keys():
        for nextTag in tagset:

            if not trans[eachTag].has_key(nextTag):
                unseen_transitions += 1
                trans[eachTag][nextTag] = 0
    non_present_tags = list(set(tagset) - set(count_tag.keys()))

    count_sentence = len(taggedword)
    for each_non_present_tag in non_present_tags:
        count_tag[each_non_present_tag] = 0
    additive =0
    for eachCurTag in trans.keys():
        for eachNextTag in trans[eachCurTag].keys():
            if trans[eachCurTag][eachNextTag]==0:
                additive=count_sentence

            if eachCurTag == "start" or eachNextTag == "endstate":
                trans[eachCurTag][eachNextTag] = (trans[eachCurTag][eachNextTag] + 1) / float(count_sentence + number_of_tags +additive)
                additive=0

            else:
                trans[eachCurTag][eachNextTag] = (trans[eachCurTag][eachNextTag] + 1) / float(count_tag[eachCurTag] + number_of_tags +additive)
                additive=0


    for eachCurWord in emission.keys():
        for eachCorrespondingTagForWord in emission[eachCurWord].keys():
            emission[eachCurWord][eachCorrespondingTagForWord] = (emission[eachCurWord][eachCorrespondingTagForWord]) / float(count_tag_em[eachCorrespondingTagForWord])


    with open('hmmmodel.txt', 'w') as f:
        dump_text = {"transition_probabilities" :trans ,"emission_probabilities":emission , "tagset":tagset  }
        json.dump(dump_text, f)


if __name__ == "__main__":
    start = time.time()
    main(sys.argv)
    #print time.time()-start