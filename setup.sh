echo '#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "Jalankan script ini sebagai root atau dengan sudo!"
    exit 1
fi

echo "Memperbarui paket..."
apt update && apt upgrade -y

echo "Menginstal OpenSSH Server..."
apt install -y openssh-server

echo "Mengaktifkan dan memulai SSH..."
systemctl enable ssh
systemctl start ssh

echo "Mengubah konfigurasi SSH..."
sed -i "s/#Port 22/Port 2222/" /etc/ssh/sshd_config
sed -i "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config
echo "AllowUsers $USER" >> /etc/ssh/sshd_config

echo "Restarting SSH service..."
systemctl restart ssh

echo "Membuka firewall untuk SSH di port 2222..."
ufw allow 2222/tcp

echo "Server SSH berhasil diinstal dan dikonfigurasi!"
echo "Gunakan perintah berikut untuk login:"
echo "ssh -p 2222 $USER@$(hostname -I | awk "{print \$1}")"
' > install-ssh.s
