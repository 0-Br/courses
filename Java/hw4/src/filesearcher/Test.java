package filesearcher;
import testutil.TestRunner;


public class Test {
	public static void main(String[] args) {
		TestRunner.enableException(true);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "we");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+35);
			if (ans==35) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "google");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+0);
			if (ans==0) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "19th");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+5);
			if (ans==5) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "27");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+5);
			if (ans==5) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "i");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+193);
			if (ans==193) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "USD");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+2);
			if (ans==2) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "grimacing");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+1);
			if (ans==1) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "3900");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+1);
			if (ans==1) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		TestRunner.runTest(()->{
			String inputFile = "C:\\Users\\Liu Binrui\\OneDrive\\Cloud\\Codes\\Java\\hw4\\data\\dialog.txt";
			int ans = FileSearcher.search(inputFile, "September");
			System.out.println("Ans: "+ans);
			System.out.println("Expected: "+13);
			if (ans==13) System.out.println("Accept");
			else System.out.println("Wrong Answer");
		},1000);

		System.exit(0);
	}
}

