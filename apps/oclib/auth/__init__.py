#-*- coding: utf8 -*-
import hashlib

def build_rkauth_signature(rkauth_fields):
    """生成rkauth签名"""
    payload = "&".join(k + "=" + str(rkauth_fields[k]) for k in sorted(rkauth_fields.keys()) if k != "rkauth_token")

    return hashlib.md5(payload).hexdigest()