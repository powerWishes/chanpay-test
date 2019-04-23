import re
import uuid

UNKNOW = 0
METHOD = 1  # __abc(a,b)__
REQ_PARAM = 2  # _a_
SPECIAL_PARAM = 3  # *None*


# 自定义方法
class ParamUtil:
    # 创建无“-”UUID
    def createEasyUuid(self, len='32'):
        return str(uuid.uuid1()).replace('-', '')[:int(len)]

    # 创建有“-”UUID
    def createUuid(self, len='36'):
        return str(uuid.uuid1())[:int(len)]

    # 校验param是否以a开头
    def checkStartWith(self, param, a):
        return param.startswith(a)

# 解析参数，即自定义方法调用
# param 需解析的字符串
# data 方法调用的额外参数，最终会拼在请求参数的头部
def analysis_param(param, *data):
    kwtype = get_keyword_type(param)
    if UNKNOW == kwtype:
        return param
    if METHOD == kwtype:
        paramUtil = ParamUtil()
        method_name = get_method_name(param)
        params = get_args(param)
        if len(data) > 0:
            params = data + params
        method = None
        if method_name is not None and hasattr(paramUtil, method_name):
            method = getattr(paramUtil, method_name)
        else:
            raise Exception('该自定义方法不存在')
        if method_name == 'createEasyUuid':
            if params is None:
                return method()
            else:
                return method(params[0])
        elif method_name == 'createUuid':
            if params is None:
                return method()
            else:
                return method(params[0])
        elif method_name == 'checkStartWith':
            if params is None:
                return method()
            else:
                return method(params[0], params[1])
        else:
            raise Exception('该自定义方法不存在')
    if REQ_PARAM == kwtype:
        pass
    if SPECIAL_PARAM == kwtype:
        pass

    # 方法获取
    if param.startswith('__') and param.endswith("__"):
        paramUtil = ParamUtil()
        # 参数获取
        param_list = param.split()
        if hasattr(paramUtil, 'createRadomUuid'):
            a = getattr(paramUtil, 'createRadomUuid')  # 如果有方法method，否则打印其地址，否则打印default
            print(a(16))


def is_keyword(param):
    if type(param) != type(''):
        return False
    if param.startswith('__') and param.endswith("__"):
        return True
    if param.startswith('_') and param.endswith("_"):
        return True
    if param.startswith('*') and param.endswith("*"):
        return True
    return False


# 获取请求参数
# 返回格式:
# ['str1','str2'...]
# 注意:无请求参数返回None
def get_args(param):
    # 正则匹配参数
    paramsstr = re.search(r'\(.*\)', param)
    if paramsstr is None:
        return None
    # 参数字符串截取
    index = paramsstr.span()
    realparamsstr = param[(index[0] + 1):(index[1] - 1)]
    # 获取参数列表
    paramslist = realparamsstr.split(',')
    return paramslist


# 获取请求参数
# 返回格式:
# 'methodName'
# 注意:无方法名返回None
def get_method_name(param):
    # 正则匹配参数
    paramsstr = re.search(r'__.*\(', param)
    if paramsstr is None:
        return None
    # 参数字符串截取
    index = paramsstr.span()
    method_name = param[(index[0] + 2):(index[1] - 1)]
    return method_name


def get_keyword_type(param):
    if type(param) != type(''):
        return UNKNOW
    if param.startswith('__') and param.endswith("__"):
        return METHOD
    if param.startswith('_') and param.endswith("_"):
        return REQ_PARAM
    if param.startswith('*') and param.endswith("*"):
        return SPECIAL_PARAM
    return UNKNOW


def a(*alist):
    b = len(alist)
    print(b)


if __name__ == '__main__':
    a()
