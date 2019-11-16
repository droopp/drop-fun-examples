package org.rt.worker;

import java.io.*;
import java.util.Scanner;

public class Actor{

    private Scanner s = null;

    public Actor(){
        s = new Scanner(System.in);
    }

    public Boolean hasNext(){
        return s.hasNextLine();
    }

    public String read(){
        return s.nextLine().replaceAll("\tncm\t", "\n");
    }

    public void send(String msg){
        System.out.println(msg.replaceAll("\n", "\tncm\t"));
    }

    public void log(String msg){
        System.err.println(System.currentTimeMillis() + " : " + msg);
    }

}


