<?php 
$configFile = file_get_contents("/etc/torquitor/torquitor.conf");
$settings = explode("\n", $configFile);
$iconinstitution = "";
$icondepartment = "";
$urlinstitution = "";
$urldepartment = "";
$refreshrate = "";

foreach ($settings as $line) 
{
	if(strpos($line, 'ICONINSTITUTION') !== false)
	{
		$arr = explode("=", $line);
		$iconinstitution = $arr[1];
	}
	else if(strpos($line, 'ICONDEPARTMENT') !== false)
	{
		$arr = explode("=", $line);
		$icondepartment = $arr[1];
	}
	else if(strpos($line, 'URLINSTITUTION') !== false)
	{
		$arr = explode("=", $line);
		$urlinstitution = $arr[1];
	}
	else if(strpos($line, 'URLDEPARTMENT') !== false)
	{
		$arr = explode("=", $line);
		$urldepartment = $arr[1];
	}
	else if(strpos($line, 'REFRESHRATE') !== false)
	{
		$arr = explode("=", $line);
		$refreshrate = $arr[1];
		$refreshrate *= 1000;
	}
}
?>

<!DOCTYPE html><html><head>

<link rel="stylesheet" type="text/css" href="DataTables/media/css/jquery.dataTables.css">
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<link rel="stylesheet" type="text/css" href="torquitor.css">
<script src="DataTables/media/js/jquery.js"></script>
<script src="DataTables/media/js/jquery.dataTables.min.js"></script>
<script src="DataTables/extensions/ColReorder/js/dataTables.colReorder.min.js"></script>
<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>

<script>

function requireData()
{
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
		{
			var response = xmlhttp.responseText.split("$");

			$("#pbsnodesDiv").html($(response[0]));
			$("#qstatDiv").html($(response[1]));
			$("#jobinfoDiv").html($(response[2]));
			$("#timestamp").html(response[3]);
			formatUI();
		}
	}
	xmlhttp.open("GET", "data.php", true);
	xmlhttp.send();
}

function formatUI()
{
	$('.jid').click(function(event){
		$( "#jobInfo" ).empty();
		info = $("#Job\\." + (event.target.id.replace(/\./g, "\\."))).clone().appendTo( "#jobInfo" );
		$( "#jobInfoDialog" ).dialog({
			modal: true,
			width:'auto',
			buttons: {
				Ok: function() {
					$( this ).dialog( "close" );
				}
			}
		});
	});

	$('#qstat').DataTable( {
		"order": [[0,'desc']], 
		"pageLength": 50,
		dom: 'Rlfrtip',
		"columnDefs": [
		    {
		        "targets": [ 4,5,6,7 ],
		        "visible": false,
		        "searchable": false
		    }
		],
		colReorder: {order: [ 0,9,3,1,2,8,10,4,5,6,7 ]}
		
	} );
}

$(document).ready(function() {
	requireData();
	setInterval(requireData, <?php echo $refreshrate; ?>);
});

</script>

</head>
<body style="font-family: monospace; ">

	<div id="header" class="fullwidth margin5 roundbox1" style="height:50px; padding: 5px 30px 5px 30px; margin-bottom:20px;">
		<div class="alignleft" style="height:50px;">
			<a href="<?php echo $urlinstitution; ?>"><img src="<?php echo $iconinstitution; ?>" style="height:50px; width:auto;"/></a>
			<a href="<?php echo $urldepartment; ?>"><img src="<?php echo $icondepartment; ?>" style="height:50px; width:auto;"/></a>
		</div>
		<div class="aligncenter" style="height:50px;">
			<h1 class="alignmiddle">Torquitor</h1>
		</div>	
		<div class="alignright" style="height:50px;">
			<div style="position: relative; top: 50%; transform: translateY(-50%);">
				<span>Updated every 5 seconds</span><br>
				<span>Server time : <span id="timestamp"></span></span>
			</div>
		</div>
	</div>

	<div class="fullwidth margin5 roundbox2">
		<h2>pbsnodes</h2>
		<div id="pbsnodesDiv"></div>
		<div class="fullwidth margin5"></div>
	</div>
	<br>

<!--
	<div class="fullwidth margin5">
		<h2>ShowQ</h2>
		<?php
		echo file_get_contents("data/showq.txt");
		?>
	</div>
	<br>
-->
	<div class="fillwidth margin5 roundbox2">
		<h2>qstat</h2>
		<div id="qstatDiv" class="roundbox1"></div>		
	</div>
	<div id="jobInfoDialog" title="Job Information">
		<div id="jobInfo"></div>
	</div>
	<br>
	<div id="jobinfoDiv" style="display:none">
	</div>

	<div id="footer" class="fullwidth margin5 roundbox1" style="height:50px; padding-left:30px; padding-right:30px; padding-top:5px; padding-bottom:5px;">
		<div class="alignleft" style="height:50px;">
			<a href="<?php echo $urlinstitution; ?>"><img src="<?php echo $iconinstitution; ?>" style="height:50px; width:auto;"/></a>
			<a href="<?php echo $urldepartment; ?>"><img src="<?php echo $icondepartment; ?>" style="height:50px; width:auto;"/></a>
		</div>
		<div class="aligncenter" style="height:50px;">
			<a href="https://creativecommons.org/licenses/by-sa/2.0/"><img src="by-sa.png" style="height:50px; width:auto;"/></a>
		</div>	
		<div class="alignright" style="height:50px;">
			<div style="position: relative; top: 50%; transform: translateY(-50%);">
				<span>Contact: <a href="mailto:cnca@cenat.ac.cr">cnca@cenat.ac.cr</a></span><br>
				<a href="">Download torquitor</a>
			</div>
		</div>
	</div>

</body>
</html>

