import hashlib

# 渠道api签名
# 秘钥与请求参数值拼接后进行md5签名，字典应为按key排序的OrderedDict
def sign_api_channel_map(channelKey, orderedDict):
    sign_data = str(channelKey)
    for key, value in orderedDict.items():
        sign_data += str(value)
    md = hashlib.md5()
    md.update(sign_data.encode('utf-8'))
    return md.hexdigest()

