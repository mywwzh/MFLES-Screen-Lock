<?php
// 检查是否有文件上传
if (isset($_FILES['file']) && $_POST['addr']) {
    $addr = $_POST['addr']; // 获取POST参数addr

    // 检查上传的文件是否为图像类型
    $check = getimagesize($_FILES['file']['tmp_name']);
    if ($check !== false) {
        // 指定保存目录
        $upload_dir = './cameras/';
        // 构造保存路径
        $upload_path = $upload_dir . $addr . '.png';
        // 移动上传的文件到目标路径
        if (move_uploaded_file($_FILES['file']['tmp_name'], $upload_path)) {
            echo "文件上传成功，保存在: " . $upload_path;
        } else {
            echo "文件上传失败";
        }
    } else {
        echo "上传的文件不是有效的图像文件";
    }
} else {
    echo "缺少必要的参数";
}
