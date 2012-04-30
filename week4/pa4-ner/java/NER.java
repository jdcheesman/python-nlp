import java.util.*;
import java.io.*;


/** Do not modify this class
 *  The submit script does not use this class 
 *  It directly calls the methods of FeatureFactory and MEMM classes.
 */
public class NER {
    
    public static void main(String[] args) throws IOException {
	if (args.length < 2) {
	    System.out.println("USAGE: java -cp classes NER ../data/train ../data/dev");
	    return;
	}	    

	String print = "";
	if (args.length > 2 && args[2].equals("-print")) {
	    print = "-print";
	}

	System.out.println("Setting up Environment");
	setUpEnv(args);
	System.gc(); // ever hopeful.
	System.out.println("Running process");

	// run MEMM
	String[] newArgs = {"trainWithFeatures.json", "testWithFeatures.json", print};
	new MEMM(newArgs);
//        ProcessBuilder pb =
//	    new ProcessBuilder("java", "-cp", "classes", "-Xmx2G", "MEMM", "trainWithFeatures.json", "testWithFeatures.json", print);
//        pb.redirectErrorStream(true);
//        Process proc = pb.start();
//
//	BufferedReader br = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//	String line = br.readLine();
//	while (line != null) {
//	    System.out.println(line);
//	    line = br.readLine();
//	}
	
    }

	private static void setUpEnv(String[] args) throws IOException {
		FeatureFactory ff = new FeatureFactory();
		// read the train and test data
		String name = args[0];
		String outputFileName = "trainWithFeatures";
		writeJSONFile(ff, name, outputFileName);

		name = args[1];
		outputFileName = "testWithFeatures";
		writeJSONFile(ff, name, outputFileName);
	}

	private static void writeJSONFile(FeatureFactory ff, String name,
			String outputFileName) throws IOException {
		List<Datum> trainData = ff.readData(name);
		List<Datum> trainDataWithFeatures = ff.setFeaturesTrain(trainData);
		ff.writeData(trainDataWithFeatures, outputFileName);
	}
}