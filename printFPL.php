<?php
/* At the moment the things I have avail to display are: 

'leg' ,'from', 'to', 'TAS', 'Magnetic Heading, 'Ground Speed', 'Distance', 'ETA', 'CumETA'

*/
require __DIR__ . '/vendor/autoload.php';
use Mike42\Escpos\PrintConnectors\FilePrintConnector;
use Mike42\Escpos\Printer;

$connector = new FilePrintConnector("/dev/usb/lp0");
$printer = new Printer($connector);

// Get data from Python script
$data = json_decode($argv[1], true);

foreach ($data as $entry) {
    // premade
    $eta_cumeta = "ETA " . $entry['ETA'] . " Total " . $entry['CumETA'];
    $path = $entry['from'] . " > " . $entry['to'];
    $at = $entry['TAS'] . "kt for " . $entry['Distance'] . "NM";

    $printer->setTextSize(2, 2);
    $printer->text(wordwrap($path, 15, "\n"));
    $printer->text("\n"); // Force a new line
    $printer->text(wordwrap($entry['Magnetic Heading'], 15, "\n"));
    $printer->setTextSize(1, 1);
    $printer->text(wordwrap($at, 22, "\n"));
    $printer->text("\n"); // Force a new line
    $printer->text(wordwrap($eta_cumeta, 22, "\n"));
    $printer->text("\n"); // Force a new line

    // Print separator
    $printer->setTextSize(1, 1);    
    $printer->text("\n"); // Force a new line
    $printer->text("--------------------------\n");

    $printer->feed();
}

// Close the printer connection
$printer->cut();
$printer->close();
?>
