import bech32
# def node_id_to_address(node_id):
#     hrp = 'sm'
#     data = bytes.fromhex(node_id)
#     converted_data = bech32.convertbits(data, 8, 5)  # 将字节数据从 8 位转换为 5 位
#     return bech32.bech32_encode(hrp, converted_data)
#
# def address_to_node_id(address):
#     pass
#
#
#
# import bech32
#
# # 输入原始数据和人类可读部分
# hrp = "sm"
# data = "qqqqqza0ppemf98djf65jrpdsm3lnw05xtc6kg70vkxl"
# address = 'sm1qqqqqq97ygsmk5nsa4uy5vztgq2tj5fkpknjrrcxl37cu'
#
# encoded_data = bech32.decode(hrp,address)
# # encoded_data = bech32.convertbits(encoded_data,5,8)
# print(encoded_data)
# print(bytes.hex(bytes(encoded_data)))


#
# # 生成Bech32地址的校验和
# checksum = bech32.create_checksum(hrp, decoded_data)
#
# # 添加校验和
# encoded_address = bech32.bech32_encode(hrp, decoded_data + checksum)
#
# # 添加5个零作为前缀
# bech32_address_with_zeros = "00000" + encoded_address
#
# print(bech32_address_with_zeros)


xxx = b'���7�N�w�}�#1�I�^�l�.C9���dpg'

print(xxx.hex())

