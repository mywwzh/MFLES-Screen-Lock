<?php
$addr = $_GET['addr'];

// 设置响应头为json格式
header('Content-Type: application/json');

if($addr == "Axxx")
{
    return json_encode(array('set_time' => time(), 'status' => 'lock'));
}
else
{
    return json_encode(array('set_time' => 1, 'status' => 'lock'));
}
