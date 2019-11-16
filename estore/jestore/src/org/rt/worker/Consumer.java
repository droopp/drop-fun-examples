package org.rt.worker;

import java.util.concurrent.*;
import org.json.*;


public class Consumer implements Runnable {

    private Actor api = null;
    private BlockingQueue<String> queue = null;

    public Consumer(Actor api, BlockingQueue<String> queue){
        this.api = api;
        this.queue = queue;

    }

    public void process(String msg){

        String[] parts = msg.split("::");

        try{

            JSONObject obj = new JSONObject(parts[1]);

            String uri = obj.getString("uri");
            JSONObject headers = obj.getJSONObject("headers");
            String method = obj.getString("method");
            JSONObject args = obj.getJSONObject("args");
            String data = obj.getString("data");

            String res = null;

            switch (method){
                case "get":
                    res = Handler.get(uri, headers, args, data);
                    break;
                case "post":
                    res = Handler.post(uri, headers, args, data);
                    break;
                case "put":
                    res = Handler.put(uri, headers, args, data);
                    break;
                case "patch":
                    res = Handler.patch(uri, headers, args, data);
                    break;
                case "delete":
                    res = Handler.delete(uri, headers, args, data);
                    break;
            }

            api.send(parts[0] + "::" + res);

        }catch (Exception e){

            String err = "{\"x_res_code\":500, \"x_res_body\":\"" + e.getMessage() + "\"}";

            api.send(parts[0] + "::" + new JSONObject(err));

        }

    }

    public void run(){

        try{

            String msg = null;

            while(true){

                msg = queue.take();
                long startTime = System.currentTimeMillis();

                api.log("received (" + Thread.currentThread().getName() + ") msg: " + msg);

                process(msg);

                api.log("message send: " + (System.currentTimeMillis() - startTime));

            }

        }catch (InterruptedException e){}

    }
}


