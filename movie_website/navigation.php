
	<a href="./homepage.php"><img class="logo" src="http://i.imgur.com/Td27HbI.png" alt="" /></a>
	
	<span class="loginlinks">
	<div id="toprightlogin"><a href="./register.php">Register</a> &nbsp;&nbsp;<a href="./login.php">Login</a></div>
	</span>
	
<span class="menulinks">
	<div class="menubar">
		<div class="menuoptions">
			<font color="white">
			<div class="inactivemovieoption" id="activemovieoption"><center><a href="./movie-list.php">Movies</a></center></div>
			<div class="inactivetvoption" id="activetvoption"><center><a href="./tv-list.php">TV</a></center></div>
			<div class="inactiveactoroption" id="activeactoroption"><center><a href="./actor-list.php">Actors</a></center></div>
			</font>
		</div>
		
		<div id="searchbar"> 
			<form name="search">
			<input type="text" size="25" id="search"/>
			<select>
				<option value="movies">Movies</option>
				<option value="tv">TV</option>
				<option value="actors">Actors</option>
				<option value="users">Users</option>
			</select>
			<input type="image" class="searchpic" height="20px" src="http://i.imgur.com/pZewlpP.png" onClick = checkForm(this.form) alt="" />
			</form>
		</div>
	</div>
</span>
