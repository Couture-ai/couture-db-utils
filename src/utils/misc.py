import lz4
import orjson


def decode_response(input_string):
    try:
        decompressed = lz4.frame.decompress(input_string)
        parsed = orjson.loads(decompressed)
        return parsed
    except Exception as e:
        print(f"Decode error: {e}")
        return input_string
