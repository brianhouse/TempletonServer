var SERVER = "{{ server }}";
var VIDEOS = [{%- for video in videos -%}"{{ video }}", {%- endfor -%}]

var ratcam;
var playing = false;
var socket;
var socket_id;
var current_video;

function setup() {

    // socket = new WebSocket("ws://" + SERVER + "/displaysocket");
    // socket.onmessage = function (evt) {
    //     data = JSON.parse(evt.data);
    //     console.log(data);
    //     if ('socket_id' in data) {
    //         socket_id = data['socket_id'];
    //         console.log("--> received socket_id " + socket_id);
    //     }
    //     if ('rms' in data) {
    //         console.log('do stuff');
    //     }        
    // };

    setVideo(VIDEOS[0]);
    current_video = VIDEOS[0];

    var button = createButton("play/pause");
    button.mousePressed(togglePlay);
    button.parent("playpause");

    $('#timefield').click(function() {
        $(this).select();
    });

    var canvas = createCanvas(640, 480);
    canvas.parent("p5");    
}

function draw() {
    if (mouseIsPressed) {
        if (mouseY > 10 && mouseY < 20) {
            ratcam.time((mouseX/width) * ratcam.duration());
            $('#timefield').val(split(current_video, ".")[0] + " " + ratcam.time());
        }
    }

    image(ratcam, 0, 0);
    position = ratcam.time() / ratcam.duration();    

    // progress bar
    fill(255);    
    rect(0, 10, width, 10);
    fill(0);
    rect(0, 12, position * width, 6);
    // textSize(8);
    // text(ratcam.time(), width - 50, 18);            // util: format this

    // update
    if (playing) {
        $('#timefield').val(split(current_video, ".")[0] + " " + ratcam.time());
    }

    // border
    noFill();    
    rect(0, 0, 639, 479);         

    // console.log(ratcam.time() + "s " + floor((ratcam.time() / ratcam.duration()) * 100.0) + "%")
}

function togglePlay() {
    if (!playing) {
        ratcam.play();
        playing = true;
    } else {
        ratcam.pause();
        playing = false;
    }
}

function setVideo(filename) {
    if (ratcam != undefined) {
        ratcam.stop();
        loadImage("/static/img/loading.jpg", function(img) {
            image(img, 0, 0);
        });
        ratcam.src = ["/static/video/" + filename];       
        // console.log("Loading " +  "https://s3.amazonaws.com/{{ s3_bucket }}/" + filename);
        // ratcam.src = ["https://s3.amazonaws.com/{{ s3_bucket }}/" + filename];        
    } else {
        ratcam = createVideo(["/static/video/" + filename]);
        // console.log("Loading " +  "https://s3.amazonaws.com/{{ s3_bucket }}/" + filename);
        // ratcam = createVideo(["https://s3.amazonaws.com/{{ s3_bucket }}/" + filename]);
    }
    ratcam.size(640, 480);    
    ratcam.loop();
    ratcam.hide();
    ratcam.pause();
    ratcam.volume(1);
}

