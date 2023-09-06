import  toml

# vsm_cfg = toml.load('./sector-manager.cfg')
# vsm_cfg = toml.load('./worker_config.toml')
vsm_cfg = toml.load('./test.toml')
print(vsm_cfg)
# print(vsm_cfg.keys())

# def print_dict_keys(d, prefix='worker'):
#     for key, value in d.items():
#         full_key = f"{prefix}.{key}" if prefix else key
#         print(full_key)
#         if isinstance(value, dict):
#             print_dict_keys(value, full_key)

# 打印字典所有层级的键
# print_dict_keys(vsm_cfg)
