import json

import requests


# param 格式:{key1: value1,key2: value2}
def get(url, param):
    # 添加http报头信息
    req = requests.get(url, params=param)
    # 下面是响应的内容
    content = req.text
    return req


def post(aim_url, param):
    # 发送请求
    req = requests.post(aim_url, json=param)
    # 下面是响应的内容
    content = req.text

    return req


if __name__ == '__main__':
    parm = {"productDesc": "自动化测试", "trxTyp": "1301", "mrchntNo": "100000000000008", "trxChnNo": "2100",
              "sign": "abedb7be5cb42660b3c5465c40639cf2", "accUsrNo": "4000", "mrchntNm": "微信主扫商户",
              "trxId": "9753aafd960c9be3", "trxAmt": "0.01"}
    url = 'http://10.255.0.113:7185/gateway/channel/api/qrCode/mainSweep'
    req = requests.post(url, json=parm)
    print(req.text)
    print(json.loads(req.text))
