import redis
from django.http import JsonResponse
from django.shortcuts import render
import hashlib

def redis_():
    conn = redis.Redis(host='47.107.175.211', port=6379)
    conn.set('count', 0)
    with conn.pipeline() as pipe:
        # 先监视，自己的值没有被修改过
        conn.watch('count')

        # 事务开始
        pipe.multi()
        old_count = conn.get('count')
        count = int(old_count)
        if count > 0:  # 有库存
            pipe.set('count', count + 1)

        # 执行，把所有命令一次性推送过去
        pipe.execute()

def convert(num):
    all_charts ='12yhn34qazws567XEDCRF89UJMI0xedcrfvtgbujmikolpQAZWSVTGBYHNKLOP'
    digits = []
    while num > 0:
        digits.insert(0, all_charts[num%62])
        num //= 62
    return ''.join(digits)


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def to_link(request):
    if request.method == 'POST':
        conn = redis.Redis(host='47.107.175.211', port=6379)
        custom_key = request.POST.get('custom_key', '')
        url = request.POST.get('url', '')
        print(custom_key, url)
        if custom_key:
            m2 = hashlib.md5()
            m2.update(custom_key.encode('utf-8'))
            key = m2.hexdigest()[:5]
            conn.set(key, url)
        else:

            num = int(conn.get('num'))
            key = convert(num + 1238328)
            conn.set(key, url)
            conn.set('num', num+1)
        return JsonResponse({'msg':key})


def to(request):
    if request.method == 'GET':
        key = request.GET.get('url')
        conn = redis.Redis(host='47.107.175.211', port=6379)
        url = conn.get(key).decode('utf-8')
        return JsonResponse({'url': url})
