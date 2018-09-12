import java.io.File;

public class Main {

    public static void main(String[] args)
    {
        SmilesGrabber sg = new SmilesGrabber("E:/Development Project/Data/GNPS", 6);
        BitmapWriter bw = new BitmapWriter(sg.getSmilesList());

        bw.writeBitmap();
    }
}
