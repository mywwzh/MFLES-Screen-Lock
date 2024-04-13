var xhr = new XMLHttpRequest();
        xhr.open('GET', '/details.php', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                var table = document.getElementById('details');
                data.forEach(function (item) {
                    var row = table.insertRow();
                    row.insertCell(0).textContent = item.addr;
                    row.insertCell(1).textContent = item.class;
                    var lockedCell = row.insertCell(2);
                    if (item.is_locked != "lock" && item.is_locked != "unlock")
                    {
                        lockedCell.textContent = item.is_locked;
                        lockedCell.className = 'unlocked';
                    }
                    else
                    {
                        lockedCell.textContent = item.is_locked === 'lock' ? '已锁屏' : '未锁屏';
                        lockedCell.className = item.is_locked === 'lock' ? 'locked' : 'unlocked';
                    }
                    row.insertCell(3).textContent = item.last_request;

                    // 判断在线状态并更新对应的CSS类
                    var lastRequestTime = new Date(item.last_request).getTime();
                    var currentTime = new Date().getTime();
                    var timeDifference = (currentTime - lastRequestTime) / 1000; // 差值单位为秒
                    var statusCell = row.insertCell(4);
                    if (timeDifference < 10) {
                        statusCell.textContent = '在线';
                        statusCell.className = 'online';
                    } else {
                        statusCell.textContent = '离线';
                        statusCell.className = 'offline';
                    }

                    var actionCell = row.insertCell(5);

                    var lockButton = document.createElement('button');
                    lockButton.className = 'btn ' + (item.status === 'lock' ? 'btn-secondary' : 'btn-success');
                    lockButton.textContent = '锁屏';
                    lockButton.disabled = item.status === 'lock';
                    lockButton.setAttribute('data-addr', item.addr);
                    lockButton.addEventListener('click', function() {
                        lockUnlockScreen(this.getAttribute('data-addr'), 'lock');
                    });
                    actionCell.appendChild(lockButton);
                    
                    var unlockButton = document.createElement('button');
                    unlockButton.className = 'btn ' + (item.status === 'unlock' ? 'btn-secondary' : 'btn-danger');
                    unlockButton.textContent = '解锁';
                    unlockButton.disabled = item.status === 'unlock';
                    unlockButton.setAttribute('data-addr', item.addr);
                    unlockButton.addEventListener('click', function() {
                        lockUnlockScreen(this.getAttribute('data-addr'), 'unlock');
                    });
                    actionCell.appendChild(unlockButton);
                    
                    
                    var remoteCommandButton = document.createElement('button');
                    remoteCommandButton.className = 'btn btn-primary';
                    remoteCommandButton.textContent = '远程命令';
                    remoteCommandButton.addEventListener('click', function() {
                        window.location.href = '/command.php?addr=' + item.addr;
                    });
                    actionCell.appendChild(remoteCommandButton);
                    
                    var showScreenButton = document.createElement('button');
                    showScreenButton.className = 'btn btn-primary';
                    showScreenButton.textContent = '查看屏幕';
                    showScreenButton.addEventListener('click', function() {
                        window.location.href = '/show_screen.php?addr=' + item.addr;
                    });
                    actionCell.appendChild(showScreenButton);
                    
                    var showCameraButton = document.createElement('button');
                    showCameraButton.className = 'btn btn-primary';
                    showCameraButton.textContent = '状态巡查';
                    showCameraButton.addEventListener('click', function() {
                        window.location.href = '/show_camera.php?addr=' + item.addr;
                    });
                    actionCell.appendChild(showCameraButton);

                });
            }
        };
        xhr.send();
        
        // 处理锁屏按钮点击事件
        document.querySelectorAll('.lock-btn').forEach(button => {
            button.addEventListener('click', function() {
                const addr = this.getAttribute('data-addr');
                lockUnlockScreen(addr, 'lock');
            });
        });

        // 处理解锁按钮点击事件
        document.querySelectorAll('.unlock-btn').forEach(button => {
            button.addEventListener('click', function() {
                const addr = this.getAttribute('data-addr');
                lockUnlockScreen(addr, 'unlock');
            });
        });
        // 使用AJAX发送锁屏/解锁请求
        function lockUnlockScreen(addr, status) {
            const xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        if (response.status === 'success') {
                            alert('指令下发成功，设备可能会有最多10s的延迟。');
                            // 请求成功，刷新页面
                            location.reload();
                        } else {
                            alert('Error: ' + response.message);
                        }
                    } else {
                        console.error('Failed to lock/unlock screen');
                    }
                }
            };
            xhr.open('POST', 'backend.php', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.send('addr=' + encodeURIComponent(addr) + '&status=' + encodeURIComponent(status));
        }