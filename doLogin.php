<?php
session_start();

include 'config.php';

$conn = new mysqli($host, $username, $password, $dbname);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 检查验证码
if (isset($_POST['captcha']) && isset($_SESSION['captcha'])) {
    if ($_POST['captcha'] !== $_SESSION['captcha']) {
        die("验证码不正确");
    }
} else {
    die("验证码不能为空");
}

// 获取用户提交的用户名和密码
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // 使用预处理语句防止SQL注入
    $stmt = $conn->prepare("SELECT * FROM screenlock.user WHERE username=? AND password=?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        // 登录成功，设置Cookie
        setcookie("access", $username, 0, "/");
        header("Location: /indexv1.php");
        exit; // 重定向后立即退出脚本以防止进一步执行
    } else {
        echo "用户名或密码不正确";
    }
} else {
    echo "用户名或密码不能为空";
}

$conn->close();
