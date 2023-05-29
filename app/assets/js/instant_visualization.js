childeren_data = [{
    x: 0,
    y: 0,
    r: 10
},{
    x: 800,
    y: 800,
    r: 10
},{
    x: 400,
    y: 400,
    r: 50
},
{
    x: 200,
    y: 200,
    r: 10
}
]

var popData = {
    datasets: [{
        label: [],
        data: [],
        // backgroundColor: "#FF9966"
        backgroundColor: "rgba(255, 0, 0, 0.2)"
    },
        {
            label: [],
            data: [],
            // backgroundColor: "#9BD2E9"
            backgroundColor: "rgba(0, 255, 0, 0.2)"
        },
        {
            label: [],
            data: [],
            // backgroundColor: "#FF9966"
            backgroundColor: "rgba(0, 0, 255, 0.2)"
        },
    ]
};

var popCanvas = document.getElementById("popChart");

var bubbleChart = new Chart(popCanvas, {
    type: 'bubble',
    data: popData,
    options: {
        aspectRatio: 1,
        responsive: false,
        maintainAspectRation : false,
        animation:false,
        layout : {
            autoPadding : false
        },
        scales: {
            x: {
                min: 0,
                max: 800,
            },
            y: {
                min: 0,
                max: 800
            },

        },
        plugins : {
            tooltip: {
                enabled : false
            }
        }

    }
});


function print_children_position(data, idx=0, my_angle=0) {
    bubbleChart.data.datasets[idx].label = my_angle.toString()
    bubbleChart.data.datasets[idx].data = data
}
function chart_update() {
    bubbleChart.update()
}

function remove_children() {
    bubbleChart.data.datasets[0].data = []
    bubbleChart.data.datasets[1].data = []
    bubbleChart.data.datasets[2].data = []
    bubbleChart.update();
}
