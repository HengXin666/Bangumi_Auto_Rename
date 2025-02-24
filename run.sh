#!/bin/bash

WORK_DIR=$(pwd)
echo "📌 当前工作目录: $WORK_DIR"

# 1. 生成 start.sh
echo "📌 生成 start.sh..."
cat <<EOF > "$WORK_DIR/start.sh"
#!/bin/bash
cd "$WORK_DIR"
python -m src.start
EOF
chmod +x "$WORK_DIR/start.sh"
echo "✅ start.sh 创建完成！"

# 2. 配置 crontab
echo "📌 配置 crontab 开机自启..."
(crontab -l 2>/dev/null; echo "@reboot /bin/bash $WORK_DIR/start.sh") | crontab -
echo "✅ crontab 配置完成！"

# 3. 安装并配置 supervisord（可选）
echo "📌 安装 supervisord..."
apt update && apt install -y supervisor
mkdir -p /etc/supervisor/conf.d
cat <<EOF | tee /etc/supervisor/conf.d/bangumi_autorename.conf > /dev/null
[program:bangumi_autorename]
command=/bin/bash $WORK_DIR/start.sh
autostart=true
autorestart=true
stderr_logfile=/var/log/bangumi_autorename.err.log
stdout_logfile=/var/log/bangumi_autorename.out.log
EOF
echo "✅ supervisor 配置完成！"

# 4. 启动 supervisord
echo "📌 启动 supervisord..."
supervisord -c /etc/supervisor/supervisord.conf
supervisorctl reread
supervisorctl update
supervisorctl start bangumi_autorename
echo "✅ 进程守护已启动！"

echo "🎉 配置完成！重启后 Bangumi Auto Rename 将自动运行！"
