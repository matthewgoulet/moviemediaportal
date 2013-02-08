<!DOCTYPE html>
<html>

<title>Movies</title>

<head>
<link rel="stylesheet" type="text/css" href="./style.css">
<link rel="stylesheet" type="text/css" href="./form-style.css">
<style>
#activemovieoption{
	background-color:#ABCABC;
}
</style>
</head>

<script type="text/javascript" >
function checkForm(form) {
	var movieTitle = form.movieTitle.value;
	var yearReleased = form.yearReleased.value;
	var genre = form.genre.value;
	var star = form.star.value;
	var costar = form.costar.value;
	var director = form.director.value;
	var producer = form.producer.value;
	var synopsis = form.synopsis.value;
	
	//Checks that the first name and password fields are filled.
	if (movieTitle.length == 0) {
		alert("Title field is empty");	
	}
	else if(yearReleased.length == 0){
		alert("Year released field is empty");	
	}
	else if(genre.length == 0){
		alert("Genre field is empty");	
	}	
	else if(star.length == 0){
		alert("Star field is empty");	
	}
	else if(costar.length == 0) {
		alert("COstar field is empty");
	}
	else if(director.length == 0){
		alert("Star field is empty");	
	}
	else if(producer.length == 0){
		alert("Star field is empty");	
	}
	else if(synopsis.length == 0) {
		alert("Synopsis field is empty");
	}
	
	function genAlert(){
	alert("This test worked!");	
	}
}

</script>


<body>

<div class="column">

<div class="headerheader">
	<?php include 'navigation.php' ?>
</div><!--ends header-->

<div class="notheader">
<center>
<form id="data" name="movieSubmissionMenu">
<fieldset>
<legend>Suggestion</legend>
<p><label for = movieTitle> <strong>Title:</strong></label><input type="text" name="movieTitle"></p>
<p><label for = yearReleased> <strong>Year Released:</strong></label> <input type="text" name="yearReleased"></p>
<p><label for = genre> <strong>Genre:</strong> </label> <input type="text" name="genre"></p>
<p><label for = star> <strong>Star:</strong> </label> <input type="text" name="star"></p>
<p><label for = costar> <strong>Co-star:</strong> </label> <input type="text" name="costar"></p>
<p><label for = director> <strong>Director:</strong> </label> <input type="text" name="director"></p>
<p><label for = producer> <strong>Producer:</strong> </label> <input type="text" name="producer"></p>
<p><label for = synopsis> <strong>Synopsis:</strong> </label> <input type="text" name="synopsis"></p>

<p class = "submit"><input type="submit" value="Submit" onClick = checkForm(this.form)></p>

</fieldset>

</form>
</center>
</div>
</div><!--ends column-->



<div class="footer">
	<?php include 'footer.php' ?>
</div>


</body>

</html>

