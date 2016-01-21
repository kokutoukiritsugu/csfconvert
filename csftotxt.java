import java.io.*;

public class csftotxt {
    private static void processFile(String in, String out) {
        try {
            int CountNum = byteToint((getbybyte(in, 8, 4)));
            int offset = 24;
            PrintWriter w = new PrintWriter(new OutputStreamWriter(new FileOutputStream(out), "UTF-8"));
            for (int i = 0; i < CountNum; i++) {
                if ((new String(getbybyte(in, offset, 4))).equals(" LBL")) {
                    offset += 4;
                    int FlagNum = byteToint(getbybyte(in, offset, 4));
                    offset += 4;
                    int FlagStrLen = byteToint((getbybyte(in, offset, 4)));
                    offset += 4;
                    String FlagStr = new String(getbybyte(in, offset, FlagStrLen));
                    offset += FlagStrLen;
                    String rtsStr = new String(getbybyte(in, offset, 4));
                    if (rtsStr.equals(" RTS")) {
                        offset += 4;
                        int Strlen = (byteToint(getbybyte(in, offset, 4)));
                        offset += 4;
                        String Str = convertU16toANSI(decode(getbybyte(in, offset, Strlen * 2)));
                        if (Str.equals("")) {
                            Str = "";
                        }
                        String string = "flag" + FlagNum + "\n" + rtsStr + "\n" + FlagStr + "\n" + "strStart" + "\n" + Str + "\n" + "strEnd";

                        w.println(string);
                        offset += Strlen * 2;
                    }
                    if (rtsStr.equals("WRTS")) {
                        offset += 4;
                        int Strlen = (byteToint(getbybyte(in, offset, 4)));
                        offset += 4;
                        String Str = convertU16toANSI(decode(getbybyte(in, offset, Strlen * 2)));
                        if (Str.equals("")) {
                            Str = "";
                        }
                        offset += Strlen * 2;
                        int addFlaglen = (byteToint(getbybyte(in, offset, 4)));
                        offset += 4;
                        String addFlagStr = new String(getbybyte(in, offset, addFlaglen));
                        String string = "flag" + FlagNum + "\n" + rtsStr + "\n" + FlagStr + "\n" + "strStart" + "\n" + Str + "\n" + "strEnd" + "\n" + addFlagStr;
                        w.println(string);
                        offset += addFlaglen;
                    }
                }
            }
            w.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static byte[] decode(byte aByte[]) {
        byte temp[] = new byte[aByte.length];
        for (int i = 0; i < aByte.length; i++) {
            temp[i] = (byte) ((~aByte[i]) & 0xff);
        }
        return temp;
    }

    public static byte[] getbybyte(String filename, long offset, int strlen) throws IOException {
        byte buffer[] = new byte[strlen];
        FileInputStream fis = new FileInputStream(filename);
        if (fis.skip(offset) == -1) {
            throw new IOException();
        }
        if ((fis.read(buffer, 0, strlen)) == -1) {
            throw new IOException();
        }
        fis.close();
        return buffer;
    }

    public static String convertU16toANSI(byte[] strbyte) throws UnsupportedEncodingException {
        return new String(strbyte, "UTF-16LE");
    }

    public static int byteToint(byte aByte[]) {
        return ((aByte[3] & 0xff) << 24) |
                ((aByte[2] & 0xff) << 16) |
                ((aByte[1] & 0xff) << 8) |
                ((aByte[0] & 0xff));
    }

    public static void main(String[] args) {
        if (args.length == 2) {
            powered();
            processinfo();
            processFile(args[0], args[1]);
        } else {
            usage();
            powered();
        }
    }

    private static void processinfo() {
        System.out.println("csftotxt converting...");
    }

    private static void usage() {
        System.out.println("Usage:");
        System.out.println("csftotxt csffile txtfile");
        System.out.println();
    }

    public static void powered() {
        System.out.println("powered by litel");
    }

}
