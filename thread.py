from fastapi import FastAPI
import threading
import random
import time
import os
from pydantic import BaseModel
from time import sleep, ctime
from random import randrange
from fastapi import APIRouter
router = APIRouter()


@router.get("/thread1_1/{num_threads}")#چاپ پیغام ها ب ترتیب
async def scenario1(num_threads: int):
    messages = []

    def my_func(thread_number):
        messages.append(f"my_func called by thread N°{thread_number}")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=my_func, args=(i,))
        threads.append(thread)

    for thread in threads:
        thread.start()
        thread.join()

    return {"messages": messages}


@router.get("/thread1_2/{num_threads}")#چاپ پیغام ها رندوم
async def scenario2(num_threads: int):
    messages = []

    def my_func(thread_number):
        time.sleep(random.random())
        messages.append(f"my_func called by thread N°{thread_number}")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=my_func, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {"messages": messages}


@router.get("/thread1_3")#چاپ پیغام ها بطور معکوس
async def scenario3():
    messages = []
    def my_func(thread_number, delay):
        time.sleep(delay)
        messages.append(f"my_func called by thread N°{thread_number}")
    thread0 = threading.Thread(target=my_func, args=(0,0.1))
    thread1 = threading.Thread(target=my_func, args=(1,0.09))
    thread2 = threading.Thread(target=my_func, args=(2,0.08))
    thread3 = threading.Thread(target=my_func, args=(3,0.07))
    thread4 = threading.Thread(target=my_func, args=(4,0.06))
    thread5 = threading.Thread(target=my_func, args=(5,0.05))
    thread6 = threading.Thread(target=my_func, args=(6,0.04))
    thread7 = threading.Thread(target=my_func, args=(7,0.03))
    thread8 = threading.Thread(target=my_func, args=(8,0.02))
    thread9 = threading.Thread(target=my_func, args=(9,0.01))
    thread0.start()
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread0.join()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()

    return {"messages": messages}



@router.get("/thread2_1")#ابتدا نخ ها به ترتیب شروع شوند. سپس نخ ها به همان ترتیب تمام شوند.
async def scenario1():
    messages = []
    def function_A():
        messages.append(f"{threading.current_thread().name} --> function_A starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_A exiting")
    def function_B():
        messages.append(f"{threading.current_thread().name} --> function_B starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_B exiting")
    def function_C():
        messages.append(f"{threading.current_thread().name} --> function_C starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_C exiting")

    thread_A = threading.Thread(target=function_A, name="Thread-A")
    thread_B = threading.Thread(target=function_B, name="Thread-B")
    thread_C = threading.Thread(target=function_C, name="Thread-C")

    thread_A.start()
    thread_B.start()
    thread_C.start()

    thread_A.join()
    thread_B.join()
    thread_C.join()

    return {"messages": messages}

@router.get("/thread2_2")#هرنخ بعد از اتمام نخ قبل شروع شود
async def scenario2():
    messages = []
    def function_A():
        messages.append(f"{threading.current_thread().name} --> function_A starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_A exiting")
    def function_B():
        messages.append(f"{threading.current_thread().name} --> function_B starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_B exiting")
    def function_C():
        messages.append(f"{threading.current_thread().name} --> function_C starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_C exiting")
    thread_A = threading.Thread(target=function_A, name="Thread-A")
    thread_B = threading.Thread(target=function_B, name="Thread-B")
    thread_C = threading.Thread(target=function_C, name="Thread-C")
    thread_A.start()
    thread_A.join()

    thread_B.start()
    thread_B.join()

    thread_C.start()
    thread_C.join()
    return {"messages": messages}


@router.get("/thread2_3")#ابتدا نخ اول شروع و تمام شود. بعد نخ دو وسه شروع شوند. بعد نخ دو و سه تمام شوند.
async def scenario3():
    messages = []
    def function_A():
        messages.append(f"{threading.current_thread().name} --> function_A starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_A exiting")
    def function_B():
        messages.append(f"{threading.current_thread().name} --> function_B starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_B exiting")
    def function_C():
        messages.append(f"{threading.current_thread().name} --> function_C starting")
        time.sleep(1)
        messages.append(f"{threading.current_thread().name} --> function_C exiting")
    thread_A = threading.Thread(target=function_A, name="Thread-A")
    thread_B = threading.Thread(target=function_B, name="Thread-B")
    thread_C = threading.Thread(target=function_C, name="Thread-C")
    thread_A.start()
    thread_A.join()
    thread_B.start()
    thread_C.start()
    thread_B.join()
    thread_C.join()
    return {"messages": messages}


@router.get("/thread3_1/{num_threads}")#ابتدا شروع تمام نخ ها تصادفی و سپس پایان تمام نخ ها تصادفی
async def scenario1(num_threads: int):
    messages = []

    class MyThread(threading.Thread):
        def __init__(self, thread_number, delay):
            threading.Thread.__init__(self)
            self.thread_number = thread_number
            self.delay = delay

        def run(self):
            time.sleep( random.randint(1, 3))
            messages.append(f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}")
            time.sleep(self.delay)
            messages.append(f"---> Thread#{self.thread_number} over")

    start_time = time.time()
    threads = [MyThread(thread_number, random.randint(4, 6)) for thread_number in range(1, num_threads + 1)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    messages.append(f"--- {end_time - start_time} seconds ---")

    return {'messages': messages}

@router.get("/thread3_2")#ابتدا 5نخ اول شروع شوند و بعد همان پنج نخ تمام شوند.سپس 4نخ بعد شروع شوند.و بعد همان 4نخ تمام شوند
async def scenario2():
    messages = []

    class MyThread(threading.Thread):
        def __init__(self, thread_number, delay):
            threading.Thread.__init__(self)
            self.thread_number = thread_number
            self.delay = delay

        def run(self):
            messages.append(f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}")
            time.sleep(self.delay)
            messages.append(f"---> Thread#{self.thread_number} over")

    start_time = time.time()
    thread1 = MyThread(1, 0.01)
    thread2 = MyThread(2, 0.02)
    thread3 = MyThread(3, 0.03)
    thread4 = MyThread(4,0.04)
    thread5 = MyThread(5,0.05)
    thread6 = MyThread(6, 0.01)
    thread7 = MyThread(7,0.02)
    thread8 = MyThread(8,0.03)
    thread9 = MyThread(9, 0.04)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()

    end_time = time.time()
    messages.append(f"--- {end_time - start_time} seconds ---")

    return {'messages': messages}

@router.get("/thread3_3")#هر نخ بعد از اتمام نخ قبل شروع بشه
async def scenario3():
    messages = []

    class MyThread(threading.Thread):
        def __init__(self, thread_number, delay):
            threading.Thread.__init__(self)
            self.thread_number = thread_number
            self.delay = delay

        def run(self):
            messages.append(f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}")
            time.sleep(self.delay)
            messages.append(f"---> Thread#{self.thread_number} over")

    start_time = time.time()
    thread1 = MyThread(1, 1)
    thread2 = MyThread(2, 1)
    thread3 = MyThread(3, 1)
    thread4 = MyThread(4, 1)
    thread5 = MyThread(5,1)
    thread6 = MyThread(6, 1)
    thread7 = MyThread(7, 1)
    thread8 = MyThread(8, 1)
    thread9 = MyThread(9,1)

    thread1.start()
    thread1.join()
    thread2.start()
    thread2.join()
    thread3.start()
    thread3.join()
    thread4.start()
    thread4.join()
    thread5.start()
    thread5.join()
    thread6.start()
    thread6.join()
    thread7.start()
    thread7.join()
    thread8.start()
    thread8.join()
    thread9.start()
    thread9.join()

    end_time = time.time()
    messages.append(f"--- {end_time - start_time} seconds ---")

    return {'messages': messages}

@router.get("/thread4_1/{num_threads}")#اجرای  نخ ها کاملا به ترتیب
async def scenario1(num_threads: int):
    messages = []
    lock = threading.Lock()

    class MyThread(threading.Thread):
        def __init__(self, thread_number, delay):
            threading.Thread.__init__(self)
            self.thread_number = thread_number
            self.delay = delay

        def run(self):
            with lock:
                messages.append(f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}")
                time.sleep(self.delay)
                messages.append(f"---> Thread#{self.thread_number} over")

    threads = [MyThread(thread_number, random.randint(1, 5)) for thread_number in range(1, num_threads + 1)]

    start_time = time.time()
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    messages.append(f"--- {end_time - start_time} seconds ---")

    return {'messages': messages}


@router.get("/thread4_2/{num_threads}")#ابتدا شروع تمام نخ ها به ترتیب و سپس پایان تمام نخ ها به ترتیب
async def scenario2(num_threads: int):
    messages = []
    lock = threading.Lock()

    class MyThread(threading.Thread):
        def __init__(self, thread_number, delay):
            threading.Thread.__init__(self)
            self.thread_number = thread_number
            self.delay = delay

        def run(self):
                messages.append(f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}")
                with lock:
                    time.sleep(self.delay)
                    messages.append(f"---> Thread#{self.thread_number} over")

    threads = [MyThread(thread_number, random.randint(1, 5)) for thread_number in range(1, num_threads + 1)]

    start_time = time.time()
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    messages.append(f"--- {end_time - start_time} seconds ---")
    return {'messages': messages}

@router.get("/thread4_3/{num_threads}")#ابتدا شروع تمام نخ ها تصادفی و سپس پایان تمام نخ ها دقیقا به همان ترتیب تصادفی قبلی
async def scenario3(num_threads: int):
    messages = []
    lock = threading.Lock()

    class MyThread(threading.Thread):
        def __init__(self, thread_number, delay):
            threading.Thread.__init__(self)
            self.thread_number = thread_number
            self.delay = delay

        def run(self):
            time.sleep( random.randint(1, 3))
            messages.append(f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}")
            with lock:
                time.sleep(self.delay)
                messages.append(f"---> Thread#{self.thread_number} over")

    threads = [MyThread(thread_number, random.randint(4, 6)) for thread_number in range(1, num_threads + 1)]

    start_time = time.time()
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    messages.append(f"--- {end_time - start_time} seconds ---")
    return {'messages': messages}




class Items(BaseModel):
    adder_items: int
    remover_items: int
@router.post("/thread5_1")#اجرای یک در میان افزایش و کاهش
async def scenario1(items: Items):
    messages = []
    class Box:
        def __init__(self):
            self.lock = threading.RLock()
            self.total_items = 0
        def execute(self, value):
            with self.lock:
                self.total_items += value
        def add(self):
            with self.lock:
                self.execute(1)
        def remove(self):
            with self.lock:
                self.execute(-1)
    def adder(box, items):
        messages.append(f"N° {items} items to ADD")
        while items:
            box.add()
            time.sleep(1)
            items -= 1
            messages.append(f"ADDED one item -->{items} item to ADD")
    def remover(box, items):
        messages.append(f"N° {items} items to REMOVE".format(items))
        while items:
            box.remove()
            time.sleep(1)
            items -= 1
            messages.append(f"REMOVED one item -->{items} item to REMOVE")
    box = Box()
    t1 = threading.Thread(target=adder, args=(box,items.adder_items))
    t2 = threading.Thread(target=remover, args=(box, items.remover_items))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return {'messages': messages, 'total_items': box.total_items}

@router.post("/thread5_2")#هر سه بار افزایش،یک کاهش
async def scenario2(items: Items):
    messages = []
    class Box:
        def __init__(self):
            self.lock = threading.RLock()
            self.total_items = 0
        def execute(self, value):
            with self.lock:
                self.total_items += value
        def add(self):
            with self.lock:
                self.execute(1)
        def remove(self):
            with self.lock:
                self.execute(-1)
    def adder(box, items):
        messages.append(f"N° {items} items to ADD")
        while items:
            box.add()
            time.sleep(1)
            items -= 1
            messages.append(f"ADDED one item -->{items} item to ADD")
    def remover(box, items):
        messages.append(f"N° {items} items to REMOVE".format(items))
        while items:
            box.remove()
            time.sleep(3)
            items -= 1
            messages.append(f"REMOVED one item -->{items} item to REMOVE")
    box = Box()
    t1 = threading.Thread(target=adder, args=(box,items.adder_items))
    t2 = threading.Thread(target=remover, args=(box, items.remover_items))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return {'messages': messages, 'total_items': box.total_items}


@router.post("/thread5_3")#ابتدا تمام افزایش ها انجام شوند و بعد تمام کاهش ها
async def scenario1(items: Items):
    messages = []
    class Box:
        def __init__(self):
            self.lock = threading.RLock()
            self.total_items = 0
        def execute(self, value):
            with self.lock:
                self.total_items += value
        def add(self):
            with self.lock:
                self.execute(1)
        def remove(self):
            with self.lock:
                self.execute(-1)
    def adder(box, items):
        messages.append(f"N° {items} items to ADD")
        while items:
            box.add()
            time.sleep(1)
            items -= 1
            messages.append(f"ADDED one item -->{items} item to ADD")
    def remover(box, items):
        messages.append(f"N° {items} items to REMOVE".format(items))
        while items:
            box.remove()
            time.sleep(1)
            items -= 1
            messages.append(f"REMOVED one item -->{items} item to REMOVE")
    box = Box()
    t1 = threading.Thread(target=adder, args=(box,items.adder_items))
    t2 = threading.Thread(target=remover, args=(box, items.remover_items))
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    return {'messages': messages, 'total_items': box.total_items}



class Items(BaseModel):
    number_of_steps: int
@router.post("/thread6_1")#اجرای یک در میان تولید و مصرف کننده
def scenario1(items: Items):
    semaphore = threading.Semaphore(0)
    item = 0
    messages = []
    def consumer():
        nonlocal item
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name}INFO Consumer is waiting")
        semaphore.acquire()
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')}{threading.current_thread().name} INFO Consumer notify: item number {item}")
    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name}INFO Producer notify: item number {item}")
        semaphore.release()
    for i in range(items.number_of_steps):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    return {"messages": messages}


@router.post("/thread6_2")#برداشتن جوین ها و انتظار همیشگی مصرف کننده به اندازه گام ها
def scenario2(items: Items):
    semaphore = threading.Semaphore(0)
    item = 0
    messages = []
    def consumer():
        nonlocal item
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name}INFO Consumer is waiting")
        semaphore.acquire()
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')}{threading.current_thread().name} INFO Consumer notify: item number {item}")
    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name}INFO Producer notify: item number {item}")
        semaphore.release()
    for i in range(items.number_of_steps):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)
        t1.start()
        t2.start()
    return {"messages": messages}



@router.post("/thread6_3")#اجرای متوالی تولید کننده و از دست رفتن محتوای ایتم قبل از مصرف
def scenario3(items: Items):
    semaphore = threading.Semaphore(0)
    item = 0
    messages = []
    def consumer():
        nonlocal item
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer is waiting")
        semaphore.acquire()
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer notify: item number {item}")
    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        messages.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Producer notify: item number {item}")
        semaphore.release()
    # تولید کننده همه آیتم ها را تولید میکند به اندازه تعداد مراحل
    for i in range(items.number_of_steps):
        t2 = threading.Thread(target=producer)
        t2.start()
        t2.join()
    # مصرف کننده  آیتم نهایی را مصرف میکند به اندازه تعداد مراحل
    for i in range(items.number_of_steps):
        t1 = threading.Thread(target=consumer)
        t1.start()
        t1.join()
    return {"messages": messages}



@router.post("/thread7_1")#تمام دوندگان با ترتیب تصادفی ب مانع برسند.
def scenario1():
    num_runners = 3
    finish_line = threading.Barrier(num_runners)
    runners = ['Huey', 'Dewey', 'Louie']
    messages = []
    def runner():
        nonlocal messages
        name = runners.pop()
        sleep(randrange(2, 5))
        messages.append( f'{name} reached the barrier at: {ctime()}')
        finish_line.wait()
    threads = []
    messages.append('START RACE!!!!')
    for i in range(num_runners):
        threads.append(threading.Thread(target=runner))
        threads[-1].start()

    for thread in threads:
        thread.join()
    messages.append('Race over!')
    return {"messages": messages}


@router.post("/thread7_2")#دوندگان به ترتیب شروعی که دارند، به مانع میرسند(یعنی از اخر لیست به اول)
def scenario2():
    num_runners = 3
    finish_line = threading.Barrier(num_runners)
    runners = ['Huey', 'Dewey', 'Louie']
    messages = []
    lock = threading.Lock()
    def runner():
        nonlocal messages
        name = runners.pop()
        with lock:
            sleep(randrange(1, 5))
            messages.append(f'{name} reached the barrier at: {ctime()}')

        finish_line.wait()
    threads = []
    messages.append('START RACE!!!!')
    for i in range(num_runners):
        threads.append(threading.Thread(target=runner))
        threads[-1].start()
    for thread in threads:
        thread.join()
    messages.append('Race over!')
    return {"messages": messages}


@router.post("/thread7_3")#دوندگان هم زمان به مانع میرسند
def scenario3():
    num_runners = 3
    finish_line = threading.Barrier(num_runners)
    runners = ['Huey', 'Dewey', 'Louie']
    messages = []
    lock = threading.Lock()
    def runner():
        nonlocal messages
        name = runners.pop()
        sleep(randrange(2, 5))
        finish_line.wait()
        now = ctime()
        messages.append(f'{name} reached the barrier at: {now}')
    threads = []
    messages.append('START RACE!!!!')
    for i in range(num_runners):
        threads.append(threading.Thread(target=runner))
        threads[-1].start()
    for thread in threads:
        thread.join()
    messages.append('Race over!')
    return {"messages": messages}

