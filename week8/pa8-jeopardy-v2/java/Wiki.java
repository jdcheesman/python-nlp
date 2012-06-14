//CS124 HW6 Wikipedia Relation Extraction
//Alan Joyce (ajoyce)

import java.util.regex.*;
import java.io.*;
import java.util.*;

public class Wiki {  

	public List<String> addWives(String fileName) {
		List<String> wives = new ArrayList<String>();
		try {
			BufferedReader input = new BufferedReader(new FileReader(fileName));
			// for each line
			for(String line = input.readLine(); line != null; line = input.readLine()) {
				wives.add(line);
			}
			input.close();
		} catch(IOException e) {
			e.printStackTrace();
			System.exit(1);
			return null;
		}
		return wives;
	}
	/*
    * read through the wikipedia file and attempts to extract the matching husbands. note that you will need to provide
    * two different implementations based upon the useInfoBox flag.
    */
	public List<String> processFile(File f, List<String> wives, boolean useInfoBox) {
		
		List<String> husbands = new ArrayList<String>();
		
		//TODO:
		// Process the wiki file and fill the husbands Array
		// +1 for correct Answer, 0 for no answer, -1 for wrong answers
		// add 'No Answer' string as the answer when you dont want to answer
		
		for(String wife : wives) {
			husbands.add("No Answer");
		}  
		return husbands;
	}

	/*
	 * scores the results based upon the aforementioned criteria
	 */
	public void evaluateAnswers(boolean useInfoBox, List<String> husbandsLines, String goldFile){
		int correct = 0;
		int wrong = 0;
		int noAnswers = 0;
		int score = 0;
		try {
			BufferedReader goldData = new BufferedReader(new FileReader(goldFile));
			List<String> goldLines = new ArrayList<String>();
			String line;
			while((line = goldData.readLine()) != null) {
				goldLines.add(line);
			}
			if(goldLines.size() != husbandsLines.size()) {
				System.err.println("Number of lines in husbands file should be same as number of wives!");
				System.exit(1);
			}
			for(int i = 0; i < goldLines.size(); i++) {
				String husbandLine = husbandsLines.get(i).trim();
				String goldLine = goldLines.get(i).trim();
				boolean exampleWrong = true; // guilty until proven innocent
				if(husbandLine.equals("No Answer")) {
					exampleWrong = false;
					noAnswers++;
				} else { // check if correct.
					String[] golds = goldLine.split("\\|");
					for(String gold : golds) {
						if (husbandLine.equals(gold)) {
							correct++;
							score++;
							exampleWrong = false;
							break;
						}
					}
				}
				if(exampleWrong) {
					wrong++;
					score--;
				} 
			}
			goldData.close();
		} catch(IOException e) {
			e.printStackTrace();
			System.exit(1);
		}     

		System.out.println("Correct Answers: " + correct); 
		System.out.println("No Answers     : " + noAnswers); 
		System.out.println("Wrong Answers  : " + wrong); 
		System.out.println("Total Score    : " + score); 

	}

	public static void main(String[] args) {
		String wikiFile = "../data/small-wiki.xml";
		String wivesFile = "../data/wives.txt";
		String goldFile = "../data/gold.txt";
		boolean useInfoBox = true;
		Wiki pedia = new Wiki();
		List<String> wives = pedia.addWives(wivesFile);
		List<String> husbands = pedia.processFile(new File(wikiFile), wives, useInfoBox);
		pedia.evaluateAnswers(useInfoBox, husbands, goldFile);
	}
}
