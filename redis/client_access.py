import redis

my_client = redis.StrictRedis(host="34.22.76.148", db="1")

my_client.sadd("yuhu", "haha")
item = my_client.get("yuhu")
print(item.title())


