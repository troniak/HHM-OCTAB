<%@ taglib prefix="c" uri="http://java.sun.com/jstl/core_rt"%>
<%@ taglib prefix="tt" tagdir="/WEB-INF/tags"%>
<tt:html>
<tt:head title="${game.video.title}">
	<script src="/static/script/ugslplayer.js"></script>
	<script src="/static/script/utils.js"></script>
	<script src="/static/script/videoplayer.js"></script>
	<script src="/static/script/taggingHistory.js"></script>
	<script src="/static/script/game.js"></script>
</tt:head>
<tt:body cssClass="game" pageName="game">

<div class="equal-cols-game">
	<div id="gameCanvas" class="box span8 relative col-game leading">		
	
		<header class="clear extended">
			<h1 class="h4 pull-left reset"><c:out value="${game.video.title}" /></h1>			
			<span id="timer-remaining" class="pull-right"></span>	
		</header>
        
        <section class="reset">
			<div id="vid-overlay-screen" class="row-fluid show">
				<div id="explanation" class="box clean span6">
					<div id="timer-intro" class="timer-intro"><small>The game starts in</small><strong>00:15</strong></div>
				
					<h2 class="h4">Instructions</h2>
					<ul>
						<li>Try to enter as many words as possible to describe what you see or hear</li>
						<li>Confirm a word by pushing [enter] on your keyboard</li>
						<li>Earn points by <strong>matching</strong>, which happens when you enter the same word as another player</li>
						<li>By joining a game, you submit to the following <a href="/voorwaarden" target="_blank">terms and conditions</a></li>
					</ul>				
					<h3 class="h5">Good luck!</h3>
				</div>
				<div class="box clean span6">
					<div id="playerList" class="box">
						<header class="rich">
							<h2 class="h3 pull-left reset">Players</h2>
							<a href="/game/${game.id}/recap/${user.id}" class="btn btn-primary pull-right">stop</a>
						</header>
						<section class="reset">
							<ul class="unstyled reset">
							</ul>
						</section>
						
					</div>		
				</div>
			</div>
			
            <%--
			<div id="videoFrame" class="outside">
				<div id="video" class="video"></div>
            </div>
            --%>
            <!-- Video -->
        <div id="gameCanvas" class="box span8 relative col-game leading">
        <%--    
        --%>   
            <div id="video-container" class="outside">
                <video class="video" id="video">
                    <source id="vidsource" src="${game.video.sourceUrl}" type="video/webm">
                    <%--<source src="/static/videos/bike.mp4" type="video/mp4">
                    <source src="/static/videos/mikethefrog.webm" type="video/webm">
                    <source src="/static/videos/mikethefrog.ogv" type="video/ogv">--%>
                    <p>
                      Your browser doesn't support HTML5 video.
                      <a href="/videos/mikethefrog.mp4">Download</a> the video instead.
                    </p>
                </video>
                
                <!-- Video Controls -->
                <div id="video-controls">
                    <button type="button" id="play-pause">P</button>
                    <input class="range" type="range" id="seek-bar" value="0" max="100">
                    <button type="button" id="step-back">&lt;</button>
                    <button type="button" id="step-forward">&gt;</button>
                    <%--<button type="button" id="mute">M</button>--%>
                    <input type="range" id="volume-bar" min="0" max="1" step="0.1" value="1">
                </div>
                <div id="video-controls2">
                    <button type="button" id="start-match">M</button>
                    <input class="range" type="range" id="start-tag-bar"  value="0" >
                </div>
                <div id="video-controls3">
                    <button type="button" id="end-match">M</button>
                    <input class="range" type="range" id="end-tag-bar"  value="0" >
                </div>
            </div>
        </div>
        </section>
        <%--
        <div id="gameCanvas" class="box span8 relative col-game leading">
            <div id="video-container">
            </div>
        </div>
        --%>
		<footer class="outside">
			<input type="text" maxlength="42" class="input-mega-xxl" id="inputField" />
		</footer>
		
	</div>
	
	<div id="rightColumn" class="box span4 col-game">
		<header class="rich extended">
			<h1 id="playerSessionScore" class="pull-left board span2">0</h1>				
			<h2 id="playerPosition" class="pull-right reset">
				<small class="h4">Rank</small>
				<span id="playerPositionMine">-</span> / <span id="playerPositionTotal" class="h4">-</span>
			</h2>
		</header>
		<section class="reset">
			<h3 class="h4 sub-header">Your tags:</h3>		
			<div id="tagList" class="tag-list scroll-box">
			</div>
		</section>
	</div>

</div>

<script type="text/javascript">
    // Video
    var html5video = document.getElementById("video");
    var vidsource  = document.getElementById("vidsource");

    // Buttons
    var playButton = document.getElementById("play-pause");
    var muteButton = document.getElementById("mute");
    var startMatchButton = document.getElementById("start-match");
    var endMatchButton = document.getElementById("end-match");
    var fullScreenButton = document.getElementById("full-screen");
    var stepForwardButton = document.getElementById("step-forward");
    var stepBackButton = document.getElementById("step-back");

    // Sliders
    var seekBar = document.getElementById("seek-bar");
    var volumeBar = document.getElementById("volume-bar");
    var startTagBar = document.getElementById("start-tag-bar");
    var endTagBar = document.getElementById("end-tag-bar");

    //playback
    var start_time = ${game.video.startTime};//5;
    var end_time = ${game.video.endTime};//10;
    if(end_time < 0){
        end_time = ${game.video.duration} / 1000; //convert ms to seconds
    }
    
    window.onload = function() {
        html5video.currentTime = start_time;
    }
    function getElapsed(){ //return time elapsed (in milliseconds)
        var elapsed = Math.ceil(html5video.currentTime * 1000);
        return elapsed;
    }
    function getDuration(){ //return video duration (in milliseconds)
        var duration = Math.ceil(Math.min(end_time-start_time,html5video.duration) * 1000);
        return duration;
    }
    function getTagStartTime(){ //get time of video at start tag (in ms)
        return Math.ceil(getVidTime(startTagBar.value) * 1000);
    }
    function getTagEndTime(){ //get time of video at end tag (in ms)
        return Math.ceil(getVidTime(endTagBar.value) * 1000);
    }
	// Event listener for the volume bar
	volumeBar.addEventListener("change", function() {
        html5video.playbackRate = volumeBar.value / volumeBar.max;
    });

    function getVidTime(barValue){
        var seek_mult = barValue / 100;
        var time = start_time + (end_time - start_time) * seek_mult;
        return time;
    }
    function getBarValue(vidTime){
        //alert(vidTime);
        var value = (vidTime - start_time) / (end_time - start_time) * 100;
        //alert('value: ' + value);
        return value;
    }

    // Calculate and update the seekBar value from video time
    function updateSeekBar(){
        var value = getBarValue(html5video.currentTime);
        seekBar.value = value;
        if(html5video.paused == false && seekBar.value >= 100){
            html5video.pause();
            seekBar.value = 0;
            html5video.currentTime = start_time;
        }
        var elapsed = getElapsed();
        var duration = getDuration();
        game.videoplayer.dispatchEvents("tick", [ elapsed, duration ]);
    }

    // Update the html5video time from seekBar value
    function updateVidTime() {
        // multiplier from 0 to 1
        var time = getVidTime(seekBar.value);
        html5video.currentTime = time;
    }
    
	jQuery(function() {
		<c:choose>
			<c:when test="${game.video.playerType == 'NPO'}">
				var video = {
						playerType : 'NPO',
						fragmentId : ${game.video.fragmentID},
						startTimeWithinEpisode : ${game.video.startTime},
						duration : ${game.video.duration}
					};
			</c:when>
			<c:when test="${game.video.playerType == 'JW'}">
				var video = {
						playerType : 'JW',
						sourceUrl : '${game.video.sourceUrl}',
						imageUrl : '${game.video.imageUrl}'
					};

			</c:when>
			<c:otherwise>
			var video = null;
			</c:otherwise>
		</c:choose>
        
        window.game = new Game(${game.id}, video, ${game.elapsed});
        
        
        // Event listener for the play/pause button
        playButton.addEventListener("click", function() {
            if (html5video.paused == true) {
                html5video.play();
            } else {
                html5video.pause();
            }
        });
        // Event listener for the start-match button to match start-tag bar with seekbar
        startMatchButton.addEventListener("click", function() {
                startTagBar.value = seekBar.value;
        });
        // Event listener for the start-match button to match end-tag bar with seekbar
        endMatchButton.addEventListener("click", function() {
                endTagBar.value = seekBar.value;
        });
        

        // Event listener for the step-forward button
        stepForwardButton.addEventListener("click", function() {
            html5video.pause();
            var currTime = html5video.currentTime;
            html5video.currentTime = currTime+0.04;
        });
        // Event listener for the step-back button
        stepBackButton.addEventListener("click", function() {
            html5video.pause();
            var currTime = html5video.currentTime;
            html5video.currentTime = currTime-0.04;
        });/**/
        // Event listener for the step-forward button
        stepForwardButton.addEventListener("onmousedown", function() {
        });
        // Event listener for the step-back button
        stepBackButton.addEventListener("onmousedown", function() {
        });
        // Event listener for the step-forward button
        stepForwardButton.addEventListener("onmouseup", function() {
        });
        // Event listener for the step-back button
        stepBackButton.addEventListener("onmouseup", function() {
        });
        
        // Update the seek bar as the html5video plays
        html5video.addEventListener("timeupdate", updateSeekBar);

        // Pause the video when the seek handle is being dragged
        seekBar.addEventListener("mousedown", function() {
            html5video.pause();
        });
        startTagBar.addEventListener("mousedown", function() {
            html5video.pause();
        });
        endTagBar.addEventListener("mousedown", function() {
            html5video.pause();
        });


        // Event listener for the seek bar
        seek_bar.addEventListener("change", updateVidTime);

        startTagBar.addEventListener("change", function() {
            seekBar.value = startTagBar.value;
            updateVidTime();
        });
        endTagBar.addEventListener("change", function() {
            seekBar.value = endTagBar.value;
            updateVidTime();
        });
	});
</script>

</tt:body>
</tt:html>
