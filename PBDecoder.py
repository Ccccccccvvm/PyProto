from google.protobuf.internal.decoder import ReadTag
from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal.decoder import wire_format
from google.protobuf.internal.decoder import _DecodeFixed64
from google.protobuf.internal.decoder import _DecodeFixed32
from google.protobuf.internal.decoder import _DecodeUnknownFieldSet
from google.protobuf.internal.decoder import _DecodeError
from google.protobuf.internal.decoder import _DecodeVarint32



def parseByGoogle(input):
    input = memoryview(bytes.fromhex(input))
    pos = 0
    ProtoAll = {}
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
            ProtoAll[str(field_number)] = str(data)
        elif wire_type == wire_format.WIRETYPE_FIXED64:
            (data, pos) = _DecodeFixed64(input, pos)
            ProtoAll[str(field_number)] = str(data)
        elif wire_type == wire_format.WIRETYPE_FIXED32:
            (data, pos) = _DecodeFixed32(input, pos)
            ProtoAll[str(field_number)] = str(data)
        elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
            (size, pos) = _DecodeVarint32(input, pos)
            data = input[pos:pos + size].tobytes()
            try:
                ProtoAll[str(field_number)] = data.decode()
            except:
                ProtoAll[str(field_number)] = data.hex()
            pos += size
        elif wire_type == wire_format.WIRETYPE_START_GROUP:
            (data, pos) = _DecodeUnknownFieldSet(input, pos)
        elif wire_type == wire_format.WIRETYPE_END_GROUP:
            return (0, -1)
        else:
            raise _DecodeError('Wrong wire type in tag.')
    return ProtoAll


