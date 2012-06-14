import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Googling {

	/*
	 * defines the components of a query result from Google.
	 */
	public class GoogleQuery {

		String title;
		String snip;
		String link;

		public GoogleQuery(String title, String snip, String link) {
			this.title = title;
			this.snip = snip;
			this.link = link;
		}

        @Override
        public String toString() {
            return ("title: " + title + "\nsnip: " + snip + "\nlink: " + link);
        }

	}

	/*
	 * note that you should not need to use this class. this class defines the possible locations 
	 * of a landmark. it differs from the location object in that it stores multiple possible location
	 * objects, while the location object only stores one possible guess for a city location.
	 */
	public class LocationPossibilities {

		List<String> cities;
		String country;

		public LocationPossibilities(List<String> cities, String country) {
			this.cities = cities;
			this.country = country;
		}
        
        @Override
        public String toString() {
            String locations = "";
            for(String city : cities) {
                locations += (city + ", ");
            }
            locations = locations.substring(0, locations.length() - 2); 
            return ("possible cities: " + locations + "\ncountry: " + country);
        }

	}

	/*
	 * defines the components of a location.
	 */
	class Location {

		String city;
		String country;

		public Location(String city, String country) {
			this.city = city;
			this.country = country;
		}
        
        @Override
        public String toString() {
            return ("city: " + city + "\ncountry: " + country);
        }
	}

	/*
	 * reads in data for a set of results for a single query
	 */
	List<GoogleQuery> readInSegment(List<String> lines) {
		List<GoogleQuery> queryResults = new ArrayList<GoogleQuery>();
		for(int i = 0; i < lines.size(); i += 3) {
			queryResults.add(new GoogleQuery(lines.get(i), lines.get(i + 1), lines.get(i + 2)));
		}
		return queryResults;
	}

	/*
	 * reads in data from a string rather than a file. assumes the same text file structure as readInData
	 */
	List<List<GoogleQuery>> readString(ArrayList<String> infoString){
		List<List<GoogleQuery>> queryData = new ArrayList<List<GoogleQuery>>();
		List<String> lines = infoString;
		int startline = 0;
		int endline = 0;
		while(startline < lines.size()) {
			int i = startline;
			while(i < lines.size() && lines.get(i).trim().length() > 0) {
				++i;
			}
			endline = i;
			List<String> tempLines = new ArrayList<String>(endline - startline);
			for(int j = startline; j < endline; ++j) {
				tempLines.add(lines.get(j));
			}
			queryData.add(readInSegment(tempLines));
			startline = endline + 1;
		}
		return queryData;
	}
	
	/*
	 * reads in the tagged query results output by Google. Takes in the name of the file containing the tagged Google results.
	 */
	List<List<GoogleQuery>> readInData(String googleResultsFile) {
		List<List<GoogleQuery>> queryData = new ArrayList<List<GoogleQuery>>();
		List<String> lines = new ArrayList<String>();
		try {
			BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(googleResultsFile), "UTF-8"));
			for(String line = reader.readLine(); line != null; line = reader.readLine()) {
				lines.add(line);
			}
			reader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		int startline = 0;
		int endline = 0;
		while(startline < lines.size()) {
			int i = startline;
			while(i < lines.size() && lines.get(i).trim().length() > 0) {
				++i;
			}
			endline = i;
			List<String> tempLines = new ArrayList<String>(endline - startline);
			for(int j = startline; j < endline; ++j) {
				tempLines.add(lines.get(j));
			}
			queryData.add(readInSegment(tempLines));
			startline = endline + 1;
		}
		return queryData;
	}

	/*
	 * takes a line and parses out the correct possible locations of the landmark for that line.
	 * returns a LocationPossibilities object as well as the associated landmark
	 */
	LocationPossibilities readGoldEntry(String line, List<String> landmarks) {
		String[] parts = line.split("\t");
		String[] locationParts = parts[2].split(",");
		String[] cities = locationParts[0].split("/");
		landmarks.add(parts[1].toLowerCase().trim());
		return new LocationPossibilities(Arrays.asList(cities), locationParts[1].toLowerCase().trim());
	}

	/*
	 * reads in a file containing data about the landmark and where it's located 
	 * returns a list of LocationPossibilities object as well as a list of landmarks. takes in
	 * the name of the gold file
	 */
	List<LocationPossibilities> readInGold(List<String> landmarks, String goldFile) {
		List<LocationPossibilities> goldData = new ArrayList<LocationPossibilities>();
		List<String> lines = new ArrayList<String>();
		try {
			BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(goldFile), "UTF8"));
			for(String line = reader.readLine(); line != null; line = reader.readLine()) {
				lines.add(line);
			}
			reader.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		for(String line : lines) {
			LocationPossibilities goldEntry = readGoldEntry(line, landmarks);
			goldData.add(goldEntry);
		}
		return goldData;
	}

	/*
	 * in this method, you must return Location object, where the first parameter of the constructor is the city where
	 * the landmark is located and the second parameter is the state or the country containing the city. 
	 * the return parameter is a Location object. if no good answer is found, returns a GoogleQuery object with
	 * empty strings as parameters
	 * 
	 * note that the method does not get passed the actual landmark being queried. you do not need this information,
	 * as your primary task in this method is to simply extract a guess for the location of the landmark given
	 * Google results. you can, however, extract the landmark name from the given queries if you feel that helps.
	 */
	Location guessLocation(List<GoogleQuery> data) {
		// TODO: use the GoogleQuery object for landmark to generate a tuple of the location
		// of the landmark
		return new Location("", "");
	}

	/*
	 * loops through each of the data associated with each query and passes it into the
	 * guessLocation method, which returns the guess of the user
	 */
	List<Location> processQueries(List<List<GoogleQuery>> queryData) {
		// TODO: this todo is optional. this is for anyone who might want to write any initialization code that should only be performed once.
		Location[] guesses = new Location[queryData.size()];
		for(int i = 0; i < queryData.size(); ++i) {
			guesses[i] = guessLocation(queryData.get(i));
		}
		return Arrays.asList(guesses);
	}

	/*
	 * prints out the results as described in the handout
	 */
	void printResults(List<Integer> correctCities, List<Integer> incorrectCities, List<Integer> noguessCities, List<Integer> correctCountries, List<Integer> incorrectCountries, List<Integer> noguessCountries, List<String> landmarks, List<Location> guesses, List<LocationPossibilities> gold) {
		System.out.println("LANDMARK\tYOUR GUESSED CITY\tCORRECT CITY/CITIES\tYOUR GUESSED COUNTRY\tCORRECT COUNTRY");
		Set<Integer> correctGuesses = new HashSet<Integer>(correctCities);
		correctGuesses.retainAll(new HashSet<Integer>(correctCountries));
		Set<Integer> noGuesses = new HashSet<Integer>(noguessCities); 
		noGuesses.addAll(new HashSet<Integer>(noguessCountries));
		Set<Integer> incorrectGuesses = new HashSet<Integer>(incorrectCities);
		correctGuesses.addAll(new HashSet<Integer>(incorrectCountries));
		System.out.println("=====CORRECT GUESSES=====");
		for(Integer i : correctGuesses) {
			System.out.println(landmarks.get(i) + '\t' + guesses.get(i).city + '\t' + gold.get(i).cities + '\t' + guesses.get(i).country + '\t' + gold.get(i).country);
		}
		System.out.println("=====NO GUESSES=====");
		for(Integer i : noGuesses) {
			System.out.println(landmarks.get(i) + '\t' + guesses.get(i).city + '\t' + gold.get(i).cities + '\t' + guesses.get(i).country + '\t' + gold.get(i).country);
		}
		System.out.println("=====INCORRECT GUESSES=====");
		for(Integer i : incorrectGuesses) {
			System.out.println(landmarks.get(i) + '\t' + guesses.get(i).city + '\t' + gold.get(i).cities + '\t' + guesses.get(i).country + '\t' + gold.get(i).country);
		}
		System.out.println("=====TOTAL SCORE=====");
		int correctTotal = correctCities.size() + correctCountries.size();
		int noguessTotal = noguessCities.size() + noguessCountries.size();
		int incorrectTotal = incorrectCities.size() + incorrectCountries.size();
		System.out.println("correct guesses: " + correctTotal);
		System.out.println("no guesses: " + noguessTotal);
		System.out.println("incorrect guesses: " + incorrectTotal);
		System.out.println("total score: " + (correctTotal - incorrectTotal) + " out of " + (correctTotal + noguessTotal + incorrectTotal));
	}

	/*
	 * takes a list of Location objects and prints a list of correct and incorrect answers as well as scores the results
	 */
	void scoreAnswers(List<Location> guesses, List<LocationPossibilities> gold, List<String> landmarks) {
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
		printResults(correctCities, incorrectCities, noguessCities, correctCountries, incorrectCountries, noguessCountries, landmarks, guesses, gold);
	}

	public static void main(String[] args) {
		String googleResultsFile = "../data/googleResults_tagged.txt"; // file where Google query results are read
		String goldFile = "../data/landmarks.txt"; // contains the results 
		Googling g = new Googling();
		List<List<GoogleQuery>> queryData = g.readInData(googleResultsFile);
		List<String> landmarks = new ArrayList<String>();
		List<LocationPossibilities> goldData = g.readInGold(landmarks, goldFile);
		List<Location> guesses = g.processQueries(queryData);
		g.scoreAnswers(guesses, goldData, landmarks);
	}

}
