var Config = {};

//base:
Config.debug = false;
Config.framerate = 60;

//piece:
Config.bgColor = '#fff';
Config.colorPairs = [
	["#0000FF","#00FFFF"],
	["#FF8AFF","#00FFFF"],
	["#FF00DF","#FFFF00"],
	["#FF00FF","#00FF00"],
	["#FF0000","#FFB3FF"],
	["#0000FF","#FF0000"]
]

Config.size = .18;//relative to smallest dimension
Config.offset = .0025;//offset per frame, relative to window diagonal

Config.margin = -.04;//relative to smallest dimension

Config.bounceRandomAngle = 25;//in degrees, max random change in angle when bouncing

Config.circlesPerFrame = 24;

Config.resetOnResume = true;

Config.desktopWidth = 100;
Config.mobileWidth = 50;
