# -*- coding: utf-8 -*-
# 多进程-协程模型： 单独用协程并不是最高效
# 为什么不用线程和协程结合？多线程Cpython会有GIL锁
import asyncio
import datetime
import os
import time
from multiprocessing import Pool


async def test(time):
    # 异步 所以 2500个协程只耗时1s 遇到io阻塞就切换做其他事情
    await asyncio.sleep(time)


async def main(num):
    start_time = datetime.datetime.now()
    tasks = [asyncio.create_task(test(1)) for _ in range(num)]
    # print(f"task len {len(tasks)}")
    [await t for t in tasks]
    end_time = datetime.datetime.now()
    print(f"process id {os.getpid()} start_time = {start_time.strftime('%Y-%m-%d %H:%M:%S')} end_time = {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")


def run(num):
    asyncio.run(main(num))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    p = Pool()
    # 多进程
    for i in range(4):
        # 异步启动进程 -> 4个进程只耗时一个进程的时间
        # p.apply_async(run, args=(2500,))

        # 同步启动进程 -> 一个进程完成才会触发下一个进程
        p.apply(run, args=(2500,))
    p.close()
    p.join()
    end_time = datetime.datetime.now()
    print(f"start_time = {start_time.strftime('%Y-%m-%d %H:%M:%S')} end_time = {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
