import java.io.BufferedReader;
import java.io.FileReader;
import java.io.StringReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.io.File;
import java.util.Arrays;


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
    return "3";
  }


  private List<String> validParts() {
    List<String> parts = new ArrayList<String>();
    parts.add("Development All Words");
    parts.add("Testing All Words");
    parts.add("Development Without Stop Words");
    parts.add("Testing Without Stop Words");
    return parts;
  }

  private List<List<String>> sources() {
    List<List<String>> srcs = new ArrayList<List<String>>();
    List<String> tmp;
    
    // Java.
    tmp = new ArrayList<String>(1);
    tmp.add("NaiveBayes.java");
    srcs.add(tmp);
    tmp = new ArrayList<String>(1);
    tmp.add("NaiveBayes.java");
    srcs.add(tmp);
    tmp = new ArrayList<String>(1);
    tmp.add("NaiveBayes.java");
    srcs.add(tmp);
    tmp = new ArrayList<String>(1);
    tmp.add("NaiveBayes.java");
    srcs.add(tmp);
    return srcs;
  }

  private String challenge_url() {
    return "http://www.coursera.org/nlp/assignment/challenge";
  }

  private String submit_url() {
    return "http://www.coursera.org/nlp/assignment/submit";
  }


  // return either accuracy or the answer list.
  protected String output(int partId, String ch_aux) {
    String trainPath = "../data/imdb1/";

    if(partId == 1) { // train splits, all words return null;
      NaiveBayes nb = new NaiveBayes();
      List<NaiveBayes.TrainSplit> splits = nb.getTrainSplits(trainPath);
      // naive bayes.
      double avgAccuracy = 0.0;
      for(NaiveBayes.TrainSplit split : splits) {
        NaiveBayes classifier = new NaiveBayes();
        classifier.train(split);
        // now eval.
        double accuracy = classifier.evaluate(split);
        avgAccuracy += accuracy;
      }
      avgAccuracy /= splits.size();
      return String.format("accuracy: 1 %f", avgAccuracy);
    } else if (partId == 2) { // test data, all words
      NaiveBayes nb = new NaiveBayes();
      nb.train(trainPath);
      List<List<String>> testData = nb.readTest(ch_aux);
      StringBuilder sb = new StringBuilder();
      sb.append("2\n");
      for(List<String> document : testData) {
        String guess = nb.classify(document);
        sb.append(guess + "\n");
      }
      return sb.toString();
    } else if (partId == 3) { // train splits, no stopwords
      NaiveBayes nb = new NaiveBayes();
      nb.FILTER_STOP_WORDS = true;
      List<NaiveBayes.TrainSplit> splits = nb.getTrainSplits(trainPath);
      double avgAccuracy = 0.0;
      for(NaiveBayes.TrainSplit split : splits) {
        NaiveBayes classifier = new NaiveBayes();
        classifier.train(split);
        double accuracy = classifier.evaluate(split);
        avgAccuracy += accuracy;
      }
      avgAccuracy /= splits.size();
      return String.format("accuracy: 3 %f", avgAccuracy);
    } else if (partId == 4) { // test data, no stopwods
      NaiveBayes nb = new NaiveBayes();
      nb.FILTER_STOP_WORDS = true;
      nb.train(trainPath);
      List<List<String>> testData = nb.readTest(ch_aux);
      StringBuilder sb = new StringBuilder();
      sb.append("4\n");
      for(List<String> document : testData) {
        String guess = nb.classify(document);
        sb.append(guess + "\n");
      }
      return sb.toString();
    } else {
      System.err.println("Unknown partId: " + partId);
      return null;
    }
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
      out.write("email_address=" + email.replaceAll("\\+", "%2B"));
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
      System.out.print("Login (Email address): ");
      BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
      String line = in.readLine();
      results[0] = line.trim();

      System.out.print("Password: ");
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


  public static void main(String [] args) {
    Submit submit = new Submit();
    submit.submit(0);
  }
}
