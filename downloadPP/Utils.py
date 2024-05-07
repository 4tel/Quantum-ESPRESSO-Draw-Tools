from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from time import time
        start_time = time()  # 시작 시간 측정
        result = func(*args, **kwargs)  # 원래 함수 실행
        end_time = time()  # 종료 시간 측정
        print(f"{func.__name__} 함수 실행 시간: {end_time - start_time}초")
        return result
    return wrapper
