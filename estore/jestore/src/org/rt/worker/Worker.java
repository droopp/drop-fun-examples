package org.rt.worker;

import org.rt.worker.Actor;
import java.util.concurrent.*;


public class Worker{

    public static void main(String[] args) throws InterruptedException{

        Actor api = new Actor();
        BlockingQueue<String> queue = new LinkedTransferQueue<String>();

        //Thread t = new Thread(new Consumer(api, queue));
        //t.start();

        int num = 10;

        try{

            num = Integer.parseInt(args[1]);

        }catch(Exception e){}

        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(num);

        //start tasks
        for (int i = 1; i <= num; i++)
        {
            Consumer c = new Consumer(api, queue);
            executor.execute(c);
        }

        api.log("start worker");

        String msg = null;

        while(api.hasNext()){

            msg = api.read();

            if (msg.equals("")){
                executor.shutdownNow();
                break;

            }else if(msg.equals("stop_async_worker")){
                executor.shutdownNow();
                api.send(msg);
                break;

            }else{
                api.log("received msg: " + msg);
                queue.put(msg);

            }

        }

    }


}
