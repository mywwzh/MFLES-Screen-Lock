<?php

include 'config.php';

// 创建数据库连接
$conn = new mysqli($host, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 处理 GET 请求
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // 检查是否存在 addr 参数
    if(isset($_GET['addr'])) {
        $addr = $_GET['addr'];
        $html_content = file_get_contents('./statics/command.html');
        // 替换模板中的占位符
        $html_content = str_replace('{addr}', $addr, $html_content);
        echo $html_content;
    } else {
        echo "Missing addr parameter";
    }
}

// 处理 POST 请求
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // 检查是否存在 addr 和 command 参数
    if(isset($_POST['addr']) && isset($_POST['command'])) {
        $addr = $_POST['addr'];
        $command = $_POST['command'];
        $time = time();
        // 更新数据库中的 command 字段
        $sql = "UPDATE classroom SET command=?, command_set_time=? WHERE addr=?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sds", $command, $time, $addr);
        if ($stmt->execute()) {
            echo "<script>alert('指令下发成功，设备可能会有最多15s的延迟。');window.location.href='/indexv1.php'</script>";
        } else {
            echo "Error: " . $stmt->error;
        }
    } else {
        echo "Missing addr or command parameter";
    }
}

// 关闭数据库连接
$conn->close();
?>
