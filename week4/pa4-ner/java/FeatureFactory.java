import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;

public class FeatureFactory {

    /** Add any necessary initialization steps for your features here.
     *  Using this constructor is optional. Depending on your
     *  features, you may not need to intialize anything.
     */
    public FeatureFactory() {

    }

    /**
     * Words is a list of the words in the entire corpus, previousLabel is the label
     * for position-1 (or O if it's the start of a new sentence), and position
     * is the word you are adding features for. PreviousLabel must be the
     * only label that is visible to this method. 
     */
    private List<String> computeFeatures(List<String> words,
    		String previousLabel, int position) {

    	List<String> features = new ArrayList<String>();

    	String currentWord = words.get(position);

    	// Baseline Features  
    	features.add("word=" + currentWord);
    	features.add("prevLabel=" + previousLabel);
    	features.add("word=" + currentWord + ", prevLabel=" + previousLabel);
    	/** Warning: If you encounter "line search failure" error when
    	 *  running the program, considering putting the baseline features
    	 *  back. It occurs when the features are too sparse. Once you have
    	 *  added enough features, take out the features that you don't need. 
    	 */

    	// TODO: Add your features here
    	if ((position-2) >= 0) {
    		features.add("prevBigram=" + words.get(position-2) + ' ' + words.get(position-1));
    	}
    	if ((position-1) >= 0) {
    		features.add("bigram=" + words.get(position-1) + ' ' + currentWord);
    	}
        features.add("word=" + currentWord + ", prevLabel=" + previousLabel);
    	
    	String[] greetings = {"hi", "hello", "hallo", "hullo", "thanks", "cheers", "dear"};
    	for (String g : greetings) {
            features.add("word=" + currentWord + ",prevWord=" + g);
            features.add("word=" + currentWord + ",prevWord=" + g + ", ");
    	}
    	String[] prepositions = {"to","for","in","on","at","by","near","besides","beside","opposite","from", "of", "off", "about", "onto", "below", "under", "before", "after"}; 
    	for (String prep : prepositions) {
    		features.add("word=" + currentWord + ",prevWord=" + prep);
    	}

    	features.add(getCharsFeature(currentWord));

    	return features;
    }

	public String getCharsFeature(String currentWord) {
		String charsFeature;
		char[] chars = currentWord.toCharArray();
    	boolean firstLetterCapital = isCapital(chars[0]);
    	boolean allCapitals = true;
    	boolean mixedCapitals = false;
    	boolean hasNumeric = false;
    	boolean allNumeric = true;
    	boolean weirdStuff = false;
    	
    	for (int i=0;i<chars.length;i++) {
    		allNumeric &= isNumeric(chars[i]);
    		hasNumeric |= isNumeric(chars[i]);
    		if (!isCapital(chars[i])) {
    			allCapitals = false;
    		}
    		if (i>0) {
    			mixedCapitals |= isCapital(chars[i]);
    		}
    		weirdStuff |= !isAlphaNumeric(chars[i]);
    	}
    	if (weirdStuff) {
    		charsFeature = "case=Weird";
    	}
    	else if (allNumeric) {
    		charsFeature = "case=Numeric";
    	}
    	else if (hasNumeric) {
    		charsFeature = "case=MixedNumeric";
    	}
    	else if (allCapitals) {
    		charsFeature = "case=Capitals";
    	}
    	else if (mixedCapitals) {
    		charsFeature = "case=Mixed";
    	}
    	else if (firstLetterCapital) {
    		charsFeature = "case=Title";
    	}
    	else {
    		charsFeature = "case=Lower";
    	}
		return charsFeature;
	}
	
	public boolean isAlphaNumeric(char c) {
		return isNumeric(c) || isCapital(c) || isLower(c);
	}

	public boolean isNumeric(char c) {
		return c >= '0' && c <= '9';
	}
    
    public boolean isCapital(char c) {
    	return c >= 'A' && c <= 'Z';
    }
    
    public boolean isLower(char c) {
    	return c >= 'a' && c <= 'z';
    }

    /** Do not modify this method **/
    public List<Datum> readData(String filename) throws IOException {

	List<Datum> data = new ArrayList<Datum>();
	BufferedReader in = new BufferedReader(new FileReader(filename));

	for (String line = in.readLine(); line != null; line = in.readLine()) {
	    if (line.trim().length() == 0) {
		continue;
	    }
	    String[] bits = line.split("\\s+");
	    String word = bits[0];
	    String label = bits[1];

	    Datum datum = new Datum(word, label);
	    data.add(datum);
	}

	return data;
    }

    /** Do not modify this method **/
    public List<Datum> readTestData(String ch_aux) throws IOException {

	List<Datum> data = new ArrayList<Datum>();

	for (String line : ch_aux.split("\n")) {
	    if (line.trim().length() == 0) {
		continue;
	    }
	    String[] bits = line.split("\\s+");
	    String word = bits[0];
	    String label = bits[1];

	    Datum datum = new Datum(word, label);
	    data.add(datum);
	}

	return data;
    }

    /** Do not modify this method **/
    public List<Datum> setFeaturesTrain(List<Datum> data) {
	// this is so that the feature factory code doesn't accidentally use the
	// true label info
	List<Datum> newData = new ArrayList<Datum>();
	List<String> words = new ArrayList<String>();

	for (Datum datum : data) {
	    words.add(datum.word);
	}

	String previousLabel = "O";
	for (int i = 0; i < data.size(); i++) {
	    Datum datum = data.get(i);

	    Datum newDatum = new Datum(datum.word, datum.label);
	    newDatum.features = computeFeatures(words, previousLabel, i);
	    newDatum.previousLabel = previousLabel;
	    newData.add(newDatum);

	    previousLabel = datum.label;
	}

	return newData;
    }

    /** Do not modify this method **/
    public List<Datum> setFeaturesTest(List<Datum> data) {
	// this is so that the feature factory code doesn't accidentally use the
	// true label info
	List<Datum> newData = new ArrayList<Datum>();
	List<String> words = new ArrayList<String>();
	List<String> labels = new ArrayList<String>();
	Map<String, Integer> labelIndex = new HashMap<String, Integer>();

	for (Datum datum : data) {
	    words.add(datum.word);
	    if (labelIndex.containsKey(datum.label) == false) {
		labelIndex.put(datum.label, labels.size());
		labels.add(datum.label);
	    }
	}

	// compute features for all possible previous labels in advance for
	// Viterbi algorithm
	for (int i = 0; i < data.size(); i++) {
	    Datum datum = data.get(i);

	    if (i == 0) {
		String previousLabel = "O";
		datum.features = computeFeatures(words, previousLabel, i);

		Datum newDatum = new Datum(datum.word, datum.label);
		newDatum.features = computeFeatures(words, previousLabel, i);
		newDatum.previousLabel = previousLabel;
		newData.add(newDatum);

	    } else {
		for (String previousLabel : labels) {
		    datum.features = computeFeatures(words, previousLabel, i);

		    Datum newDatum = new Datum(datum.word, datum.label);
		    newDatum.features = computeFeatures(words, previousLabel, i);
		    newDatum.previousLabel = previousLabel;
		    newData.add(newDatum);
		}
	    }

	}

	return newData;
    }

    /** Do not modify this method **/
    public void writeData(List<Datum> data, String filename)
	throws IOException {


	FileWriter file = new FileWriter(filename + ".json", false);

	       
	for (int i = 0; i < data.size(); i++) {
	    try {
		JSONObject obj = new JSONObject();
		Datum datum = data.get(i);
		obj.put("_label", datum.label);
		obj.put("_word", base64encode(datum.word));
		obj.put("_prevLabel", datum.previousLabel);

		JSONObject featureObj = new JSONObject();

		List<String> features = datum.features;
		for (int j = 0; j < features.size(); j++) {
		    String feature = features.get(j).toString();
		    featureObj.put("_" + feature, feature);
		}
		obj.put("_features", featureObj);
		obj.write(file);
		file.append("\n");
	    } catch (JSONException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	    }
	}
	file.close();
    }

    /** Do not modify this method **/
    private String base64encode(String str) {
	Base64 base = new Base64();
	byte[] strBytes = str.getBytes();
	byte[] encBytes = base.encode(strBytes);
	String encoded = new String(encBytes);
	return encoded;
    }

}
