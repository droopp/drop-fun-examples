package org.rt.worker;

import org.rt.worker.Actor;
import java.util.concurrent.*;


public class Worker{

    public static void main(String[] args) throws InterruptedException{

        Actor api = new Actor();
        BlockingQueue<String> queue = new LinkedTransferQueue<String>();

        int num = 10;

        try{

            num = Integer.parseInt(args[1]);

        }catch(Exception e){}

        //start producer
        Thread t0 = new Thread(new Producer(api, queue));
        t0.start();

        //start tasks
        for (int i = 1; i <= num; i++)
        {
            Thread t = new Thread(new Consumer(api, queue));
            t.start();

        }

    }


}
