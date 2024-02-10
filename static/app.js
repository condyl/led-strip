var socket = io();

// Event handler for new connections.
// The callback function is invoked when a connection with the
// server is established.
socket.on("connect", function () {
    socket.emit("my_event", { data: "I'm connected!" });
});

// Event handler for server sent data.
// The callback function is invoked whenever the server emits data
// to the client.
socket.on("my response", function (msg) {
    console.log(msg.data);
    document.getElementById("text").innerHTML = msg.data;
});

function colour(fromhtml) {
    socket.emit("colour", { data: fromhtml }); // send data to python file
    document.getElementById("colourtext").innerHTML =
        "current colour: " + fromhtml; // change "current colour" text on website to the updated colour
}

function fill() {
    socket.emit("fill", { data: "fill" }); // run fill_leds() function
}

function rainbow() {
    socket.emit("rainbow", { data: "rainbow" }); // run rainbow() function
    document.getElementById("colourtext").innerHTML = "current colour: rainbow"; // change "current colour" text on website to rainbow
}

function slider(value) {
    var output = document.getElementById("brightness");
    var slider = document.getElementById("myRange");
    output.innerHTML = "brightness: " + slider.value; // change brightness text to current brightness
    var step = slider.value;
    socket.emit("slider", { data: step }); // run slider function
}

function choosecolour(value) {
    var output = document.getElementById("colourtext");
    colour = document.getElementById("myColor").value;
    output.innerHTML = "current colour: " + value; // change current colour text
    socket.emit("choose", { data: colour }); // run choose function
}

function off() {
    socket.emit("off"); // run off function
}
