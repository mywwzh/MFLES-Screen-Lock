<?php
// 引入配置文件
include 'config.php';

/**
 * 创建数据库连接
 * @param string $host 服务器名
 * @param string $username 用户名
 * @param string $password 密码
 * @param string $dbname 数据库名
 * @return mysqli 数据库连接对象
 */
function createDatabaseConnection($host, $username, $password, $dbname)
{
    $conn = new mysqli($host, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }
    return $conn;
}

/**
 * 处理 GET 请求
 * @param mysqli $conn 数据库连接对象
 */
function handleGetRequest($conn)
{
    // 检查是否存在必要参数
    if (isset($_GET['password']) && isset($_GET['machine_uuid']) && isset($_GET['addr'])) {
        // 获取参数值
        $password = $_GET['password'];
        $machine_uuid = $_GET['machine_uuid'];
        $addr = $_GET['addr'];
        $ua = mysqli_real_escape_string($conn, $_SERVER['HTTP_USER_AGENT']); // 获取用户代理信息
        $ip = $_SERVER['REMOTE_ADDR']; // 获取用户IP地址

        // 解码出解锁码
        $unlock_code = substr($password, 0, 6); // 假设解锁码为前6个字符

        // 将日志插入到 log 表中
        $sql = "INSERT INTO log (`time`, `ip`, `addr`, `ua`) VALUES (NOW(), '$ip', '$addr', '$ua')";

        if ($conn->query($sql) === TRUE) {
            // 显示当前设备和动态解锁码
            displayUnlockInfo($addr, $unlock_code);
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    } else {
        echo "Missing password, machine_uuid, or addr parameter";
    }
}

/**
 * 显示设备解锁信息
 * @param string $addr 设备地址
 * @param string $unlock_code 动态解锁码
 */
function displayUnlockInfo($addr, $unlock_code)
{
    $html_content = file_get_contents('./statics/verify.html');
    // 替换模板中的占位符
    $html_content = str_replace('{addr}', $addr, $html_content);
    $html_content = str_replace('{unlock_code}', $unlock_code, $html_content);
    echo $html_content;
}

// 创建数据库连接
$conn = createDatabaseConnection($host, $username, $password, $dbname);

// 处理 GET 请求
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    handleGetRequest($conn);
}

// 关闭数据库连接
$conn->close();
