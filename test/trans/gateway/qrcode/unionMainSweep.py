import json
import os
import unittest

import requests

from facade.enum.db import DBName, DBENV
from test.common.paramUtil import is_keyword
from util import DBUtil, ExcelUtil, WorkspaceUtil


# 3.9、二维码主扫消费
# 请求方式：HTTP POST + JSON
# 接口地址：/gateway/channel/api/qrCode/mainSweep
# 请求参数:
# {
#   accUsrNo : String,     //接入用户编号
#   trxChnNo : String,     //交易通道编号
#   trxTyp : String,       //交易类型代码
#   trxId : String,        //交易流水号
#   trxAmt : String,       //交易金额（格式：0.00）
#   mrchntNo : String,     //商户编号
#   mrchntNm : String,     //商户名称
#   productDesc：String     // 商品描述
#   sign : String          //签名
# }
# 返回参数：
# {
#   code : String,         //接口返回码，000000 成功
#   message : String,      //接口返回描述
#   data : {
#       rpCd : String,      //交易应答码，000000 成功
#       rpDesc : String,    //交易应答描述
#       qrCodeInfo : String //二维码信息
#   }
# }

class UnionMainSweepTest(unittest.TestCase):
    conn = None
    cur = None
    # { 1:{'request': '{"accUserNo":"4000","trxChnNo":"2100","trxTyp":"1201","trxId":"17b80f1d1f75adeb","trxAmt":0.01,"mrchntNo":"__createRadomUuid(16)__","mrchntNm":"刘无媚-页面新增企业商户","productDesc":"自动化测试用例1"}',
    # 'predict_response': '{"code":"000000","message":"SUCCESS","data":{"rpCd":"000000","rpDesc":"SUCCESS","qrCodeInfo":"__checkStartWith(https://)__"}}',
    # 'predict_db_data': '',
    # 'response': '',
    # 'db_data': '',
    # 'start_params': '{"db_search_delay_seconds":0}',
    # 'id': 1}}
    test_data = {}
    excel_path_name = '/resource/testdata/trans/gateway/qrcode/unionMainSweep.xlsx'
    test_name = '渠道网关--银联主扫'
    url = 'http://10.255.0.111:7185/gateway/channel/api/qrCode/mainSweep'

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        print("【%s】测试开始执行" % self.test_name)

    # 测试准备
    # 1. 读取测试数据，包括测试数据、接口返回预测、数据库信息预测
    def setUp(self):
        self.test_data = self.load_test_data()

    # 测试流程开始
    # 1. 接口访问
    # 2. 获取接口访问结果
    # 3. 获取数据库相关数据
    # 4. 接口返回数据与预测数据对比
    # 5. 数据库真实数据与预测数据对比
    def test_flow(self):
        self.accessInterface()

    def tearDown(self):
        print("tear_down is Running")
        self.cur.close()
        self.conn.close()

    # 加载测试数据
    def load_test_data(self):
        print("【%s】测试用例加载中......" % self.test_name)
        # 读取测试数据
        test_cases = ExcelUtil.read_testdata_by_excel(
            WorkspaceUtil.get_root_path() + self.excel_path_name)
        # 测试数据转json
        for each in test_cases:
            request = json.loads(each['request'])
            each['predict_response'] = json.loads(each['predict_response'])
            each['start_params'] = json.loads(each['start_params'])
            # 请求参数自定义方法调用
            for key, value in request.items():
                if is_keyword(value):
                    request[key] = a(value)
            each['request'] = request
            self.test_data[each['id']] = each
        print("测试用例:", self.test_data)
        print("【%s】测试用例加载完毕" % self.test_name)
        return self.test_data

    # 获取数据库内容
    def get_db_result(self, delay_second):
        self.conn = DBUtil.get_connection(DBName.CHANJET_PAY_CHANNEL, DBENV.STABLE)
        self.cur = self.conn.cursor()
        for index, value in enumerate(self.test_data):
            self.cur.execute(r"select * from cp_chn_pay_trans where trans_no = '%s'" % (value['trxId']))
            each_result = self.cur.fetchall()
            self.db_data.append(each_result)
        print(self.db_data)


    def accessInterface(self):
        for key, value in self.test_data:
            # 发送请求
            resp = requests.post(url=self.url, json=json.dumps(value['request']))
            # 下面是响应的内容
            content = resp.text


if __name__ == '__main__':
    # a =UnionMainSweepTest()
    # print(a.load_test_data())
    # unittest.main()
    conn = DBUtil.get_connection(DBName.CHANJET_PAY_CHANNEL, DBENV.STABLE)
    cur = conn.cursor()
    cur.execute(r"select * from cp_chn_pay_trans where id = '3354'")
    result = cur.fetchall()
    print(result)
    a = list(result[0])
    print(a)
    b = json.loads({"channel": a})
    print(b)
    cur.close()
    conn.close()
