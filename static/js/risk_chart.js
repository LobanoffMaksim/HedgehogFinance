am5.ready(function() {

var root1 = am5.Root.new("amchartdiv1");


root1.setThemes([
  am5themes_Animated.new(root1)
]);


var chart1 = root1.container.children.push(am5radar.RadarChart.new(root1, {
  panX: false,
  panY: false,
  startAngle: 160,
  endAngle: 380
}));


var axisRenderer1 = am5radar.AxisRendererCircular.new(root1, {
  innerRadius: -30
});

axisRenderer1.grid.template.setAll({
  stroke: root1.interfaceColors.get("background"),
  visible: true,
  strokeOpacity: 0.8
});

var xAxis1 = chart1.xAxes.push(am5xy.ValueAxis.new(root1, {
  maxDeviation: 0,
  min: 0,
  max: 10,
  strictMinMax: false,
  renderer: axisRenderer1
}));


// Add clock hand
// https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Clock_hands
var axisDataItem1 = xAxis1.makeDataItem({});

var clockHand1 = am5radar.ClockHand.new(root1, {
  pinRadius: am5.percent(20),
  radius: am5.percent(90),
  bottomWidth: 40
})

var bullet1 = axisDataItem1.set("bullet", am5xy.AxisBullet.new(root1, {
  sprite: clockHand1
}));

xAxis1.createAxisRange(axisDataItem1);

var label1 = chart1.radarContainer.children.push(am5.Label.new(root1, {
  fill: am5.color(0xffffff),
  centerX: am5.percent(50),
  textAlign: "center",
  centerY: am5.percent(50),
  fontSize: "1.5em"
}));

axisDataItem1.set("value", 50);
bullet1.get("sprite").on("rotation", function () {
  var value = axisDataItem1.get("value");
  var text = Math.round(axisDataItem1.get("value")).toString();
  var fill = am5.color(0x000000);
  xAxis1.axisRanges.each(function (axisRange) {
    if (value >= axisRange.get("value") && value <= axisRange.get("endValue")) {
      fill = axisRange.get("axisFill").get("fill");
    }
  })

  label1.set("text", level);

  clockHand1.pin.animate({ key: "fill", to: fill, duration: 100, easing: am5.ease.out(am5.ease.cubic) })
  clockHand1.hand.animate({ key: "fill", to: fill, duration: 100, easing: am5.ease.out(am5.ease.cubic) })
});

setInterval(function () {
  axisDataItem1.animate({
    key: "value",
    to: Math.min(Math.max(level, 0), 10),
    duration: 500,
    easing: am5.ease.out(am5.ease.cubic)
  });
}, 2000)

chart1.bulletsContainer.set("mask", undefined);


// Create axis ranges bands
// https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Bands
var bandsData1 = [{

  color: "#3CA969",
  lowScore: 0,
  highScore: 3,
}, {

  color: "#73C469",
  lowScore: 3,
  highScore: 5
}, {

  color: "#F5EF3D",
  lowScore: 5,
  highScore: 7
}, {

  color: "#FDBE47",
  lowScore: 7,
  highScore: 8
}, {

  color: "#EE6A4B",
  lowScore: 8,
  highScore: 9
}, {

  color: "#EB484D",
  lowScore: 9,
  highScore: 10
}, ];

am5.array.each(bandsData1, function (data) {
  var axisRange = xAxis1.createAxisRange(xAxis1.makeDataItem({}));

  axisRange.setAll({
    value: data.lowScore,
    endValue: data.highScore
  });

  axisRange.get("axisFill").setAll({
    visible: true,
    fill: am5.color(data.color),
    fillOpacity: 0.8
  });

  axisRange.get("label").setAll({
    text: data.title,
    inside: true,
    radius: 20,
    fontSize: "0.8em",
    fill: root1.interfaceColors.get("background")
  });
});


// Make stuff animate on load
chart1.appear(1000, 100);