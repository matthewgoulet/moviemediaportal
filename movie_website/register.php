<!DOCTYPE html>
<html>

<title>Register</title>

<head>
<link rel="stylesheet" type="text/css" href="./style.css">
<link rel="stylesheet" type="text/css" href="./form-style.css">

</head>

<script type="text/javascript" >
function checkForm(form) {
	var firstname = form.firstname.value;
	var lastname = form.lastname.value;
	var email = form.email.value;
	var username = form.email.value;
	var inputPassword = form.password.value;
	var checkPassword = form.confirmPassword.value;
	
	//Checks that the first name and password fields are filled.
	if (firstname.length == 0) {
		alert("First name field is empty");	
	}
	else if(lastname.length == 0){
		alert("Last name field is empty");	
	}
	else if(email.length == 0){
		alert("Email field is empty");	
	}	
	else if(username.length == 0){
		alert("Username field is empty");	
	}
	else if(inputPassword.length == 0) {
		alert("Password field is empty");
	}
	else if(checkPassword.length == 0) {
		alert("Password verification field is empty");
	}
	else if(inputPassword != checkPassword) {
		alert("The passwords do not match");	
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
<form id="data" name="registerMenu">
<fieldset>
<legend>Register</legend>
<p><label for = firstname> <strong>First Name:</strong></label><input type="text" name="firstname"></p>
<p><label for = lastname> <strong>Last Name:</strong></label> <input type="text" name="lastname"></p>
<p><label for = email> <strong>Email address:</strong> </label> <input type="text" name="email"></p>
<p><label for = username> <strong>Username:</strong> </label> <input type="text" name="username"></p>
<p><label for = password> <strong>Password:</strong> </label> <input type="password" name="password"></p>
<p><label for = confirmpassword> <strong>Confirm Password:</strong> </label> <input type="password" name="confirmPassword"></p>

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

