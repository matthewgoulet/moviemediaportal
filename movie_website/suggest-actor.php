<!DOCTYPE html>
<html>

<title>Movies</title>

<head>
<link rel="stylesheet" type="text/css" href="./style.css">
<link rel="stylesheet" type="text/css" href="./form-style.css">
<style>
#activeactoroption{
	background-color:#ABCABC;
}
</style>
</head>

<script type="text/javascript" >
function checkForm(form) {
	var firstName = form.firstName.value;
	var lastName = form.lastName.value;
	var birthday = form.birthday.value;
	
	//Checks that the first name and password fields are filled.
	if (firstName.length == 0) {
		alert("Title field is empty");	
	}
	else if(lastName.length == 0){
		alert("Year released field is empty");	
	}
	else if(birthday.length == 0){
		alert("Genre field is empty");	
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
<p><label for = movieTitle> <strong>First Name:</strong></label><input type="text" name="firstName"></p>
<p><label for = yearReleased> <strong>Last Name:</strong></label> <input type="text" name="lastName"></p>
<p><label for = genre> <strong>Birthday:</strong> </label> <input type="text" name="birthday"></p>

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

