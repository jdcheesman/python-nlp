import static org.junit.Assert.*;

import org.junit.Test;


public class FeatureFactoryTest {

	final String capitals = "THIS";
	final String mixed1 = "tHis";
	final String mixed2 = "tHiS";
	final String mixed3 = "tHIS";
	final String title = "This";
	final String lower = "this";
	
	final String allNumeric = "1234";
	final String mixedNumeric = "thi5";
	
	final String weird = "th.s";
	
	@Test
	public void testGetCharsFeatureCapitals() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Capitals";
		String actual = ff.getCharsFeature(capitals);
		assertEquals(expected, actual);
	}

	@Test
	public void testGetCharsFeatureMixed1() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Mixed";
		String actual = ff.getCharsFeature(mixed1);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsFeatureMixed2() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Mixed";
		String actual = ff.getCharsFeature(mixed2);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsFeatureMixed3() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Mixed";
		String actual = ff.getCharsFeature(mixed3);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsFeatureTitle() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Title";
		String actual = ff.getCharsFeature(title);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsFeatureLower() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Lower";
		String actual = ff.getCharsFeature(lower);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsAllNumeric() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Numeric";
		String actual = ff.getCharsFeature(allNumeric);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsMixedNumeric() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=MixedNumeric";
		String actual = ff.getCharsFeature(mixedNumeric);
		assertEquals(expected, actual);
	}
	
	@Test
	public void testGetCharsWeird() {
		FeatureFactory ff = new FeatureFactory();
		String expected = "case=Weird";
		String actual = ff.getCharsFeature(weird);
		assertEquals(expected, actual);
	}

}
