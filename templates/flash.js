var isFull = false;

document.body.onkeyup = function (e) {
    if (e.keyCode == 27) {
        if (isFull) {
            exitFullScreen();
        }
    }
};

function requestFullScreen(element) {
    var requestMethod = element.requestFullscreen || 
                        element.webkitRequestFullscreen || 
                        element.mozRequestFullScreen || 
                        element.msRequestFullscreen;

    if (requestMethod) {
        requestMethod.call(element);
        updateCanvasHeight();
    } else if (typeof window.ActiveXObject !== "undefined") {
        var wscript = new ActiveXObject("WScript.Shell");
        if (wscript !== null) {
            wscript.SendKeys("{F11}");
        }
    }
}

function exitFullScreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
    }
    isFull = false;
}

var canvas = document.getElementById('hello');

function makeFullScreen() {
    isFull = true;
    requestFullScreen(canvas);
}

function updateCanvasHeight() {
    let hh = window.innerHeight;
    document.getElementById('game').height = hh;
}

updateCanvasHeight();

window.onresize = function (event) {
    updateCanvasHeight();
};

var textElement = document.getElementById("game");
var currentUrl = new URL(window.location.href);
if (currentUrl.searchParams.has("game")) {
    textElement.src = currentUrl.searchParams.get("game");
}