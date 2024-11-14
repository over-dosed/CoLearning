import multiprocessing
import time

from skeleton import get_skeleton_data

def consume_skeleton_data(shared_list, lock, batch_size = 20):
    while True:
        with lock:
            if len(shared_list) >= batch_size:
                # consume/use the data
                del shared_list[:batch_size]
                print("consume one batch data, now length is ", len(shared_list))
        time.sleep(0.01)

if __name__ == "__main__":
    # 创建一个 Manager 对象
    manager = multiprocessing.Manager()
    # 创建一个共享的 list
    shared_list = manager.list()
    lock = manager.Lock()

    # 创建并启动进程
    process_1 = multiprocessing.Process(target=get_skeleton_data, args=(shared_list, lock, 100, 30))
    process_2 = multiprocessing.Process(target=consume_skeleton_data, args=(shared_list, lock,  20) )
    process_1.start()
    process_2.start()

    process_1.join()
    process_2.join()
    