var clicked_x = 0
var clicked_y = 0
var setting_angle = -1
const isTouchDevice = (navigator.maxTouchPoints || 'ontouchstart' in document.documentElement);

// Mozilla, Opera, Webkit
if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", function () {
        document.removeEventListener("DOMContentLoaded", arguments.callee, false);
        domReady(isTouchDevice);
    }, false);
}

//DOM이 모두 로드 되었을 때
function domReady (is_touch_device) {
    var map_img = document.getElementById("map_img")

    // 스마트폰 터치 이벤트
    if (is_touch_device) {
        map_img.addEventListener('touchstart', function(event) {

            var x = event.pageX - this.offsetLeft;
            var y = event.pageY - this.offsetTop;
            var touch = undefined

            if (event.touches) {
                touch = event.touches[0]
                x = touch.pageX - this.offsetLeft;
                y = touch.pageY - this.offsetTop;
            }

            var plusUI = document.getElementById("X");
            plusUI.style = "position:absolute; z-index:2; left:"+(x-230)+"px; top:"+(y-870)+"px; display:block; pointer-events: none";
            var result_x = Number(plusUI.style.top.replace("px", ""))-48
            var result_y = Number(plusUI.style.left.replace("px", ""))-205
            console.log(result_x, result_y, "!!!")
            clicked_x = result_x
            clicked_y = result_y
            print_setting_angle(setting_angle)
        });
    }

    else {
        // PC 클릭 이벤트
        $("#map_img").on("click", function(event) {
            console.log("Hii!!!!");
            var x = event.pageX - this.offsetLeft;
            var y = event.pageY - this.offsetTop;
            var plusUI = document.getElementById("X");
            plusUI.style = "position:absolute; z-index:2; left:"+(x-230)+"px; top:"+(y-870)+"px; display:block; pointer-events: none";
            var result_x = Number(plusUI.style.top.replace("px", ""))-48
            var result_y = Number(plusUI.style.left.replace("px", ""))-205
            console.log(result_x, result_y)
            clicked_x = result_x
            clicked_y = result_y
            print_setting_angle(setting_angle)
        });
    }




}
var clicked_pos = function () {
    return clicked_x + "\t" + clicked_y
}
function set_angle(angle) {
    setting_angle = angle
    print_setting_angle()
}
function print_setting_angle() {
    if (setting_angle == -1)
        return
    var arrow = $("#arrow")[0]
    arrow.style.left = `${clicked_y + 215}px`
    arrow.style.top = `${clicked_x + 40}px`
    arrow.style.transformOrigin = `${-3}px ${15}px`
    arrow.style.transform = `rotate(${setting_angle}deg)`
}


