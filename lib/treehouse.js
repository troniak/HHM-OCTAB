window.onload = function() {

	// Video
	var video = document.getElementById("video");

	// Buttons
	var playButton = document.getElementById("play-pause");
	var muteButton = document.getElementById("mute");
	var fullScreenButton = document.getElementById("full-screen");
	var stepForwardButton = document.getElementById("step-forward");
	var stepBackButton = document.getElementById("step-back");

	// Sliders
	var seekBar = document.getElementById("seek-bar");
	var seekBar2 = document.getElementById("seek-bar2");
	var volumeBar = document.getElementById("volume-bar");

    //playback
    var start_time = 5;
    var end_time = 10;

    video.currentTime = start_time;

	// Event listener for the play/pause button
	playButton.addEventListener("click", function() {
		if (video.paused == true) {
			// Play the video
			video.play();

			// Update the button text to 'Pause'
			//playButton.innerHTML = "Pause";
		} else {
			// Pause the video
			video.pause();

			// Update the button text to 'Play'
			//playButton.innerHTML = "Play";
		}
	});
	
    // Event listener for the step-forward button
	stepForwardButton.addEventListener("click", function() {
		var currTime = video.currentTime;
		video.currentTime = currTime+0.04;
	});
    // Event listener for the step-back button
	stepBackButton.addEventListener("click", function() {
		var currTime = video.currentTime;
		video.currentTime = currTime-0.04;
	});


	// Event listener for the mute button
	muteButton.addEventListener("click", function() {
		if (video.muted == false) {
			// Mute the video
			video.muted = true;

			// Update the button text
			//muteButton.innerHTML = "Unmute";
			muteButton.innerHTML = "U";
		} else {
			// Unmute the video
			video.muted = false;

			// Update the button text
			//muteButton.innerHTML = "Mute";
			muteButton.innerHTML = "M";
		}
	});


	// Event listener for the full-screen button
	fullScreenButton.addEventListener("click", function() {
		if (video.requestFullscreen) {
			video.requestFullscreen();
		} else if (video.mozRequestFullScreen) {
			video.mozRequestFullScreen(); // Firefox
		} else if (video.webkitRequestFullscreen) {
			video.webkitRequestFullscreen(); // Chrome and Safari
		}
	});


	// Event listener for the seek bar
	seekBar.addEventListener("change", function() {
        //muteButton.innerHTML = seekBar.value;
        //playButton.innerHTML = video.currentTime;
		
        // Calculate the new time
        var start_time = 5;
        var end_time = 10;

        // multiplier from 0 to 1
        var seek_mult = seekBar.value / 100;

		//var time = video.duration * (seekBar.value / 100);
		var time = start_time + (end_time - start_time) * seek_mult;

		// Update the video time
		video.currentTime = time;
	});

	
	// Update the seek bar as the video plays
	video.addEventListener("timeupdate", function() {
			
        //muteButton.innerHTML = seekBar.value;
        //playButton.innerHTML = video.currentTime;
        
        // Calculate the slider value
		//var value = (100 / video.duration) * video.currentTime;
		var value = (video.currentTime - start_time) / (end_time - start_time) * 100;

		// Update the slider value
		seekBar.value = value;
		
        if(video.paused == false && seekBar.value >= 100){
            video.pause()
            seekBar.value = 0;
            video.currentTime = start_time;
        }
	});

	// Pause the video when the seek handle is being dragged
	seekBar.addEventListener("mousedown", function() {
		video.pause();
	});

	// Play the video when the seek handle is dropped
	seekBar.addEventListener("mouseup", function() {
		//video.play();
	});

	// Event listener for the volume bar
	volumeBar.addEventListener("change", function() {
		// Update the video volume
		//video.volume = volumeBar.value;
        video.playbackRate = volumeBar.value;
	});
}
