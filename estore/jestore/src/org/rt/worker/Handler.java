package org.rt.worker;

import org.json.*;


public class Handler{

    public static final String get(String uri, JSONObject headers, JSONObject args, String data){
    
        return "1";
    
    }

    public static final String post(String uri, JSONObject headers, JSONObject args, String data){
    
        return "2";
    
    }

    public static final String put(String uri, JSONObject headers, JSONObject args, String data){
 
        return "3";
    
    }

    public static final String patch(String uri, JSONObject headers, JSONObject args, String data){
    
        return "4";
    
    }

    public static final String delete(String uri, JSONObject headers, JSONObject args, String data){
   
        return "5";
    
    }







}


