<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>状态巡查</title>
    <style>
        #loading {
            display: none;
        }

        /* 限制图片大小 */
        #image-container {
            width: 100%;
            max-width: 1920px;
            overflow: hidden;
        }

        #image {
            width: 100%;
            height: auto;
        }
    </style>
</head>

<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" id="pauseCheckbox">
                    <label class="form-check-label" for="pauseCheckbox">
                        暂停刷新画面
                    </label>
                </div>
                <div id="loading" class="text-center mb-3">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">正在刷新画面...</span>
                    </div>
                </div>
                <div id="image-container">
                    <img id="image" src="" alt="Image">
                </div>
            </div>
        </div>
    </div>

    <script>
        var pauseCheckbox = document.getElementById('pauseCheckbox');
        var paused = false;

        // Function to fetch image from get.php
        function fetchImage(addr) {
            if (!paused) {
                var image = document.getElementById('image');
                var loading = document.getElementById('loading');

                // Show loading animation
                loading.style.display = 'block';

                // Make GET request to get.php
                var xhr = new XMLHttpRequest();
                xhr.open('GET', 'get_camera.php?addr=' + addr, true);
                xhr.responseType = 'blob';

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        // Hide loading animation
                        loading.style.display = 'none';
                        // Set image source to fetched image
                        var blob = xhr.response;
                        var url = URL.createObjectURL(blob);
                        image.src = url;
                    } else {
                        // Hide loading animation
                        loading.style.display = 'none';
                        console.error('Failed to fetch image');
                    }
                };

                xhr.send();
            }
        }

        // Function to periodically fetch image
        function periodicallyFetchImage(addr) {
            fetchImage(addr);
            setInterval(function() {
                fetchImage(addr);
            }, 2000); // Fetch image every 2 seconds
        }

        // Get the value of 'addr' parameter from the URL
        var urlParams = new URLSearchParams(window.location.search);
        var addr = urlParams.get('addr');

        // Start fetching image
        if (addr) {
            periodicallyFetchImage(addr);
        } else {
            console.error('Missing addr parameter');
        }

        // Event listener for the pause checkbox
        pauseCheckbox.addEventListener('change', function() {
            paused = this.checked;
        });
    </script>
</body>

</html>
