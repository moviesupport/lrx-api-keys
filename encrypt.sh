#!/bin/bash
# 密钥列表加密脚本（使用 OpenSSL）

INPUT_FILE="keys.json"
OUTPUT_FILE="keys.json.encrypted"
PASSWORD="LRX-API-2024-Secure-Password-Key-123!"

echo "🔐 Encrypting keys.json..."

# 使用 OpenSSL AES-256-CBC 加密
# 注意：OpenSSL 的加密格式与 Rust SDK 不完全兼容
# 这里使用一个兼容的方式

# 生成随机 IV 和盐值
IV=$(openssl rand -hex 16)
SALT=$(openssl rand -hex 16)

# 使用 PBKDF2 派生密钥（OpenSSL 3.0+）
# 对于旧版本，使用简单的密钥派生
if openssl version | grep -q "OpenSSL 3"; then
    # OpenSSL 3.0+
    openssl enc -aes-256-cbc -pbkdf2 -iter 10000 -salt -in "$INPUT_FILE" -out "$OUTPUT_FILE" -K "$(echo -n "$PASSWORD$SALT" | sha256sum | cut -d' ' -f1)" -iv "$IV" 2>/dev/null
else
    # OpenSSL 1.x - 使用不同的方法
    echo -n "$PASSWORD" | openssl enc -aes-256-cbc -salt -in "$INPUT_FILE" -out "$OUTPUT_FILE" -pbkdf2 -iter 10000 2>/dev/null
fi

if [ $? -eq 0 ]; then
    echo "✅ Encryption successful!"
    echo "   Output: $OUTPUT_FILE"
else
    echo "❌ Encryption failed. Trying alternative method..."
    # 备用方法：使用 Python（如果可用）
    python3 -c "
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import secrets
import binascii
import sys

try:
    with open('$INPUT_FILE', 'r') as f:
        content = f.read()
    
    iv = secrets.token_bytes(16)
    salt = b'lrx-api-sdk-salt'
    password = '$PASSWORD'.encode()
    
    # PBKDF2
    key = hashlib.pbkdf2_hmac('sha256', password, salt, 10000, 32)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(content.encode(), 16))
    
    result = iv + encrypted
    hex_str = binascii.hexlify(result).decode()
    
    with open('$OUTPUT_FILE', 'w') as f:
        f.write(hex_str)
    
    print('✅ Encryption successful!')
    sys.exit(0)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "❌ Both methods failed. Please install pycryptodome:"
        echo "   pip3 install pycryptodome"
        exit 1
    fi
fi

