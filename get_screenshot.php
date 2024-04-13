<?php
include "config.php";

// 创建数据库连接
$conn = new mysqli($host, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 处理 GET 请求
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // 检查是否存在 addr 参数
    if (isset($_GET['addr'])) {
        $addr = $_GET['addr'];
        $time = time();
        // 使用参数绑定来构造 SQL 查询
        $sql = "UPDATE classroom SET show_screen_set_time=? WHERE addr=?";

        // 准备 SQL 语句并绑定参数
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ss", $time, $addr);

        // 执行 SQL 查询
        if ($stmt->execute() === TRUE) {
            echo "";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
            exit();
        }
    } else {
        echo "Missing addr parameter";
        exit();
    }

    // 构造图片路径
    $image_path = './screenshots/' . $addr . '.png';

    // 检查文件是否存在
    if (file_exists($image_path)) {
        // 发送图片
        header("Content-Type: image/png");
        readfile($image_path);
    } else {
        // 图片不存在
        header('HTTP/1.1 404 Not Found');
    }
}
