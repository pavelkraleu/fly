var colorsRedtoGreen = [
  "#FF0000",
  "#FFCC00",
  "#33CC33"
]

var colorsGreenToRed = [
  "#33CC33",
  "#FFCC00",
  "#FF0000"
]

var colorsGreen = [
  "#33CC33",
  "#33CC33",
  "#33CC33"
]


  var gauge_voltage = new JustGage({
    id: "gauge_voltage",
    value: 0,
    min: 10,
    max: 16.8,
    title: "Voltage (V)",
    levelColorsGradient: false,
    levelColors : colorsRedtoGreen
  });

  var gauge_current = new JustGage({
    id: "gauge_current",
    value: 0,
    min: 0,
    max: 70,
    title: "Current (A)",
    levelColorsGradient: false,
    levelColors : colorsRedtoGreen
  });

  var gauge_battery_remaining = new JustGage({
    id: "gauge_battery_remaining",
    value: 0,
    min: 0,
    max: 100,
    title: "Battery remaining (%)",
    levelColorsGradient: false,
    levelColors : colorsRedtoGreen
  });

  var gauge_satellites_visible = new JustGage({
    id: "gauge_satellites_visible",
    value: 0,
    min: 0,
    max: 10,
    title: "GPS satellites",
    levelColorsGradient: false,
    levelColors : colorsRedtoGreen
  });

  var gauge_altitude = new JustGage({
    id: "gauge_altitude",
    value: 0,
    min: 0,
    max: 10,
    title: "Altitude (m)",
    levelColorsGradient: false,
    levelColors : colorsGreen
  });

  var gauge_climb = new JustGage({
    id: "gauge_climb",
    value: 0,
    min: 0,
    max: 5,
    title: "Climb (m/s)",
    levelColorsGradient: false,
    levelColors : colorsGreenToRed
  });

  var gauge_pitch = new JustGage({
    id: "gauge_pitch",
    value: 0,
    min: 0,
    max: 5,
    title: "Pitch (deg/s)",
    levelColorsGradient: false,
    levelColors : colorsGreenToRed
  });

  var gauge_yaw = new JustGage({
    id: "gauge_yaw",
    value: 0,
    min: 0,
    max: 5,
    title: "Yaw (deg/s)",
    levelColorsGradient: false,
    levelColors : colorsGreenToRed
  });

  var gauge_roll = new JustGage({
    id: "gauge_roll",
    value: 0,
    min: 0,
    max: 5,
    title: "Roll (deg/s)",
    levelColorsGradient: false,
    levelColors : colorsGreenToRed
  });

  var gauge_camera_fps = new JustGage({
    id: "gauge_camera_fps",
    value: 0,
    min: 0,
    max: 30,
    title: "FPS",
    levelColorsGradient: false,
    levelColors : colorsRedtoGreen
  });
