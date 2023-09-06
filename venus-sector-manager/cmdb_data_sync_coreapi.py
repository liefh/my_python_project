import coreapi

client = coreapi.Client()
schema = client.get("http://47.98.223.69/api-docs")


action = ["api", "v1 > data > miners_info > list"]
params = {
    "search": '*',
    "ordering": '',
}
result = client.action(schema, action, params=params)
print(result)