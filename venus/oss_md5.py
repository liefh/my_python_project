
import oss2

def oss_file_md5(endpoint,bucket_name,object_name):

    endpoint = endpoint
    bucket_name = bucket_name
    object_name = object_name

    # 设置 OSS 访问参数
    auth = oss2.Auth('LTAI5tQxr1wiiX7Rm9pSANvq', 'BCOwbbdZgbsTIOmjKPGIHdOSEyZjaK')
    bucket = oss2.Bucket(auth,endpoint,bucket_name)


    # 创建 OSS 对象实例
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # 获取文件内容并计算哈希值
    # object_stream = bucket.get_object(object_name)

    object_meta = bucket.get_object_tagging(object_name)
    print(object_meta.headers)
    # hash = oss2.utils.content_md5(object_stream)
    #
    #
    #
    # # 打印哈希值
    # print("File hash:", hash)



endpoint = 'http://oss-accelerate.aliyuncs.com'
bucket_name = 'ipfs-actor-cluster'
object_name = 'venus/auto-test/nv19_binaries/venus'

oss_file_md5(endpoint,bucket_name,object_name)