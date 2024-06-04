from fastapi import FastAPI, APIRouter
import multiprocessing
import time
import random
from multiprocessing import Barrier, Lock
from datetime import datetime
router = APIRouter()

#مثال اول
def myFunc(i, messages):#هرفرایند کاامل اجرا شده و بعد نوبت به فرایند بعد میرسد
    messages.append('calling myFunc from process n°: %s' % i)
    for j in range(0, i):
        messages.append('output from myFunc is :%s' % j)
@router.get("/process1_1/{num_process}")
async def scenario1(num_process: int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    for i in range(num_process):
        process = multiprocessing.Process(target=myFunc, args=(i, messages))
        process.start()
        process.join()
    return {"messages": list(messages)}


@router.get("/process1_2/{num_process}")#فرایندها تصادفی اجرا میشوند(اما اجرای هر فرایند به طور کامل هست)
async def scenario2(num_process: int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    processs=[]
    for i in range(num_process):
        process = multiprocessing.Process(target=myFunc, args=(i, messages))
        processs.append(process)
        process.start()
    for process in processs:
        process.join()
    return {"messages": list(messages)}


def myFuncc(i, messages):#ابتدا بطور تصادفی پیغام اول برای فرایندها چاپ میشه.بعد بطور تصادفی پیغام های دوم برای فرایندها چاپ میشه
    messages.append('calling myFunc from process n°: %s' % i)
    time.sleep(random.uniform(0, 3))  # تاخیر تصادفی بین 0 تا 3 ثانیه
    for j in range(0, i):
        messages.append('output from myFunc is :%s' % j)
@router.get("/process1_3/{num_process}")
async def scenario3(num_process: int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    processs = []
    for i in range(num_process):
        process = multiprocessing.Process(target=myFuncc, args=(i, messages))
        process.start()
        processs.append(process)
    for process in processs:
        process.join()
    return {"messages": list(messages)}

#مثال دوم
def myFunc1(messages):#ابتدا پیغام شروع فرایندها چاپ میشود.سپس پیغام پایان فرایندها چاپ میشود
    name = multiprocessing.current_process().name
    messages.append("Starting process name = %s" % name)
    time.sleep(3)
    messages.append("Exiting process name = %s" % name)
@router.get("/process2_1/")
async def scenario1():
    manager = multiprocessing.Manager()
    messages = manager.list()
    process1 = multiprocessing.Process(name='myFunc process', target=myFunc1 , args=(messages,))
    process2 = multiprocessing.Process(target=myFunc1 ,args=(messages,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    return {"messages": list(messages)}

@router.get("/process2_2/")#اجرای هرفرایند بعد از اتمام فرایند قبل
async def scenario2():
    manager = multiprocessing.Manager()
    messages = manager.list()
    process1 = multiprocessing.Process(name='myFunc process', target=myFunc1 , args=(messages,))
    process2 = multiprocessing.Process(target=myFunc1 ,args=(messages,))
    process1.start()
    process1.join()
    process2.start()
    process2.join()
    return {"messages": list(messages)}

def myFunc2(messages,delay):# ابتدا پیغام شروع فرایندها چاپ میشود.سپس پیغام پایان فراینددوم چاپ شده(به علت اسلیپ کمتر)و سپس پیغام پایان فرایند اول
    name = multiprocessing.current_process().name
    messages.append("Starting process name = %s" % name)
    time.sleep(delay)
    messages.append("Exiting process name = %s" % name)
@router.get("/process2_3/")
async def scenario3():
    manager = multiprocessing.Manager()
    messages = manager.list()
    process1 = multiprocessing.Process(name='myFunc process', target=myFunc2 , args=(messages,2))
    process2 = multiprocessing.Process(target=myFunc2 ,args=(messages,1))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    return {"messages": list(messages)}

#مثال سوم
############################################################################## daemon
def foo(messages):
    name = multiprocessing.current_process().name
    messages.append("Starting %s " % name)
    if name == 'background_process':
        for i in range(0, 5):
            messages.append('---> %d ' % i)
        time.sleep(1)
    else:
        for i in range(5, 10):
            messages.append('---> %d ' % i)
        time.sleep(1)
    messages.append("Exiting %s " % name)
@router.get("/process3_1/")
async def scenario3():
    manager = multiprocessing.Manager()
    messages = manager.list()
    background_process = multiprocessing.Process (name='background_process',target=foo, args=(messages,))
    background_process.daemon= True
    NO_background_process = multiprocessing.Process (name='NO_background_process',target=foo,args=(messages,))
    NO_background_process.daemon = False
    background_process.start()
    NO_background_process.start()
    background_process.join()
    NO_background_process.join()
    return {"messages": list(messages)}


############################################################################## daemon
#مثال چهارم
def foo1(messages):#نشان دادن وضعیت فرایند و خاتمه دادن به ان
    messages.append('Starting function')
    for i in range(10):
        messages.append('-->%d\n' % i)
        time.sleep(1)
    messages.append('Finished function')
@router.get("/process4_1/")
async def scenario1():
    manager = multiprocessing.Manager()
    messages = manager.list()
    p = multiprocessing.Process(target=foo1, args=(messages,))
    messages.append(f'Process before execution: {p} {p.is_alive()}')
    p.start()
    messages.append(f'Process running: {p} {p.is_alive()}')
    p.terminate()
    messages.append(f'Process terminated: {p} {p.is_alive()}')
    p.join()
    messages.append(f'Process joined: {p} {p.is_alive()}')
    messages.append(f'Process exit code: {p.exitcode}')
    return {"messages": list(messages)}


@router.get("/process4_2/")# نشان دادن وضعیت فرایند و گذاشتن زمان انتظار بعد از خاتمه دادن
async def scenario2():
    manager = multiprocessing.Manager()
    messages = manager.list()
    p = multiprocessing.Process(target=foo1, args=(messages,))
    messages.append(f'Process before execution: {p} {p.is_alive()}')
    p.start()
    messages.append(f'Process running: {p} {p.is_alive()}')
    p.terminate()
    time.sleep(0.1)
    messages.append(f'Process terminated: {p} {p.is_alive()}')
    p.join()
    messages.append(f'Process joined: {p} {p.is_alive()}')
    messages.append(f'Process exit code: {p.exitcode}')
    return {"messages": list(messages)}


@router.get("/process4_3/")#نشان دادن وضعیت فرایند و  گذاشتن زمان انتظار قبل از خاتمه دادن به منظور فرصت دادن برای اجرای تابع
async def scenario3():
    manager = multiprocessing.Manager()
    messages = manager.list()
    p = multiprocessing.Process(target=foo1, args=(messages,))
    messages.append(f'Process before execution: {p} {p.is_alive()}')
    p.start()
    messages.append(f'Process running: {p} {p.is_alive()}')
    time.sleep(5)
    p.terminate()
    time.sleep(0.1)
    messages.append(f'Process terminated: {p} {p.is_alive()}')
    p.join()
    messages.append(f'Process joined: {p} {p.is_alive()}')
    messages.append(f'Process exit code: {p.exitcode}')
    return {"messages": list(messages)}


#مثال پنجم
class MyProcess(multiprocessing.Process):#تعریف فرایند به عنوان زیرکلاس با اجرای ترتیبی
    def __init__(self, messages):
        #multiprocessing.process.__init__(self)
        super().__init__()
        self.messages = messages
    def run(self):
        self.messages.append('called run method by %s' % self.name)
        return
@router.get("/process5_1/{num_process}")
async def scenario1(num_process:int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    for i in range(num_process):
        process = MyProcess(messages)
        process.start()
        process.join()
    return {"messages": list(messages)}


class MyProcesss(multiprocessing.Process):#اجرای تصادفی
    def __init__(self, messages):
        super().__init__()
        self.messages = messages
    def run(self):
        delay = random.randint(1, 5)
        time.sleep(delay)
        self.messages.append(f'called run method by {self.name}, delay={delay}')
        return
@router.get("/process5_2/{num_process}")
async def scenario2(num_process:int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    processs=[]
    for i in range(num_process):
        process = MyProcesss(messages)
        processs.append(process)
        process.start()
    for process in processs:
        process.join()
    return {"messages": list(messages)}


class MyProcessss(multiprocessing.Process):#اجرای ترتیبی(تفاوتش با سناریو اول:وجود اسلیپ که فقط زمان اجرا را زیاد کرده و اثر خاصی نداره)
    def __init__(self, messages):
        super().__init__()
        self.messages = messages
    def run(self):
        delay = random.randint(1, 5)
        time.sleep(delay)
        self.messages.append(f'called run method by {self.name}, delay={delay}')
        return
@router.get("/process5_3/{num_process}")
async def scenario3(num_process:int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    for i in range(num_process):
        process = MyProcessss(messages)
        process.start()
        process.join()
    return {"messages": list(messages)}

#مثال ششم
class producer(multiprocessing.Process):# بعد از هر دو الی 3تولید،یک مصرف داریم.تا موقعی که به ده تا تولید برسد و بعدازآن همش مصرف
    def __init__(self, queue,messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages
    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.messages.append("Process Producer : item %d appended to queue %s" % (item, self.name))
            time.sleep(1)
            self.messages.append("The size of queue is %s" % self.queue.qsize())
class consumer(multiprocessing.Process):
    def __init__(self, queue,messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages
    def run(self):
        while True:
            if (self.queue.empty()):
                self.messages.append("the queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                self.messages.append('Process Consumer : item %d popped from by %s '% (item, self.name))
                time.sleep(1)
@router.get("/process6_1/")
async def scenario1():
    manager = multiprocessing.Manager()
    messages = manager.list()
    queue = multiprocessing.Queue()
    process_producer = producer(queue,messages)
    process_consumer = consumer(queue,messages)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
    return {"messages": list(messages)}


class producer2(multiprocessing.Process):#اجرای یک درمیان تولیدو مصرف اما به طور نصفه.واز یه جایی به بعد فقط تولید میشه بدون مصرف
    def __init__(self, queue,messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages
    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.messages.append("Process Producer : item %d appended to queue %s" % (item, self.name))
            time.sleep(1)
            self.messages.append("The size of queue is %s" % self.queue.qsize())
class consumer2(multiprocessing.Process):
    def __init__(self, queue,messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages
    def run(self):
        while True:
            if (self.queue.empty()):
                self.messages.append("the queue is empty")
                break
            else:
                item = self.queue.get()
                self.messages.append('Process Consumer : item %d popped from by %s '% (item, self.name))
                time.sleep(1)
@router.get("/process6_2/")
async def scenario2():
    manager = multiprocessing.Manager()
    messages = manager.list()
    queue = multiprocessing.Queue()
    process_producer = producer2(queue,messages)
    process_consumer = consumer2(queue,messages)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
    return {"messages": list(messages)}


class producer3(multiprocessing.Process):#
    def __init__(self, queue,messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages
    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.messages.append("Process Producer : item %d appended to queue %s" % (item, self.name))
            time.sleep(1)
            self.messages.append("The size of queue is %s" % self.queue.qsize())
class consumer3(multiprocessing.Process):
    def __init__(self, queue,messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages
    def run(self):
        while True:
            if (self.queue.empty()):
                self.messages.append("the queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                self.messages.append('Process Consumer : item %d popped from by %s '% (item, self.name))
                time.sleep(1)
@router.get("/process6_3/")
async def scenario3():
    manager = multiprocessing.Manager()
    messages = manager.list()
    queue = multiprocessing.Queue()
    process_producer = producer3(queue,messages)
    process_consumer = consumer3(queue,messages)
    process_producer.start()
    process_producer.join()
    process_consumer.start()
    process_consumer.join()
    return {"messages": list(messages)}


#مثال هفتم
def test_with_barrier(synchronizer, serializer,messages):#برای فراینداول و دوم زمان برابر ثبت میشود اما برای فرایند 3و4 نه
    name = multiprocessing.current_process().name
    synchronizer.wait()
    now = time.time()
    with serializer:
        messages.append("process %s ----> %s"%(name,datetime.fromtimestamp(now)))
def test_without_barrier(messages):
    name = multiprocessing.current_process().name
    now = time.time()
    messages.append("process %s ----> %s"% (name, datetime.fromtimestamp(now)))
@router.get("/process7_1/")
async def scenario1():
    manager = multiprocessing.Manager()
    messages = manager.list()
    synchronizer = Barrier(2)
    serializer = Lock()
    p1 = multiprocessing.Process(name='p1 - test_with_barrier', target=test_with_barrier,args=(synchronizer, serializer, messages))
    p2 = multiprocessing.Process(name='p2 - test_with_barrier', target=test_with_barrier,args=(synchronizer, serializer, messages))
    p3 = multiprocessing.Process(name='p3 - test_without_barrier', target=test_without_barrier, args=(messages,))
    p4 = multiprocessing.Process(name='p4 - test_without_barrier', target=test_without_barrier, args=(messages,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    return {"messages": list(messages)}

@router.get("/process7_2/")#برای هر 4فرایند زمان یکسانی ثبت شود
async def scenario2():
    manager = multiprocessing.Manager()
    messages = manager.list()
    synchronizer = Barrier(4)
    serializer = Lock()
    p1 = multiprocessing.Process(name='p1 - test_with_barrier', target=test_with_barrier,args=(synchronizer, serializer, messages))
    p2 = multiprocessing.Process(name='p2 - test_with_barrier', target=test_with_barrier,args=(synchronizer, serializer, messages))
    p3 = multiprocessing.Process(name='p3 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, messages))
    p4 = multiprocessing.Process(name='p4 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, messages))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    return {"messages": list(messages)}


@router.get("/process7_3/")#دو فرایند اول هم زمان باشند و دو فرایند دوم نیز هم زمان  باشند
async def scenario3():
    manager = multiprocessing.Manager()
    messages = manager.list()
    synchronizer = Barrier(2)
    serializer = Lock()
    p1 = multiprocessing.Process(name='p1 - test_with_barrier', target=test_with_barrier,args=(synchronizer, serializer, messages))
    p2 = multiprocessing.Process(name='p2 - test_with_barrier', target=test_with_barrier,args=(synchronizer, serializer, messages))
    p3 = multiprocessing.Process(name='p3 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, messages))
    p4 = multiprocessing.Process(name='p4 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, messages))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    p3.start()
    p4.start()
    p3.join()
    p4.join()
    return {"messages": list(messages)}


#مثال هشتم
def function_square(data):#به توان 2 رساندن اعداد صفر تا99 از طریق pool
    result = data * data
    return result
@router.get("/process8_1/")
async def scenario1():
    inputs = list(range(0, 100))
    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    return {"pool:": str(pool_outputs)}

def f(data):#به علاوه ده کردن اعداد 0تا9
    result = data + 10
    return result
@router.get("/process8_2/")
async def scenario2():
    inputs = list(range(0, 10))
    pool = multiprocessing.Pool(processes=5)
    pool_outputs = pool.map(f, inputs)
    pool.close()
    return {"pool":str(pool_outputs)}


def first_char(data):#برگرداندن حرف اول چندتا رشته از طریق pool
    return data[0]
@router.get("/process8_3/")
async def scenario3():
    inputs = ["parisa", "mobarak", "abadan", "tehran", "shiraz", "mashhad"]
    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(first_char, inputs)
    pool.close()
    return {"pool": str(pool_outputs)}