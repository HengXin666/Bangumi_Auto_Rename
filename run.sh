#!/bin/bash

# 获取当前脚本所在目录
WORK_DIR=$(pwd)

echo "📌 当前工作目录: $WORK_DIR"

# 1. 创建 start.sh
echo "📌 生成 start.sh 文件..."
cat <<EOF > "$WORK_DIR/start.sh"
#!/bin/bash
cd "$WORK_DIR"
python -m "$WORK_DIR/src.start"
EOF

# 赋予 start.sh 执行权限
chmod +x "$WORK_DIR/start.sh"
echo "✅ start.sh 创建完成，并赋予执行权限！"

# 2. 创建 systemd 服务文件
SERVICE_NAME="bangumi_autorename"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "📌 生成 systemd 服务文件: $SERVICE_FILE..."
cat <<EOF | sudo tee "$SERVICE_FILE" > /dev/null
[Unit]
Description=Bangumi Auto Rename Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash $WORK_DIR/start.sh
WorkingDirectory=$WORK_DIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

echo "✅ systemd 服务文件创建完成！"

# 3. 重新加载 systemd 并启用服务
echo "📌 重新加载 systemd..."
sudo systemctl daemon-reload

echo "📌 启用 ${SERVICE_NAME} 开机自启..."
sudo systemctl enable "$SERVICE_NAME"

echo "📌 启动 ${SERVICE_NAME} 服务..."
sudo systemctl start "$SERVICE_NAME"

# 4. 检查服务状态
echo "📌 检查 ${SERVICE_NAME} 运行状态..."
sudo systemctl status "$SERVICE_NAME" --no-pager

echo "🎉 配置完成！系统重启后，Bangumi Auto Rename 将自动启动！"
