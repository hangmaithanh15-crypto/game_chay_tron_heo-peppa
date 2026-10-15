import streamlit as st

st.set_page_config(
    page_title="Trò Chơi Chạy Trốn Quái Vật", page_icon="🎮", layout="centered"
)

st.title("🏃‍♂️ Trò Chơi: Chạy Trốn Quái Vật")
st.markdown(
    "Sử dụng các phím mũi tên **Trái / Phải** hoặc bấm các nút bên dưới để né chướng"
    " ngại vật và chạy trốn quái vật heo!"
)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Temple Run Game</title>
    <style>
        body {
            background-color: #0e1117;
            color: white;
            text-align: center;
            font-family: sans-serif;
            margin: 0;
            padding: 0;
        }
        canvas {
            background: linear-gradient(to bottom, #d7ccc8, #8d6e63);
            display: block;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        .controls {
            margin-top: 15px;
        }
        .btn {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin: 0 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .btn:active {
            background-color: #ff2222;
            transform: translateY(2px);
        }
    </style>
</head>
<body>

    <canvas id="gameCanvas" width="600" height="400"></canvas>
    
    <div class="controls">
        <button class="btn" onclick="moveLeft()">◀ Trái</button>
        <button class="btn" onclick="moveRight()">Phải ▶</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let gameOver = false;
        let gameStarted = false;

        // 3 làn đường
        const lanes = [150, 300, 450];
        let playerLane = 1; 
        let playerX = lanes[playerLane];
        let playerY = 300;

        let monsterX = 300;
        let monsterY = 330;

        let obstacles = [];
        let frameCount = 0;

        window.addEventListener("keydown", function(e) {
            if (!gameStarted && (e.code === "Space" || e.code === "ArrowUp")) {
                gameStarted = true;
                resetGame();
                return;
            }
            if (gameOver && e.code === "Space") {
                resetGame();
                return;
            }
            if (!gameOver && gameStarted) {
                if (e.code === "ArrowLeft" || e.code === "KeyA") {
                    moveLeft();
                }
                if (e.code === "ArrowRight" || e.code === "KeyD") {
                    moveRight();
                }
            }
        });

        function moveLeft() {
            if (playerLane > 0) playerLane--;
        }

        function moveRight() {
            if (playerLane < lanes.length - 1) playerLane++;
        }

        function resetGame() {
            score = 0;
            gameOver = false;
            obstacles = [];
            playerLane = 1;
            gameStarted = true;
        }

        function update() {
            if (!gameStarted || gameOver) return;

            let targetX = lanes[playerLane];
            playerX += (targetX - playerX) * 0.2;

            frameCount++;
            if (frameCount % 90 === 0) {
                let lane = Math.floor(Math.random() * 3);
                obstacles.push({ lane: lane, y: -50, passed: false });
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].y += 4; 

                let obsX = lanes[obstacles[i].lane];
                let obsY = obstacles[i].y;

                if (Math.abs(playerX - obsX) < 30 && Math.abs(playerY - obsY) < 40) {
                    gameOver = true;
                }

                if (obstacles[i].y > playerY && !obstacles[i].passed) {
                    score += 10;
                    obstacles[i].passed = true;
                }

                if (obstacles[i].y > 450) {
                    obstacles.splice(i, 1);
                }
            }
        }

        function draw() {
            // Vẽ nền đường
            ctx.fillStyle = "#795548";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Vẽ vạch phân làn
            ctx.strokeStyle = "#d7ccc8";
            ctx.lineWidth = 4;
            ctx.setLineDash([15, 15]);
            ctx.beginPath();
            ctx.moveTo(225, 0); ctx.lineTo(225, 400);
            ctx.moveTo(375, 0); ctx.lineTo(375, 400);
            ctx.stroke();
            ctx.setLineDash([]);

            if (!gameStarted) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "white";
                ctx.font = "28px Arial";
                ctx.textAlign = "center";
                ctx.fillText("CHẠY TRỐN QUÁI VẬT", canvas.width / 2, 160);
                ctx.font = "18px Arial";
                ctx.fillText("Nhấn phím Cách (Space) để Bắt đầu", canvas.width / 2, 220);
                return;
            }

            // Vẽ vật cản (Đá)
            for (let obs of obstacles) {
                let ox = lanes[obs.lane];
                let oy = obs.y;
                ctx.fillStyle = "#424242";
                ctx.beginPath();
                ctx.arc(ox, oy, 25, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 2;
                ctx.stroke();
            }

            // Vẽ nhân vật (Cá mập đi giày)
            ctx.fillStyle = "#03a9f4";
            ctx.beginPath();
            ctx.ellipse(playerX, playerY, 22, 14, 0, 0, Math.PI * 2);
            ctx.fill();
            // Giày cho cá mập
            ctx.fillStyle = "#ffeb3b";
            ctx.fillRect(playerX - 12, playerY + 8, 8, 10);
            ctx.fillRect(playerX + 4, playerY + 8, 8, 10);

            // Vẽ quái vật heo rượt đuổi phía sau
            ctx.fillStyle = "#e91e63";
            ctx.beginPath();
            ctx.arc(monsterX, monsterY, 32, 0, Math.PI * 2);
            ctx.fill();
            // Mắt quái vật
            ctx.fillStyle = "yellow";
            ctx.beginPath();
            ctx.arc(monsterX - 10, monsterY - 5, 5, 0, Math.PI * 2);
            ctx.arc(monsterX + 10, monsterY - 5, 5, 0, Math.PI * 2);
            ctx.fill();

            // Hiển thị điểm
            ctx.fillStyle = "white";
            ctx.font = "20px Arial";
            ctx.textAlign = "left";
            ctx.fillText("Điểm: " + score, 20, 30);

            // Màn hình thua cuộc
            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff4b4b";
                ctx.font = "36px Arial";
                ctx.textAlign = "center";
                ctx.fillText("BẠN ĐÃ BẮT GẶP QUÁI VẬT!", canvas.width / 2, 160);
                ctx.fillStyle = "white";
                ctx.font = "20px Arial";
                ctx.fillText("Điểm số: " + score, canvas.width / 2, 210);
                ctx.fillText("Nhấn phím Cách (Space) để Chơi lại", canvas.width / 2, 260);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=500)