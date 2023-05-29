 var sync_x_pos = 50;
 var sync_y_pos = 206;
//var sync_x_pos = 45;
//var sync_y_pos = 233;
var sync_circle_x = sync_x_pos-26;
var sync_circle_y = sync_y_pos-25;
var dot_num = 200;
var children_num = 2000;
var positions = [];

// 미리 점 찍어두기
for (var i=0; i<dot_num; i++) {
    positions.push([-1000, -1000, 1]);
    $("#map_area").append(`<img class="dot red ${i}" src="./images/dot.png"/>`).trigger("create");
}



function show_my_position(x_pos, y_pos, matching_level=3) {
    // document.getElementById("map_img").width = 840 // ???
    positions.pop(); // 배열의 가장 마지막값 삭제
    positions.unshift([x_pos, y_pos, matching_level]); // 배열의 가장 처음에 값 추가
    console.log(positions)
    for (var i = dot_num-1; i >= 0; i--) {
        var dot = $(`.dot.red.${i}`)[0]
        switch (positions[i][2]) {
            case 1:
                dot.src = "./images/dot.png"
                console.log("OK")
                break;
            case 2:
                dot.src = "./images/doty.png"
                break;
            case 3:
                dot.src = "./images/dotb.png"
                break;
        }
        dot.style.top = `${positions[i][0] + sync_x_pos}px`
        dot.style.left = `${positions[i][1] + sync_y_pos}px`
        dot.style.opacity = `${1.0 - (i / (dot_num-1))}`
    }

    // 매칭 레벨 보여주기
//    show_matching_level(x_pos, y_pos, matching_level);

    // 현재 위치 중심으로 맵 움직이기
    // moving_map(x_pos, y_pos);
}

function show_PDR_position(x_pos, y_pos) {
    $("#map_area").append(`<img class="dot yellow" src="./images/doty.png" style="top:${x_pos + sync_x_pos}px; left:${y_pos + sync_y_pos}px" />`).trigger("create");
}


function show_matching_level (x_pos, y_pos, matching_level) {
    var circleUI = $("#circle")[0]
    circleUI.style.top = `${x_pos + sync_circle_x}px`
    circleUI.style.left = `${y_pos + sync_circle_y}px`
    switch (matching_level) {
        case 0:
            circleUI.src = "./images/circle_red.png";
            break;
        case 1:
            circleUI.src = "./images/circle_red.png";
            break;
        case 2:
            circleUI.src = "./images/circle_green.png";
            break;
        case 3:
            circleUI.src = "./images/circle_blue.png";
            break;
    }
}

// 현재 위치 중심으로 맵 움직이기
var moving_map = function (x_pos, y_pos) {
    var center_x = 500;
    var center_y = -380;
    var elem = $("#map_area")[0]
    elem.style.left = `${center_x - yPosition2}px`;
    elem.style.top = `${center_y + xPosition2}px`;
}

// Instant Particle 시각화
function show_all_children (pos_list) {
    var num = 0
    for (var pos of pos_list) {
        var child = $(`.children.${num}`)[0]
        child.style.top = pos[0]+sync_x_pos;
        child.style.left = pos[1]+sync_y_pos;
        num += 1
    }
    for (var i=num; i<2000; i++) {
        var child = $(`.children.${i}`)[0]
        child.style.top = -1000;
        child.style.left = -1000;
    }
}

// 이동방향 시각화
function arrow_rotation (angle) {
    var arrow = $("#arrow")[0]
    arrow.style.left = `${positions[0][1] + 213}px`
    arrow.style.top = `${positions[0][0] + 40}px`
    arrow.style.transformOrigin = `${-3}px ${15}px`
    arrow.style.transform = `rotate(${angle}deg)`
}