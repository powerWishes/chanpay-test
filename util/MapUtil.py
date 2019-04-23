from collections import OrderedDict


# 字典转化为排序字典OrderedDict()
def to_tree_map(normal_map):
    acs_keys = sorted(normal_map.keys())
    res_map = OrderedDict()
    for each in acs_keys:
        res_map[each] = normal_map[each]
    return res_map
