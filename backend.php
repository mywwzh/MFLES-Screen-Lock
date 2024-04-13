<?php

include 'config.php';

// 连接到数据库
$conn = mysqli_connect($host, $username, $password, $dbname);

// 检查连接是否成功
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// 处理POST请求
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $response = array(); // 初始化响应数组

    // 获取POST数据
    $addr = $_POST['addr'];
    $status = $_POST['status'];
    $status_set_user = $_COOKIE['access'];
    $time = time();

    // 准备更新数据库的SQL语句
    $sql = "UPDATE classroom SET status_set_time=?, status=?, status_set_user=? WHERE addr=?";

    // 使用预处理语句执行SQL查询
    $stmt = mysqli_prepare($conn, $sql);
    mysqli_stmt_bind_param($stmt, "ssss", $time, $status, $status_set_user, $addr);

    // 执行查询
    if (mysqli_stmt_execute($stmt)) {
        $response['status'] = 'success';
        $response['message'] = 'Lock/Unlock successfully.';
    } else {
        $response['status'] = 'error';
        $response['message'] = 'Error updating record: ' . mysqli_error($conn);
    }

    // 返回 JSON 格式的响应
    header('Content-Type: application/json');
    echo json_encode($response);
}

// 关闭数据库连接
mysqli_close($conn);
?>
