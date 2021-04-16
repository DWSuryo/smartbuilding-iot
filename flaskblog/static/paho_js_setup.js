var mqtt;
var reconnectTimeout = 2000;

//var host="localhost";
var host="mqtt.lunar-smart.com";
//var host=document.domain;
var port=8083;                      //MQTT over WebSockets
//var port=location.port;
var username="lunar";
var password="smartsystem";

function onConnect() {
    // Once a connection has been made, make a subscription and send a message.

    console.log("Connected ");
    //mqtt.subscribe("sensor1");
    message = new Paho.MQTT.Message("Hello World");
    message.destinationName = "45856/status";
    mqtt.send(message);
}
function MQTTconnect() {
    console.log("connecting to "+ host +" "+ port);
    var x=Math.floor(Math.random() * 10000); 
    var cname="orderform-"+x;
    mqtt = new Paho.MQTT.Client(host,port,cname);
    //document.write("connecting to "+ host+'/'+port+'/'+cname);
    var options = {
        uname: username,
        pass: password,
        timeout: 3,
        onSuccess: onConnect,
    };
    
    mqtt.connect(options); //connect
}
