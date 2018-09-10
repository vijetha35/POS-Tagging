from __future__ import division
import json,sys

def  main(argv):

    line=[]
    with open(argv[1],'r') as model:
        for eachline in model.readlines():
            eachline =eachline.decode(encoding ="utf-8")
            # print " eachline" ,eachline
            line.append(eachline.replace("\n", "").split(" "))

    devline=[]
    with open(argv[2],'r') as actual:
        for eachline in actual.readlines():
            eachline =eachline.decode(encoding ="utf-8")
            # print " eachline" ,eachline
            devline.append(eachline.replace("\n", "").split(" "))
    count =0
    totalcount=0
    f =open("error.txt", "w")
    for i in range(0,len(line)):
        for j in range(0,len(line[i])):
            totalcount+=1
            if line[i][j].strip() == devline[i][j].strip():
                count +=1
            else:
                 f.write(line[i][j].encode("utf-8")+ " not matching with " + devline[i][j].encode("utf-8")+"\n")


    print "accuracy is " , (count/totalcount)*100

if __name__ == "__main__":
    main(sys.argv)