
<?php

//https://stackoverflow.com/questions/11553678/read-xml-data-from-url-using-curl-and-php/11553847 used to load xml from site

$url="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml?5105e8233f9433cf70ac379d6ccc5775";
$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_URL, $url);    // get the url contents

$data = curl_exec($ch); // execute curl request
curl_close($ch);

$xml = simplexml_load_string($data);
//print_r($xml);
$usd_value = $xml->Cube->Cube->Cube[0]->attributes()[1];

$file_name = 'usd_currency_rates_';
$file_name .= $xml->Cube->Cube->attributes();
$file_name .=  '.csv';


$fp = fopen($file_name, 'w');
$file_header = array ("Currency Code", "Rate");
fputcsv($fp, $file_header);

foreach ($xml->Cube->Cube->Cube as $cube){

	if ($cube->attributes()[0] != "USD"){
		$currency = array($cube->attributes(), $cube->attributes()[1]/$usd_value);
	}
	else 
		$currency = array("EUR", 1/$usd_value);

	//print_r ($currency);
    fputcsv($fp, $currency);

}
fclose($fp);

?>