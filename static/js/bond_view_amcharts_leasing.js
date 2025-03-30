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
  min: 1,
  max: 2,
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

  label1.set("text", DebtCoverage.toString());

  clockHand1.pin.animate({ key: "fill", to: fill, duration: 100, easing: am5.ease.out(am5.ease.cubic) })
  clockHand1.hand.animate({ key: "fill", to: fill, duration: 100, easing: am5.ease.out(am5.ease.cubic) })
});

setInterval(function () {
  axisDataItem1.animate({
    key: "value",
    to: Math.min(Math.max(DebtCoverage, 1), 2),
    duration: 500,
    easing: am5.ease.out(am5.ease.cubic)
  });
}, 2000)

chart1.bulletsContainer.set("mask", undefined);


// Create axis ranges bands
// https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Bands
var bandsData1 = [{

  color: "#EB484D",
  lowScore: 1,
  highScore: 1.2,
}, {
  color: "#73C469",
  lowScore: 1.2,
  highScore: 1.4
}, {
  color: "#3CA969",
  lowScore: 1.4,
  highScore: 1.6
},{
  color: "#73C469",
  lowScore: 1.6,
  highScore: 1.8
}, {

  color: "#F5EF3D",
  lowScore: 1.8,
  highScore: 2
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



var root2 = am5.Root.new("amchartdiv2");


root2.setThemes([
  am5themes_Animated.new(root2)
]);


var chart2 = root2.container.children.push(am5radar.RadarChart.new(root2, {
  panX: false,
  panY: false,
  startAngle: 160,
  endAngle: 380
}));


var axisRenderer2 = am5radar.AxisRendererCircular.new(root2, {
  innerRadius: -30
});

axisRenderer2.grid.template.setAll({
  stroke: root2.interfaceColors.get("background"),
  visible: true,
  strokeOpacity: 0.8
});

var xAxis2 = chart2.xAxes.push(am5xy.ValueAxis.new(root2, {
  maxDeviation: 0,
  min: 0,
  max: 25,
  strictMinMax: false,
  renderer: axisRenderer2
}));


// Add clock hand
// https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Clock_hands
var axisDataItem2 = xAxis2.makeDataItem({});

var clockHand2 = am5radar.ClockHand.new(root2, {
  pinRadius: am5.percent(20),
  radius: am5.percent(90),
  bottomWidth: 40
})

var bullet2 = axisDataItem2.set("bullet", am5xy.AxisBullet.new(root2, {
  sprite: clockHand2
}));

xAxis2.createAxisRange(axisDataItem2);

var label2 = chart2.radarContainer.children.push(am5.Label.new(root2, {
  fill: am5.color(0xffffff),
  centerX: am5.percent(50),
  textAlign: "center",
  centerY: am5.percent(50),
  fontSize: "1.5em"
}));

axisDataItem2.set("value", 50);
bullet2.get("sprite").on("rotation", function () {
  var value = axisDataItem2.get("value");
  var text = Math.round(axisDataItem2.get("value")).toString();
  var fill = am5.color(0x000000);
  xAxis2.axisRanges.each(function (axisRange) {
    if (value >= axisRange.get("value") && value <= axisRange.get("endValue")) {
      fill = axisRange.get("axisFill").get("fill");
    }
  })

  label2.set("text", EquityLevel.toString() + '%');

  clockHand2.pin.animate({ key: "fill", to: fill, duration: 100, easing: am5.ease.out(am5.ease.cubic) })
  clockHand2.hand.animate({ key: "fill", to: fill, duration: 100, easing: am5.ease.out(am5.ease.cubic) })
});

setInterval(function () {
  axisDataItem2.animate({
    key: "value",
    to: Math.min(Math.max(EquityLevel, 0), 25),
    duration: 500,
    easing: am5.ease.out(am5.ease.cubic)
  });
}, 2000)

chart2.bulletsContainer.set("mask", undefined);


// Create axis ranges bands
// https://www.amcharts.com/docs/v5/charts/radar-chart/gauge-charts/#Bands
var bandsData2 = [{

  color: "#EB484D",
  lowScore: 0,
  highScore: 8,
}, {

  color: "#F5EF3D",
  lowScore: 8,
  highScore: 16
}, {


  color: "#3CA969",
  lowScore: 16,
  highScore: 25
}, ];

am5.array.each(bandsData2, function (data) {
  var axisRange = xAxis2.createAxisRange(xAxis2.makeDataItem({}));

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
    fill: root2.interfaceColors.get("background")
  });
});


// Make stuff animate on load
chart2.appear(1000, 100);





});