<?php
session_start();

include 'config.php';

// 检查用户是否已登录
if (!isset($_COOKIE['access'])) {
    header("Location: /index.php");
    exit();
}
$conn = mysqli_connect($host, $username, $password, $dbname);

// 检查连接是否成功
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// 查询数据库获取数据
$sql = "SELECT * FROM classroom ORDER by addr";
$result = mysqli_query($conn, $sql);
$data = array();

if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $item = array(
            'addr' => $row['addr'],
            'class' => $row['class'],
            'is_locked' => $row['is_locked'],
            'last_request' => date('Y-m-d H:i:s', $row['last_request']),
            'status' => $row['status']
        );

        $data[] = $item;
    }
}

header('Content-Type: application/json');
echo json_encode($data);
