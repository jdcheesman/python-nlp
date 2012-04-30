import sys, os
from subprocess import Popen, PIPE
from FeatureFactory import FeatureFactory

"""
Do not modify this class
The submit script does not use this class
It directly calls the methods of FeatureFactory and MEMM classes.
"""
def main(argv):
    if len(argv) < 3:
        print 'USAGE: python NER.py <train|test> trainFile testFile'
        exit(0)

    printOp = ''
    if len(argv) > 3:
        printOp = '-print'


    if argv[0] == 'train':
        print 'training...'
        featureFactory = FeatureFactory()

        # read the train and test data
        trainData = featureFactory.readData(argv[1])
        testData = featureFactory.readData(argv[2])

        # add the features
        trainDataWithFeatures = featureFactory.setFeaturesTrain(trainData);
        testDataWithFeatures = featureFactory.setFeaturesTest(testData);

        # write the updated data into JSON files
        featureFactory.writeData(trainDataWithFeatures, 'trainWithFeatures');
        featureFactory.writeData(testDataWithFeatures, 'testWithFeatures');
    else:
        print 'testing...'
        # run MEMM
        output = Popen(['java','-cp', 'classes', '-Xmx2G' ,'MEMM'
                        ,'trainWithFeatures.json', 'testWithFeatures.json',
                        printOp], stdout=PIPE).communicate()[0]

        print output

    print '... done.'

if __name__ == '__main__':
    main(sys.argv[1:])



