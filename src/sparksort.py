import sys
from pyspark import SparkContext
import time


print "Input file is: ", sys.argv[1]
print "Number of arguemnts passed are: ", len(sys.argv)


def main(args):
    #Check if input file is passed for sorting
    if len(sys.argv) == 3:
        print "Input is in", sys.argv[1]
        print "Output will be stored in ", sys.argv[2]
        inFilePath=sys.argv[1]
        outFilePath=sys.argv[2]
        pass
    else:
        print "Please speify the path of the file for the program to begin."
        sys.exit()
    #Get the spark contex 
    sc = SparkContext("local","Sort on Spark")

    #start the timer
    start = time.time()
    
    #create an RDD to read the contents of input file
    #split the RDD to get each word for sorting file
    #finally sort he each word alphabetically in ascending order 
    tempRDD = sc.textFile(inFilePath).flatMap(lambda l: l.split("\n"))
    tempRDD2 = tempRDD.map(lambda l: (l[:10],l[10:])).sortByKey(True)
      
    #find time taken
    duration = time.time() - start
    print "Duration for Sorting on Spark is(ms): ", duration

    #finally save the output to the external text file
    tempRDD2.saveAsTextFile(outFilePath)

if __name__ == '__main__':
    main(sys.argv[1:])







