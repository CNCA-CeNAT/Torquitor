<?php

header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

echo file_get_contents("data/pbsnodes.txt");

echo "$";

echo file_get_contents("data/qstat.txt");

echo "$";

echo file_get_contents("data/jobinfo.txt");

echo "$";

echo date("Y/m/d - H:i:s");

?>
