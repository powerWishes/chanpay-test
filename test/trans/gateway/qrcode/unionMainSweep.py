import json
import unittest

import requests

from facade.enum.db import DBName, DBENV
from test.common.paramUtil import is_keyword, analysis_param
from util import DBUtil, ExcelUtil, WorkspaceUtil, MapUtil, SignUtil


# 3.9、二维码主扫消费
class UnionMainSweepTest(unittest.TestCase):
    conn = None
    cur = None
    # { 1:{'request': '{"accUserNo":"4000","trxChnNo":"2100","trxTyp":"1201","trxId":"17b80f1d1f75adeb","trxAmt":0.01,"mrchntNo":"__createRadomUuid(16)__","mrchntNm":"刘无媚-页面新增企业商户","productDesc":"自动化测试用例1"}',
    # 'predict_response': '{"code":"000000","message":"SUCCESS","data":{"rpCd":"000000","rpDesc":"SUCCESS","qrCodeInfo":"__checkStartWith(https://)__"}}',
    # 'predict_db_data': {'statusCode': '200', 'data': {'code': '000000', 'message': '__checkNotEmpty()__', 'data': {'rpCd': '000000', 'rpDesc': '__checkNotEmpty()__', 'qrCodeInfo': '__checkStartWith(https://)__'}}},
    # 'response': {},
    # 'db_data': {},
    # 'start_params': '{"channelKey":"0123456789ABCDEFFEDCBA9876543210"}',
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
    # 1. 接口访问 并 获取接口访问结果
    # 2. 获取数据库相关数据
    # 3. 接口返回数据与预测数据对比
    # 4. 数据库真实数据与预测数据对比
    def test_flow(self):
        self.accessInterface()
        self.get_db_result()
        self.predictResponse()

    def tearDown(self):
        print("tear_down is Running")
        print(self.test_data)
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
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
            each['predict_db_data'] = json.loads(each['predict_db_data'])
            each['response'] = {}
            each['db_data'] = {}
            # 请求参数自定义方法调用
            for key, value in request.items():
                if is_keyword(value):
                    request[key] = analysis_param(value)
            each['request'] = request
            # 签名
            sign = SignUtil.sign_api_channel_map(each['start_params']['channelKey'],
                                                 MapUtil.to_tree_map(each['request']))
            each['request']['sign'] = sign
            self.test_data[each['id']] = each
        print("测试用例:", self.test_data)
        print("【%s】测试用例加载完毕" % self.test_name)
        return self.test_data

    # 获取数据库内容
    def get_db_result(self, delay_second):
        self.conn = DBUtil.get_connection(DBName.CHANJET_PAY_CHANNEL, DBENV.STABLE)
        self.cur = self.conn.cursor()
        for key, value in self.test_data.items():
            self.cur.execute(r"select * from cp_chn_pay_trans where trans_no = '%s'" % (value['request']['trxId']))
            each_result = self.cur.fetchall()
            self.test_data[key]['db_data']['channel'] = each_result

    # 访问接口
    def accessInterface(self):
        for key, value in self.test_data.items():
            # 发送请求
            resp = requests.post(url=self.url, json=value['request'])
            # 获取接口访问状态
            self.test_data[key]['response']['statusCode'] = resp.status_code
            # 获取响应的内容
            self.test_data[key]['response']['data'] = resp.text
        return self.test_data

    # 对比返回结果
    def compareResponse(self):
        for key, value in self.test_data.items():
            real_resp = value['response']
            pre_resp = value['predict_response']
            self.assertMultiLineEqual(real_resp['statusCode'], pre_resp['statusCode'], '接口访问状态测试未通过')
            if pre_resp['data'] is None:
                self.assertIsNone(real_resp['data'], '接口返回[data]测试不通过')
            else:
                real_data = real_resp['data']
                pre_resp = pre_resp['data']
                self.assertMultiLineEqual(real_data['code'], pre_resp['code'], r'接口返回[code]测试不通过')

        return self.test_data


if __name__ == '__main__':
    unittest.main()
