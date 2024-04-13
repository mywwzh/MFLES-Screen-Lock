<?php
session_start();

include 'config.php';

// 检查用户是否已登录
if (!isset($_COOKIE['access'])) {
    header("Location: /index.php");
    exit();
}
$html_content = file_get_contents('./statics/indexv1.html');

echo $html_content;
