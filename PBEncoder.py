from google.protobuf.internal.decoder import ReadTag
from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal.decoder import wire_format
from google.protobuf.internal.decoder import _DecodeFixed64
from google.protobuf.internal.decoder import _DecodeFixed32
from google.protobuf.internal.decoder import _DecodeUnknownFieldSet
from google.protobuf.internal.decoder import _DecodeError
from google.protobuf.internal.decoder import _DecodeVarint32


def encode_varint(value):
    # 编码Varint整数
    result = bytearray()
    while True:
        if value < 0x80:
            result.append(value)
            break
        else:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
    return result

def encode_field(tag, wire_type, value):
    encoded_tag = encode_varint((tag << 3) | wire_type)
    if wire_type == 0:
        encoded_value = encode_varint(value)
    elif wire_type == 1:
        encoded_value = value.to_bytes(8, byteorder='little')
    elif wire_type == 2:
        encoded_length = encode_varint(len(value))
        encoded_value = encoded_length + value
    return (encoded_tag + encoded_value).hex()

def GenerateProto(input):
    input = memoryview(bytes.fromhex(input))
    pos = 0
    ProtoAll = {}
    ProtoBuf = '# 自动生成ProtoBuf组包代码\n'
    ProtoBuf += 'ProtoBuf = ""\n'
    while len(input.tobytes()) is None or pos < len(input.tobytes()):
        (tag_bytes, pos) = ReadTag(input, pos)
        (tag, _) = _DecodeVarint(tag_bytes, 0)
        field_number, wire_type = wire_format.UnpackTag(tag)
        if tag == 0 or wire_type == wire_format.WIRETYPE_END_GROUP:
            raise _DecodeError('Decrypt Done')
        if wire_type == wire_format.WIRETYPE_END_GROUP:
            break
        if wire_type == wire_format.WIRETYPE_VARINT:
            (data, pos) = _DecodeVarint(input, pos)
            ProtoBuf += "ProtoBuf += encode_field(field_number, wire_type, data)".replace("field_number", str(field_number)).replace("wire_type",str(wire_type)).replace("data",str(data)) +"\n"
            # ProtoBuf += encode_field(field_number, wire_type, data).hex()
            ProtoAll[str(field_number)] = str(data)
        elif wire_type == wire_format.WIRETYPE_FIXED64:
            (data, pos) = _DecodeFixed64(input, pos)
            ProtoBuf += "ProtoBuf += encode_field(field_number, wire_type, data)".replace("field_number", str(field_number)).replace("wire_type",str(wire_type)).replace("data",str(data)) +"\n"
            ProtoAll[str(field_number)] = str(data)
        elif wire_type == wire_format.WIRETYPE_FIXED32:
            (data, pos) = _DecodeFixed32(input, pos)
            ProtoBuf += "ProtoBuf += encode_field(field_number, wire_type, data)".replace("field_number", str(field_number)).replace("wire_type",str(wire_type)).replace("data",str(data)) +"\n"
            ProtoAll[str(field_number)] = str(data)
        elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
            (size, pos) = _DecodeVarint32(input, pos)
            data = input[pos:pos + size].tobytes()
            ProtoBuf += "ProtoBuf += encode_field(field_number, wire_type, data)".replace("field_number", str(field_number)).replace("wire_type",str(wire_type)).replace("data",str(data)) +"\n"
            pos += size
        elif wire_type == wire_format.WIRETYPE_START_GROUP:
            (data, pos) = _DecodeUnknownFieldSet(input, pos)
            ProtoBuf += "ProtoBuf += encode_field(field_number, wire_type, data)".replace("field_number", str(field_number)).replace("wire_type",str(wire_type)).replace("data",str(data)) +"\n"
        elif wire_type == wire_format.WIRETYPE_END_GROUP:
            return (0, -1)
        else:
            raise _DecodeError('Wrong wire type in tag.')
    return ProtoBuf


