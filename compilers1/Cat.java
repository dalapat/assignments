
import java.io.IOException; 

public class Cat {
    public static void main(String[] args) throws IOException{
        int ch;
	while ((ch = System.in.read ()) != -1)
	    System.out.write(ch);
	System.out.flush();
    }
}
