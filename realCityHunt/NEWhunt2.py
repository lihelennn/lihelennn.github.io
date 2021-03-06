#!/usr/bin/python
print "content-type: text/html\n"
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()

userHuntRequest = str(form.getvalue('nameOfHunt'))

print("""
	<!DOCTYPE html>
	<html>
		<head>tent="width=device-width, initial-scale=1.0">
			<title>CityHunt</title>
			<meta charset="UTF-8"/>
			<meta name="viewport" con
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
			<!--^This test doesn't work most likely because it's not on the server, but that's the syntax.-->
			<script>
			
				Parse.initialize("awnQXrUGXA7So4fYUhJ6voqKunuRy8Cn1LiO4erQ", "PG85c5hyH1P5ZBLEBueSe8lBzE2o9nP05sbQTcB8");
				
				//<?php
				//	$namehunt = $_POST["nameOfHunt"];
				//?>
				//var nameofhunt = <?php echo $namehunt; ?>;
				
				var nameofhunt = '""" +  userHuntRequest+ """';
				
				var arrayLoc = [];
				
				function classLoc (hint, longitude, latitude) {
					this.hint = hint;
					this.longitude = longitude;
					this.latitude = latitude;
				}
				
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
							//alert(object.get("huntList")[i].long);
							arrayLoc.push(new classLoc(object.get("huntList")[0].hint , (Math.round(((object.get("huntList")[0].longitude)*1000000)/1000000)), (Math.round(((object.get("huntList")[0].latitude)*1000000)/1000000))));
						}
					},
					error: function(error) {
						alert("Error: " + error.code + " " + error.message);
					}
				});
			
				var currentLevel = -1;

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
					currentLocation.push(Math.round(((coord.coords.latitude)*1000000)/1000000));
					currentLocation.push(Math.round(((coord.coords.longitude)*1000000)/1000000));
					checkMyLoc();
					//alert("showPosition" + currentLocation);
					//alert(currentLocation[0]);
					//alert(currentLocation[1]);
				}
				
				var checkMyLoc = function() { 
					if(currentLevel === (arrayLoc.length - 1)) { //length of hunt from parse
						//go to CONGRATS
						currentLevel = -1;
						$("#level").html("Congratulations!");
						$("#hint").html("You have completed all of the levels.");
						$("#imThere").remove();
						$("#goodJob").remove();
					}
					else if(Math.floor(currentLocation[0]) === Math.floor(arrayLoc[currentLevel].longitude) && //last two digits, 100,000th and 1,000,000th
							Math.floor(currentLocation[1]) === Math.floor(arrayLoc[currentLevel].latitude) ){ //need to add boolean here
						//use geolocator api
						//if matches up within radius, move on to next level
						currentLevel += 1;
						$("#level").html("Level " + (currentLevel+1));
						$("#hint").html(arrayLoc[currentLevel].hint);
						$("#goodJob").html("Good Job!");
					}
					else {
						//add a Try again to html, but otherwise change nothing
						$("#goodJob").html("Close but no cigar.");
					}
				}
				
				$("#imThere").click(getLocation); 
			</script>
		</body>
	</html>
""")
