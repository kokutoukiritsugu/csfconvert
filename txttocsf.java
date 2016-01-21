import java.io.*;

public class txttocsf {
    public static void main(String[] args) {
        txttocsf itoc = new txttocsf();
        try {
            if (args.length == 2) {
                powered();
                itoc.processinfo();
                itoc.processFile(args[0], args[1]);
            } else {
                itoc.usage();
                powered();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void processinfo() {
        System.out.println("txttocsf converting...");
    }

    private void usage() {
        System.out.println("Usage:");
        System.out.println("txttocsf txtfile csffile");
        System.out.println();
    }

    public static void powered() {
        System.out.println("powered by litel");
    }

    public static byte[] encode(byte aByte[]) {
        byte temp[] = new byte[aByte.length];
        for (int i = 0; i < aByte.length; i++) {
            temp[i] = (byte) ~(aByte[i]);
        }
        return temp;
    }

    public static byte[] intTobyte(int aInt) {
        return new byte[]{
                (byte) aInt,
                (byte) (aInt >>> 8),
                (byte) (aInt >>> 16),
                (byte) (aInt >>> 24)
        };
    }

    private void processFile(String in, String out) throws IOException {
        InputStreamReader isr = new InputStreamReader(new BufferedInputStream(new FileInputStream(in)), "UTF-8");
        BufferedReader buffer = new BufferedReader(isr);
        DataOutputStream dis = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(out)));
        dis.writeBytes(" FSC");
        dis.write(intTobyte(3));
        dis.writeInt(0);
        dis.writeInt(0);
        dis.writeInt(0);
        dis.writeInt(0);

        String line;
        int count = 0;
        for (; (line = buffer.readLine()) != null; count++) {
            int id = 1;
            String type = "";
            String rtsStr = "";
            String str = "";
            String addFlagStr = "";
            if (line.equals("flag1")) {
                id = 1;
            }
            dis.writeBytes(" LBL");
            line = buffer.readLine();
            if (line.equals(" RTS")) {
                type = line;
                line = buffer.readLine();
                rtsStr = line;
                line = buffer.readLine();
                if (line.equals("strStart")) {
                    line = buffer.readLine();
                    str += line;
                    line = buffer.readLine();
                    while (!line.equals("strEnd")) {
                        str += "\n";
                        str += line;
                        line = buffer.readLine();

                    }
                }
            }
            if (line.equals("WRTS")) {
                type = line;
                line = buffer.readLine();
                rtsStr = line;
                line = buffer.readLine();
                if (line.equals("strStart")) {
                    line = buffer.readLine();
                    str += line;
                    line = buffer.readLine();
                    while (!line.equals("strEnd")) {
                        str += "\n";
                        str += line;
                        line = buffer.readLine();
                    }
                }
                line = buffer.readLine();
                addFlagStr = line;
            }

            dis.write(intTobyte(id));
            dis.write(intTobyte(rtsStr.length()));
            dis.writeBytes(rtsStr);
            dis.writeBytes(type);
            dis.write(intTobyte(str.length()));
            dis.write(encode(str.getBytes("UTF-16LE")));
            if (!addFlagStr.equals("")) {
                dis.write(intTobyte(addFlagStr.length()));
                dis.writeBytes(addFlagStr);
            }
        }
        dis.close();
        RandomAccessFile raf = new RandomAccessFile(out, "rw");
        raf.seek(8);
        raf.write(intTobyte(count));
        raf.seek(12);
        raf.write(intTobyte(count));
        raf.close();
    }
}
