from facade.enum.base import DataTypeEnum

def convert(param, dataType):
    try:
        if dataType is None:
            return param
        if param is None:
            return None
        if param == '':
            return None
        elif dataType == DataTypeEnum.BOOLEAN:
            return bool(param)
        elif dataType == DataTypeEnum.DOUBLE:
            return float(param)
        elif dataType == DataTypeEnum.INTEGER:
            return int(param)
        elif dataType == DataTypeEnum.LONG:
            return int(param)
        elif dataType == DataTypeEnum.STRING:
            return str(param)
        else:
            return param
    except Exception as e:
        raise Exception("数据转换错误，请检查数据类型列表或数据！")
