//
// Nodejs example actor
// 

var readline = require('readline');

var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false

});

//API

function log(m){
    console.error(Date.now() + ": " + m);
}

function send(m){
   console.log(m);
}



//Process - actor
// line - recieve message from world
// send - send message to world
// log  -  logging anything


rl.on('line', function(line){

    msg = line.replace(/\n$/, '')

    log("get message: " + msg);



    try{

        msg0 = msg.split(",")
        count = msg0[2].split(" ")

        if (count.length > process.argv[2]){
            
            send("tag:exist," + msg0.slice(1))

        }else{
        
            send("" + msg0.slice(1))

        }

    }catch(e){

        log(e)
        send(msg)
    
    }

 
 })
