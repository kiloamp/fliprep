<?php
/* just print a custom string!
*/
require __DIR__ . '/vendor/autoload.php';
use Mike42\Escpos\PrintConnectors\FilePrintConnector;
use Mike42\Escpos\Printer;

$connector = new FilePrintConnector("/dev/usb/lp0");
$printer = new Printer($connector);

// Get raw data from command line argument
$data = $argv[1];

// Print the raw data string
$printer->setTextSize(1, 1);
$printer->text(wordwrap($data, 22, "\n"));
$printer->feed();

// Close the printer connection
$printer->cut();
$printer->close();
?>