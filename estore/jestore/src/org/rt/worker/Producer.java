package org.rt.worker;

import java.util.concurrent.*;
import org.json.*;


public class Producer implements Runnable {

    private Actor api = null;
    private BlockingQueue<String> queue = null;

    public Producer(Actor api, BlockingQueue<String> queue){
        this.api = api;
        this.queue = queue;

    }

    public void run(){

        try{

            api.log("start worker");

            String msg = null;

            while(api.hasNext()){

                msg = api.read();

                if(msg.equals("")){
                    System.exit(0);

                }else if(msg.equals("stop_async_worker")){

                    api.send(msg);
                    System.exit(0);

                }else{
                    api.log("received msg: " + msg);
                    queue.put(msg);
                }

            }


        }catch (InterruptedException e){
            System.exit(0);
        }

    }
}


