<!DOCTYPE html>
<html>

<title>Login</title>

<head>
<link rel="stylesheet" type="text/css" href="./style.css">
<link rel="stylesheet" type="text/css" href="./form-style.css">

</head>

<script type="text/javascript" >
function checkForm(form) {
	var username = form.email.value;
	var inputPassword = form.password.value;
	
	//Checks that the first name and password fields are filled.
	else if(username.length == 0){
		alert("Username field is empty");	
	}
	else if(inputPassword.length == 0) {
		alert("Password field is empty");
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
<form id="data" name="loginMenu">
<fieldset>
<legend>Login</legend>
<p><label for = username> <strong>Username:</strong> </label> <input type="text" name="username"></p>
<p><label for = password> <strong>Password:</strong> </label> <input type="password" name="password"></p>

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

