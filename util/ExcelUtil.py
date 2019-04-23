import xlrd

from util import DataConvertUtil, WorkspaceUtil

head_map = {0: "request", 1: "predict_response", 2: "predict_db_data", 3: "response", 4: "db_data",
            5: "start_params"}
excel_cols = 6


# 从Excel读取测试用例
# 返回数据格式:
# [{'request': '{"accUserNo":"4000","trxChnNo":"2100","trxTyp":"1201","trxId":"17b80f1d1f75adeb","trxAmt":0.01,"mrchntNo":"__createRadomUuid(16)__","mrchntNm":"刘无媚-页面新增企业商户","productDesc":"自动化测试用例1"}',
# 'predict_response': '{"code":"000000","message":"SUCCESS","data":{"rpCd":"000000","rpDesc":"SUCCESS","qrCodeInfo":"__checkStartWith(https://)__"}}',
# 'predict_db_data': '',
# 'response': '',
# 'db_data': '',
# 'start_params': '{"db_search_delay_seconds":0}',
# 'id': 1}]
def read_testdata_by_excel(file_path_name):
    # 打开文件
    global workbook
    try:
        workbook = xlrd.open_workbook(file_path_name)
    except BaseException as e:
        print("Read Excel Error:", e)
        raise e
    # 获取sheet
    sheet_count = workbook.nsheets
    # 选择页数检查
    if sheet_count < 1:
        raise Exception("该Excel内容为空，或页数不存在！")
    sheet = workbook.sheet_by_index(0)
    # 选择开始行检查
    row_count = sheet.nrows
    if row_count < 1:
        raise Exception("起始行数据不存在！")
    col_count = sheet.ncols
    if col_count < 1:
        raise Exception("起始列数据不存在！")

    data = []  # 总数据
    id = 1  # 为每一行生成一个id

    # 数据获取
    for rowNum in range(1, sheet.nrows):
        row = sheet.row(rowNum)
        row_map = {}  # 每行数据
        for colNum in range(0, excel_cols):
            row_map[head_map[colNum]] = row[colNum].value
        row_map['id'] = id
        id += 1
        data.append(row_map)
    return data


if __name__ == '__main__':
    print(read_testdata_by_excel(
        WorkspaceUtil.get_root_path() + '/resource/testdata/trans/gateway/qrcode/unionMainSweep.xlsx'))
