var client = null;

// Connect to the MQTT broker
function connect() {
  // Replace "test.mosquitto.org" with the hostname or IP address of your MQTT broker
  client = new Paho.MQTT.Client("test.mosquitto.org", 8080, "web_" + parseInt(Math.random() * 100, 10));

  // Set callback handlers
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;

  // Connect to the MQTT broker
  client.connect({
    onSuccess: onConnect,
    onFailure: onFailure,
    useSSL: true,
    userName: "",
    password: ""
  });
}

// Handle connection established event
function onConnect() {
  console.log("Connected to MQTT broker");

  // Subscribe to a topic
  // Replace "test/topic" with the topic you want to subscribe to
  client.subscribe("test/topic");
}

// Handle connection lost event
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("Connection lost: " + responseObject.errorMessage);
  }
}

// Handle message arrived event
function onMessageArrived(message) {
  console.log("Message received: " + message.payloadString);

  // Display the message on the web page
  var messages = document.getElementById("messages");
  messages.innerHTML += "<p>" + message.destinationName + ": " + message.payloadString + "</p>";
}

// Handle connection failure event
function onFailure(responseObject) {
  console.log("Failed to connect to MQTT broker: " + responseObject.errorMessage);
}

// Publish a message to a topic
function publish() {
  var topic = document.getElementById("topic").value;
  var message = document.getElementById("message").value;

  if (client.isConnected()) {
    var message = new Paho.MQTT.Message(message);
    message.destinationName = topic;
    client.send(message);
  } else {
    console.log("Not connected to MQTT broker");
  }
}

// Subscribe to a topic
function subscribe() {
  var topic = document.getElementById("topic").value;

  if (client.isConnected()) {
    client.subscribe(topic);
  } else {
    console.log("Not connected to MQTT broker");
  }
}

// Unsubscribe from a topic
function unsubscribe() {
  var topic = document.getElementById("topic").value;

  if (client.isConnected()) {
    client.unsubscribe(topic);
  } else {
    console.log("Not connected to MQTT broker");
  }
}

// Connect to the MQTT