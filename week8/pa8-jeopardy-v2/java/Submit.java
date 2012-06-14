import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.StringReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.StringWriter;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.io.File;
import java.util.Arrays;

import org.json.simple.*;

public class Submit {

	public void submit(Integer partId) {
		System.out.println(String.format("==\n== [nlp-class] Submitting Solutions" +
				" | Programming Exercise %s\n==", homework_id()));

		partId = promptPart();
		List<String> partNames = validParts();
		if(!isValidPartId(partId)) {
			System.err.println("!! Invalid homework part selected.");
			System.err.println(String.format("!! Expected an integer from 1 to %d.", 
					partNames.size() + 1));
			System.err.println("!! Submission Cancelled");
			return;
		}

		String [] loginPassword = loginPrompt();
		String login = loginPassword[0];
		String password = loginPassword[1];

		if(login == null || login.equals("")) {
			System.out.println("!! Submission Cancelled");
			return;
		}

		System.out.print("\n== Connecting to nlp-class ... ");

		// Setup submit list
		List<Integer> submitParts = new ArrayList<Integer>();
		if(partId == partNames.size() + 1) {
			for(int i = 1; i < partNames.size() + 1; i++) {
				submitParts.add(new Integer(i));
			}
		}
		else {
			submitParts.add(new Integer(partId));
		}

		for(Integer part : submitParts) {
			// Get Challenge
			String [] loginChSignature = getChallenge(login, part);
			if(loginChSignature == null) {
				return;
			}
			login = loginChSignature[0];
			String ch = loginChSignature[1];
			String signature = loginChSignature[2];
			String ch_aux = loginChSignature[3];

			// Attempt Submission with Challenge
			String ch_resp = challengeResponse(login, password, ch);
			String result = submitSolution(login, ch_resp, part.intValue(), output(part, ch_aux),
					source(part), signature);
			if(result == null) {
				result = "NULL RESPONSE";
			}
			System.out.println(String.format(
					"\n== [nlp-class] Submitted Homework %s - Part %d - %s",
					homework_id(), part, partNames.get(part - 1)));
			System.out.println("== " + result.trim());
		}
	}


	private String homework_id() {
		return "8";
	}


	private List<String> validParts() {
		List<String> parts = new ArrayList<String>();
		parts.add("Development Wiki");
		parts.add("Testing Wiki");
		parts.add("Development Googling");
		parts.add("Testing Googling");
		return parts;
	}

	private List<List<String>> sources() {
		List<List<String>> srcs = new ArrayList<List<String>>();
		List<String> tmp;

		// Java.
		tmp = new ArrayList<String>(1);
		tmp.add("Wiki.java");
		srcs.add(tmp);
		tmp = new ArrayList<String>(1);
		tmp.add("Wiki.java");
		srcs.add(tmp);
		tmp = new ArrayList<String>(1);
		tmp.add("Googling.java");
		srcs.add(tmp);
		tmp = new ArrayList<String>(1);
		tmp.add("Googling.java");
		srcs.add(tmp);
		return srcs;
	}

	private String challenge_url() {
		return "https://class.coursera.org/nlp/assignment/challenge";
	}

	private String submit_url() {
		return "https://class.coursera.org/nlp/assignment/submit";
	}

	// ========================= CHALLENGE HELPERS =========================

	private String source(int partId) {
		StringBuffer src = new StringBuffer();
		List<List<String>> src_files = sources();
		if(partId < src_files.size()) {
			List<String> flist = src_files.get(partId - 1);
			for(String fname : flist) {
				try {
					BufferedReader reader = new BufferedReader(new FileReader(fname));
					String line;
					while((line = reader.readLine()) != null) {
						src.append(line);
					}
					reader.close();
					src.append("||||||||");
				} catch (IOException e) {
					System.err.println(String.format("!! Error reading file '%s': %s",
							fname, e.getMessage()));
					return src.toString();
				}
			}
		}
		return src.toString();
	}


	private boolean isValidPartId(int partId) {
		List<String> partNames = validParts();
		return (partId >= 1 && partId <= partNames.size() + 1);
	}

	private int promptPart() {
		int partId = -1;
		System.out.println("== Select which part(s) to submit:");
		List<String> partNames = validParts();
		List<List<String>> srcFiles = sources();
		StringBuffer prompt = new StringBuffer();
		for(int i = 1; i < partNames.size() + 1; i++) {
			prompt.append(String.format("==  %d) %s [", i, partNames.get(i - 1)));
			List<String> srcs = srcFiles.get(i - 1);
			for(String src : srcs) {
				prompt.append(String.format(" %s ", src));
			}
			prompt.append("]\n"); 
		}
		prompt.append(String.format("==  %d) All of the above \n", partNames.size() + 1));
		prompt.append(String.format("==\nEnter your choice [1-%d]: ", partNames.size() + 1));
		System.out.println(prompt.toString());
		try {
			BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
			String line = in.readLine();
			partId = Integer.parseInt(line);
			if(!isValidPartId(partId)) {
				partId = -1;
			}
		} catch (Exception e) {
			System.err.println("!! Error reading partId from stdin: " + e.getMessage());
			return -1;
		}
		return partId;
	}


	// Returns [email,ch,signature]
	private String[] getChallenge(String email, int partId) {
		String [] results = new String[4];
		try {
			URL url = new URL(challenge_url());
			URLConnection connection = url.openConnection();
			connection.setDoOutput(true);
			OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());
			out.write("email_address=" + email);
			out.write("&assignment_part_sid=" + String.format("%s-%s", homework_id(), partId));
			out.write("&response_encoding=delim");
			out.close();
			BufferedReader in = new BufferedReader(
					new InputStreamReader(connection.getInputStream()));
			StringBuffer sb = new StringBuffer();
			String line;
			while((line = in.readLine()) != null) {
				sb.append(line + "\n");
			}
			String str = sb.toString(); 
			in.close();

			String[] splits = str.split("\\|"); 

			if(splits.length < 8) {
				System.err.println("!! Error getting challenge from server.");
				for(String string : results) {
					System.err.println(string);
				}
				return null;
			} else {
				results[0] = splits[2]; // email
				results[1] = splits[4]; // ch
				results[2] = splits[6]; // signature
				if(splits.length == 9) { // if there's a challenge, use it
					results[3] = splits[8];
				} else {
					results[3] = null;
				}
			}
		} catch (Exception e) {
			System.err.println("Error getting challenge from server: " + e.getMessage());
		}
		return results;
	}

	private String submitSolution(String email, String ch_resp, int part, String output,
			String source, String state) {
		String str = null;
		try {
			StringBuffer post = new StringBuffer();
			post.append("assignment_part_sid=" + URLEncoder.encode(
					String.format("%s-%d", homework_id(), part), "UTF-8"));
			post.append("&email_address=" + URLEncoder.encode(email, "UTF-8"));
			post.append("&submission=" + URLEncoder.encode(base64encode(output), "UTF-8"));
			post.append("&submission_aux=" + URLEncoder.encode(base64encode(source), "UTF-8"));
			post.append("&challenge_response=" + URLEncoder.encode(ch_resp, "UTF-8"));
			post.append("&state=" + URLEncoder.encode(state, "UTF-8"));

			URL url = new URL(submit_url());
			URLConnection connection = url.openConnection();
			connection.setDoOutput(true);
			OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream());
			out.write(post.toString());
			out.close();

			BufferedReader in = new BufferedReader(
					new InputStreamReader(connection.getInputStream()));
			str = in.readLine();
			in.close();

		} catch (Exception e) {
			System.err.println("!! Error submittion solution: " + e.getMessage());
			return null;
		}
		return str;
	}


	// =========================== LOGIN HELPERS ===========================

	// Returns [login, password]
	private String[] loginPrompt() {
		String[] results = new String[2];
		try {
			System.out.println("Login (Email address): ");
			BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
			String line = in.readLine();
			results[0] = line.trim();

			System.out.println("Password: ");
			line = in.readLine();
			results[1] = line.trim();
		} catch (IOException e) {
			System.err.println("!! Error prompting for login/password: " + e.getMessage());
		}
		return results;
	}

	private String challengeResponse(String email, String passwd, String challenge) {
		MessageDigest md = null;
		try {
			md = MessageDigest.getInstance("SHA-1");
		} catch (NoSuchAlgorithmException e) {
			System.err.println("No such hashing algorithm: " + e.getMessage());
		}
		try {
			String message = challenge + passwd;
			md.update(message.getBytes("US-ASCII"));
			byte[] byteDigest = md.digest();
			StringBuffer buf = new StringBuffer();
			for(byte b : byteDigest) {
				buf.append(String.format("%02x",b));
			}
			return buf.toString();
		} catch (Exception e) {
			System.err.println("Error generating challenge response: " + e.getMessage());
		}
		return null;
	}

	public String base64encode(String str) {
		Base64 base = new Base64();
		byte[] strBytes = str.getBytes();
		byte[] encBytes = base.encode(strBytes);
		String encoded = new String(encBytes);
		return encoded;
	}

	// =========================== ASSIGNMENT CODE ===========================
	
	public String passXML() {
		String fname = "../XML/xml_output.txt";
		try {
			StringBuilder sb = new StringBuilder();
			sb.append("part[1]");
			BufferedReader br = new BufferedReader(new FileReader(fname));
			String line;
			while((line = br.readLine()) != null) {
				sb.append(line);
			}
			return sb.toString();
		} catch (IOException e) {
			System.err.println("Error submitting part 1 from filename '" + fname + "'. Error: " + e.getMessage());
			return null;
		}
	}

	public String gradeWiki(int partId, String ch_aux) {
		PrintStream out = System.out;
		PrintStream err = System.err;
		System.setOut(new PrintStream(new OutputStream() {
		    @Override public void write(int b) throws IOException {}
		}));
		System.setErr(new PrintStream(new OutputStream() {
		    @Override public void write(int b) throws IOException {}
		}));
		Wiki wiki = new Wiki();
		List<String> wives;
		String goldFile = "../data/gold.txt";
		String wivesFile = "../data/wives.txt";
		if (partId == 1) {
			wives = wiki.addWives(wivesFile);
		} else {
			String[] wivesSplit = ch_aux.split("\n");   
			wives = new ArrayList<String>(Arrays.asList(Arrays.copyOfRange(wivesSplit, 1, wivesSplit.length)));
		}
		String wikiFile = "../data/small-wiki.xml";
		List<String> infoBoxHusbands = wiki.processFile(new File(wikiFile), wives, true); 
		File mod_file = modifyWiki(ch_aux, wikiFile);
		List<String> noInfoHusbands = wiki.processFile(mod_file, wives, false);
		mod_file.delete();
		System.setOut(out);
		System.setErr(err);
		if (partId == 1) {
			int infoScore = evaluateAnswers(infoBoxHusbands, goldFile);
			int noInfoScore = evaluateAnswers(noInfoHusbands, goldFile);
			return String.format("%d", infoScore + noInfoScore);
		} else {
			return encodeWiki(infoBoxHusbands, noInfoHusbands);
		}
	}

	public File modifyWiki(String ch_aux, String wikiFile) {
		// open wikiFile...
		File wiki_mod = null;
		try {
			wiki_mod = new File("wiki_mod");
			BufferedReader br = new BufferedReader(new FileReader(wikiFile));
			BufferedWriter bw = new BufferedWriter(new FileWriter(wiki_mod));
			String line;
			while((line = br.readLine()) != null) {
				line.replace("Infobox", ch_aux);
				line.replace("|spouse", ch_aux.substring(3));
				bw.write(line + "\n");
			}
			br.close();
			bw.close();
		} catch (IOException e) { 
			System.err.println("Error modifying wiki: " + e.getMessage());
			return null;
		}
		return wiki_mod;
	}

	private int evaluateAnswers(List<String> husbandsLines, String goldFile) {
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
				return 0;
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
			return score;
		} catch (IOException e) {}
		return 0;
	}

	public String packageWiki(List<String> infoBoxHusbands, List<String> noInfoHusbands) {
		StringBuilder result = new StringBuilder();
		for(String husband : infoBoxHusbands) {
			result.append(husband);
			result.append("##");
		}
		result = result.delete(result.length() - 2, result.length()); 
		result.append("\n");
		for(String husband : noInfoHusbands) {
			result.append(husband);
			result.append("##");
		}
		result = result.delete(result.length() - 2, result.length()); 
		return result.toString();
	}
	
	public String encodeWiki(List<String> infoBoxHusbands, List<String> noInfoHusbands) {
		JSONArray result = new JSONArray();
		result.add(infoBoxHusbands);
		result.add(noInfoHusbands);
		StringWriter out = new StringWriter();
		try {
			result.writeJSONString(out);
		} catch (IOException e) {
			e.printStackTrace();
		}
		String jsonText = out.toString();
		return jsonText;
	}

	int scoreAnswers(List<Googling.Location> guesses, List<Googling.LocationPossibilities> gold, List<String> landmarks) {
		List<Integer> correctCities = new ArrayList<Integer>();
		List<Integer> incorrectCities = new ArrayList<Integer>();
		List<Integer> noguessCities = new ArrayList<Integer>();
		List<Integer> correctCountries = new ArrayList<Integer>();
		List<Integer> incorrectCountries = new ArrayList<Integer>();
		List<Integer> noguessCountries = new ArrayList<Integer>();
		for(int i = 0; i < guesses.size(); ++i) {
			if(gold.get(i).cities.contains(guesses.get(i).city.toLowerCase())) {
				correctCities.add(i);
			} else if(guesses.get(i).city == "") {
				noguessCities.add(i);
			} else {
				incorrectCities.add(i);
			}
			if(guesses.get(i).country.equalsIgnoreCase(gold.get(i).country)) {
				correctCountries.add(i);
			} else if(guesses.get(i).country == "") {
				noguessCountries.add(i);
			} else {
				incorrectCountries.add(i);
			}
		}
		int correctTotal = correctCities.size() + correctCountries.size();
		int noguessTotal = noguessCities.size() + noguessCountries.size();
		int incorrectTotal = incorrectCities.size() + incorrectCountries.size();
		return correctTotal - incorrectTotal;
	}
	
	public String constructDataObject(List<Googling.Location> guesses) {
		StringBuilder result = new StringBuilder();
		for(Googling.Location guess : guesses) {
			result.append(guess.city);
			result.append("##");
		}
		result = result.delete(result.length() - 2, result.length()); 
		result.append("\n");
		for(Googling.Location guess : guesses) {
			result.append(guess.country);
			result.append("##");
		}
		result = result.delete(result.length() - 2, result.length()); 
		return result.toString();
	}
	
	public String encodeGoogling(List<Googling.Location> guesses) {
		List<String> cities = new ArrayList<String>();
		List<String> countries = new ArrayList<String>();
		for(Googling.Location guess : guesses) {
			cities.add(guess.city);
			countries.add(guess.country);
		}
		JSONArray result = new JSONArray();
		result.add(cities);
		result.add(countries);
		StringWriter out = new StringWriter();
		try {
			result.writeJSONString(out);
		} catch (IOException e) {
			e.printStackTrace();
		}
		String jsonText = out.toString();
		return jsonText;
	}

	public String gradeGoogling(int partId, String ch_aux) {
		PrintStream out = System.out;
		PrintStream err = System.err;
		System.setOut(new PrintStream(new OutputStream() {
		    @Override public void write(int b) throws IOException {}
		}));
		System.setErr(new PrintStream(new OutputStream() {
		    @Override public void write(int b) throws IOException {}
		}));
		String googleResultsFile = "../data/googleResults_tagged.txt";
		String goldFile = "../data/landmarks.txt";
		Googling googling = new Googling(); 
		List<List<Googling.GoogleQuery>> queryData = null;
		List<Googling.LocationPossibilities> goldData = null;
		List<String> landmarks = null;
		if(partId == 3) {
			queryData = googling.readInData(googleResultsFile);
			landmarks = new ArrayList<String>();
			goldData = googling.readInGold(landmarks, goldFile);
		}
		if (partId == 4) {
			String[] lines = ch_aux.split("\n");
			landmarks = new ArrayList<String>();
			for(int i = 0; i < 10; ++i) {
				landmarks.add(lines[i]);
			}
			ArrayList<String> queryPart = new ArrayList<String>();
			for(int i = 11; i < lines.length; ++i) {
				queryPart.add(lines[i]);
			}
			queryData = googling.readString(queryPart);
		}
		List<Googling.Location> guesses = googling.processQueries(queryData);
		System.setOut(out);
		System.setErr(err);
		if(partId == 3) {
			return "" + scoreAnswers(guesses, goldData, landmarks);
		} else {
			//return constructDataObject(guesses);
			return encodeGoogling(guesses);
		}
	}



	// return either accuracy or the answer list.
	protected String output(int partId, String ch_aux) {
		if (partId == 1 || partId == 2) {
			String score = gradeWiki(partId, ch_aux);
			return String.format("part[%d][%s", partId, score);
		} else if (partId == 3 || partId == 4) {
			String score = gradeGoogling(partId, ch_aux);
			return String.format("part[%d][%s", partId, score);
		} else {
			System.err.println("Unknown partId: " + partId);
			return null;
		}
	}

	public static void main(String [] args) {
		Submit submit = new Submit();
		submit.submit(0);
	}
}
