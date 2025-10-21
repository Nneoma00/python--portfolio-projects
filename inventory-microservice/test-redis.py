from redis_om import get_redis_connection


try:
    print("Connecting to Redis...")
    redis = get_redis_connection(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        password=os.getenv("REDIS_PASS"),
        decode_responses=True
    )


    print(redis.ping())  # should return True

except Exception as e:
    print("Connection failed.")
    print(e)

