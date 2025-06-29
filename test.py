import requests

res = requests.get("http://localhost:5600/api/0/buckets")
buckets = res.json()

print("=== 使用可能なバケットID ===")
for bucket_id in buckets:
    print(bucket_id)

