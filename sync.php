<?php

include "config.php";

$mysqli = new mysqli($host, $username, $password, $dbname);

// 检查连接是否成功
if ($mysqli->connect_errno) {
    echo "连接数据库失败: " . $mysqli->connect_error;
    exit();
}

// 获取传入的地址和锁定状态
$addr = $_GET['addr'];
$is_locked = $_GET['is_locked'];


// 设置响应头为json格式
header('Content-Type: application/json');

// 查询数据库
$query = "SELECT * FROM classroom WHERE addr = ?";
$stmt = $mysqli->prepare($query);
$stmt->bind_param("s", $addr);
$stmt->execute();
$result = $stmt->get_result();

// 处理查询结果
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo json_encode(array(
        'status' => $row['status'],
        'status_set_time' => $row['status_set_time'],
        'status_set_user' => $row['status_set_user'],
        'command' => $row['command'],
        'command_set_time' => $row['command_set_time'],
        'show_screen_set_time' => $row['show_screen_set_time'],
        'show_camera_set_time' => $row['show_camera_set_time']
    ));
} else {
    echo json_encode(array(
        'status' => 'lock',
        'status_set_time' => 1,
        'status_set_user' => $row['status_set_user'],
        'command' => 1,
        'command_set_time' => 1,
        'show_screen_set_time' => 1,
        'show_camera_set_time' => 1
    ));
}

// 更新最后请求时间和锁定状态
$lastRequestTime = strval(time());
$query = "UPDATE classroom SET last_request = ?, is_locked = ? WHERE addr = ?";
$stmt = $mysqli->prepare($query);
$stmt->bind_param("sss", $lastRequestTime, $is_locked, $addr); // 使用引用传递的变量
$stmt->execute();

// 关闭数据库连接
$stmt->close();
$mysqli->close();
