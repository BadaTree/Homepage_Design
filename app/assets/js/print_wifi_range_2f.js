var sync_x_pos = 50;
var sync_y_pos = 206;

function show_wifi_range(min_x, max_x, min_y, max_y) {
    const container = document.getElementById("map_area");

    // ID가 "rec"인 요소를 찾고, 만약 존재한다면 제거합니다.
    const existingRectangle = document.getElementById("rec");
    if (existingRectangle) {
        container.removeChild(existingRectangle);
    }


    const rectangle = document.createElement("div");
    rectangle.id = "rec"

    rectangle.style.position = "absolute";
    rectangle.style.top = min_x + sync_x_pos + "px";
    rectangle.style.left = min_y + sync_y_pos + "px";
    rectangle.style.height = max_x-min_x + "px";
    rectangle.style.width = max_y-min_y + "px";
    rectangle.style.backgroundColor = "#FF0000";
    rectangle.style.opacity = 0.5;

    container.appendChild(rectangle);
}

function remove_rectangle(){
    const container = document.getElementById("map_area");

    // ID가 "rec"인 요소를 찾고, 만약 존재한다면 제거합니다.
    const existingRectangle = document.getElementById("rec");
    if (existingRectangle) {
        container.removeChild(existingRectangle);
    }
}