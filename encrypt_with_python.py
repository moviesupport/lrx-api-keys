#!/usr/bin/env python3
"""
密钥列表加密工具（Python 版本）

需要安装依赖：
    pip3 install pycryptodome

使用方法：
    python3 encrypt_with_python.py
"""

import json
import hashlib
import secrets
import binascii
import sys

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
except ImportError:
    print("❌ Error: pycryptodome not installed")
    print("Please install it with: pip3 install pycryptodome")
    sys.exit(1)

def encrypt_keys(input_file="keys.json", output_file="keys.json.encrypted", password="LRX-API-2024-Secure-Password-Key-123!"):
    """加密密钥列表文件"""
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证 JSON 格式
        json.loads(content)
        
        # 生成随机 IV（16 字节）
        iv = secrets.token_bytes(16)
        
        # 使用 PBKDF2 派生密钥（从密码派生 32 字节密钥）
        salt = b"lrx-api-sdk-salt"  # 固定盐值
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 10000, 32)
        
        # 创建加密器
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 加密
        encrypted = cipher.encrypt(pad(content.encode('utf-8'), 16))
        
        # 组合 IV + 密文
        result = iv + encrypted
        
        # 转换为 hex 字符串
        hex_str = binascii.hexlify(result).decode('ascii')
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(hex_str)
        
        print("✅ Encryption successful!")
        print(f"   Input:  {input_file}")
        print(f"   Output: {output_file}")
        print(f"   Password: {password}")
        print("\n⚠️  Remember to:")
        print("   1. Upload the encrypted file to GitHub")
        print("   2. Set the decrypt password in your SDK code")
        print("   3. Keep the password secure!")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "keys.json.encrypted"
        password = sys.argv[3] if len(sys.argv) > 3 else "LRX-API-2024-Secure-Password-Key-123!"
    else:
        input_file = "keys.json"
        output_file = "keys.json.encrypted"
        password = "LRX-API-2024-Secure-Password-Key-123!"
    
    if not encrypt_keys(input_file, output_file, password):
        sys.exit(1)

