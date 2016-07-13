var ratcam;
var playing = false;

function setup() {
    createCanvas(640, 480);
    ratcam = createVideo(["/static/video/1467738431.mov"]);
    ratcam.size(640, 480);    
    ratcam.loop();
    ratcam.hide();
    ratcam.pause();
    ratcam.volume(1);
    button = createButton('play/pause');
    button.mousePressed(togglePlay);
}

function draw() {
    if (mouseIsPressed) {
        if (mouseY > 10 && mouseY < 20) {
            ratcam.time((mouseX/width) * ratcam.duration());
        }
    }

    image(ratcam, 0, 0);
    position = ratcam.time() / ratcam.duration();    

    // progress bar
    fill(255);    
    rect(0, 10, width, 10);
    fill(0);
    rect(0, 12, position * width, 6);
    textSize(8);
    text(ratcam.time(), width - 50, 18);            // format this

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