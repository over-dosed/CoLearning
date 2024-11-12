var socket = io.connect('http://127.0.0.1:8081', { port: 8081, rememberTransport: false });

let video;
let poses = [];

function preload() {
	// Load the bodyPose model
	// bodyPose = ml5.bodyPose();
  }

function setup() {
	createCanvas(1280, 960);

	// Create the video and hide it
	video = createCapture(VIDEO);
	video.size(640, 480);
	video.hide();

	// Start detecting poses in the webcam video
	// bodyPose.detectStart(video, gotPoses);

	setupOsc(12000, 4444);
}

function draw() {
	background(0, 0, 255);
	image(video, 0, 0, width/2, height/2);

	sendOsc('/body', mouseX);

	// Draw all the tracked landmark points
	if (poses.length == 0) {
		return;
	}
	// let pose = poses[0];
	// for (let j = 0; j < pose.keypoints.length; j++) {
	// 	let keypoint = pose.keypoints[j];
	// 	// Only draw a circle if the keypoint's confidence is bigger than 0.1
	// 	if (keypoint.confidence > 0.1) {
	// 	fill(0, 255, 0);
	// 	noStroke();
	// 	circle(keypoint.x, keypoint.y, 10);
	// 	circle(keypoint.x, keypoint.y + height/2, 10);
	// 	}
	// }
	// // console.log(pose);
	// let trainData = [pose.left_ear.x, pose.left_ear.y, pose.right_ear.x, pose.right_ear.y, pose.left_eye.x, pose.left_eye.y, pose.right_eye.x, pose.right_eye.y, pose.nose.x, pose.nose.y];
	// sendOsc('/landmark', trainData)
}

function receiveOsc(address, value) {
	if (address == '/landmark') {
		console.log("received OSC: " + address + ", " + value);
		return;
	}
}

function sendOsc(address, value) {
	console.log("send OSC: " + address + ", " + value);
	socket.emit('message', [address].concat(value));
}

function setupOsc(oscPortIn, oscPortOut) {
	socket.on('connect', function() {
		socket.emit('config', {
			server: { port: oscPortIn,  host: '127.0.0.1'},
			client: { port: oscPortOut, host: '127.0.0.1'}
		});
	});
	socket.on('message', function(msg) {
		if (msg[0] == '#bundle') {
			for (var i=2; i<msg.length; i++) {
				receiveOsc(msg[i][0], msg[i].splice(1));
			}
		} else {
			receiveOsc(msg[0], msg.splice(1));
		}
	});
}

// Callback function for when bodyPose outputs data
function gotPoses(results) {
	// Save the output to the poses variable
	poses = results;
}
