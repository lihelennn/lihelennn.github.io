#!/usr/bin/python
print "content-type: text/html\n"
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()
userHuntRequest = '"'  + str(form.getvalue('nameOfHunt')) + '"' + ';'
print '''<!DOCTYPE html>
        <html>
		<head> 
			<meta charset="UTF-8"/>
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>CityHunt</title>
			<link rel="stylesheet" href="NEWhunt.css" type="text/css" />
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
			<script type="text/javascript" src="http://www.parsecdn.com/js/parse-1.5.0.min.js"></script>
		</head>
		<body>
			<header>
				<img src="logo.png" alt="logo"/> 
				<h1 id="level">Complete a CityHunt</h1>
				
				<h2 id="goodJob">Get to Know the City</h2>
				<p id="credits">Created by Stephanie Yoon and Helen Li</p>
				<br>
				<p id="hint">When you think you've arrived at the location described in the hint, tap the "I am Here" button.</p> <!--THIS IS THE HINT THAT GETS CHANGED-->
				<br><br>
			</header>
			<button id="imThere">I am Here</button>
			<!--^This test doesn't work most likely because it's not on the server, but that's the syntax.-->
			<script>
			
				Parse.initialize("awnQXrUGXA7So4fYUhJ6voqKunuRy8Cn1LiO4erQ", "PG85c5hyH1P5ZBLEBueSe8lBzE2o9nP05sbQTcB8");
				
				//<?php
				//	$namehunt = $_POST["nameOfHunt"];
				//?>
				//var nameofhunt = <?php echo $namehunt; ?>;
				
				var nameofhunt = '''+ userHuntRequest

print '''		var arrayLoc = [];
				
				function classLoc (hint, latitude, longitude) {
					this.hint = hint;
					this.longitude = longitude;
					this.latitude = latitude;
				}
				
				var NewHunt = Parse.Object.extend("NewHunt");
				var query = new Parse.Query(NewHunt);
				query.equalTo("huntName", nameofhunt);
				console.log("query" + nameofhunt);
				query.first({
				//query.find({
					success: function(object) {
					//alert("Successfully retrieved " + (object.get("huntList"))[0].hint);
					// Do something with the returned Parse.Object values
								
						for (var i = 0; i < object.get("huntList").length; i++) {
							//var object = results[i];
							//alert(object.id + ' - ' + object.get('huntName'));
							//alert(object.get("huntList")[i].hint);
							//alert(object.get("huntList")[i].latitude);
							//alert(object.get("huntList")[i].longitude);
							var hintt = object.get("huntList")[i].hint;
							//var lat = (Math.round(((object.get("huntList")[i].latitude)*1000000)/1000000));
							//var lon = (Math.round(((object.get("huntList")[i].longitude)*1000000)/1000000));
							var lat = object.get("huntList")[i].latitude;
							var lon = object.get("huntList")[i].longitude;
							arrayLoc.push(new classLoc(hintt , lat, lon));				
							//console.log("pushing" + arrayLoc[i].hint);							
						}
						showHintFirstLevel();

					},
					error: function(error) {
						alert("Error: " + error.code + " " + error.message);
					}
				});
			
				var currentLevel = 0;

				var currentLocation = [];
										
				function getLocation() {
					if (navigator.geolocation) {
						navigator.geolocation.getCurrentPosition(showPosition);
					} else { 
						console.log("Geolocation not supported by your browser");
					}
				}
		
				
				function showPosition(coord) {
					currentLocation=[];	
					//currentLocation.push(Math.round(((coord.coords.latitude)*1000000)/1000000));
					//currentLocation.push(Math.round(((coord.coords.longitude)*1000000)/1000000));
					currentLocation.push(coord.coords.latitude);
					currentLocation.push(coord.coords.longitude);
					checkMyLoc();
					//alert("showPosition" + currentLocation);
					//alert(currentLocation[0]);
					//alert(currentLocation[1]);
				}
				
				var showHintFirstLevel = function(){
					$("#level").html("Level 1");
					$("#hint").html(arrayLoc[currentLevel].hint);
				}
				
				var checkMyLoc = function() { 
					if((Math.abs(currentLocation[0] - arrayLoc[currentLevel].latitude <= 0.001)) && //last two digits, 100,000th and 1,000,000th
							(Math.abs(currentLocation[1] - arrayLoc[currentLevel].longitude <= 0.001))){ //need to add boolean here
						//use geolocator api
						//if matches up within radius, move on to next level
						//console.log(arrayLoc[currentLevel].latitude);
						//console.log(arrayLoc[currentLevel].latitude);
						//console.log(arrayLoc[currentLevel].latitude);
						
						currentLevel += 1;
						
						
						if(currentLevel === (arrayLoc.length)) { //length of hunt from parse
						//go to CONGRATS
						currentLevel = -1;
						$("#level").html("Congratulations!");
						$("#hint").html("You have completed all of the levels.");
						$("#imThere").remove();
						$("#goodJob").remove();
						}else{
						
						$("#level").html("Level " + (currentLevel+1));
						$("#hint").html(arrayLoc[currentLevel].hint);
						$("#goodJob").html("Good Job!");
						}
					

					}
					else {
						//add a Try again to html, but otherwise change nothing
						$("#goodJob").html("Close but no cigar.");
					}
				}
				
				$("#imThere").click(getLocation); 
			</script>
		</body>
	</html>'''
