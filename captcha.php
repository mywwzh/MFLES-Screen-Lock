<?php
session_start();

$code = substr(md5(mt_rand()), 0, 6);
$_SESSION['captcha'] = $code;

$width = 100;
$height = 40;

$image = imagecreatetruecolor($width, $height);

$bgColor = imagecolorallocate($image, 255, 255, 255);
imagefill($image, 0, 0, $bgColor);

$textColor = imagecolorallocate($image, 0, 0, 0);
imagestring($image, 5, 10, 10, $code, $textColor);

header('Content-Type: image/png');
imagepng($image);
imagedestroy($image);
