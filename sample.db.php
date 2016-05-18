<?php

	$mysqli = new mysqli("localhost","wordpress","mysecurepassword","command");
	if ($mysqli->connect_error) {
		die("Connect error $mysqli->connect_error");
	}

?>


