from PBDecoder import *
from PBEncoder import *

if __name__ == '__main__':
    Pb = "08C45E1218E5B7B2E59CA8E585B6E4BB96E59CB0E696B9E799BBE5BD95"
    print(parseByGoogle(Pb)["2"],parseByGoogle(Pb)["2"])  # 解析ProtoBuf
    print(GenerateProto(Pb))  # 生成ProtoBuf

    # 自动生成ProtoBuf组包代码
    ProtoBuf = ""
    ProtoBuf += encode_field(1, 0, 12100)
    ProtoBuf += encode_field(2, 2,
                             b'\xe5\xb7\xb2\xe5\x9c\xa8\xe5\x85\xb6\xe4\xbb\x96\xe5\x9c\xb0\xe6\x96\xb9\xe7\x99\xbb\xe5\xbd\x95')

    print("ProtoBuf组包结果",ProtoBuf)
