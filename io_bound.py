import threading
import time
import os
import sys
import hashlib

DIR_1 = "C:\masm32\include"
DIR_2 = "C:\masm32\lib"
DIR_3 = "C:\masm32\m32lib"
DIR = [DIR_1, DIR_2, DIR_3]
hash_md5 = hashlib.md5()

def read_f(work):
    for pair in work:
        for f in pair[1]:
            try:
                file = open(f"{pair[0]}\{f}", 'rb')
                r = file.read()
            except OSError:
                print("Файл не может быть открыт на чтение")
                #sys.exit()


def division_work_to_threads(n):
    global files_name
    global DIR
    sr_f = all // n
    f_n = []
    cnt_f = 0
    cnt_thr = -1
    cnt_kort = 0
    c = False

    for j in range(len(files_name)):
        i = j % 3
        c = True
        for f in files_name[i]:

            if cnt_f != 0 and c:
                f_n[cnt_thr].append((DIR[i], []))  
                cnt_kort += 1
                c = False

            if cnt_f == 0:
                cnt_thr += 1
                f_n.append([])
                f_n[cnt_thr].append((DIR[i], []))         
                cnt_kort = 0          
                c = False

            f_n[cnt_thr][cnt_kort][1].append(f)
            cnt_f += 1

            if (cnt_f == sr_f) and (cnt_thr != (n-1)):
                cnt_f = 0

    return f_n


def hash_work(work):
    global hash_md5

    for pair in work:
        for file in pair[1]:
            f = open(f"{pair[0]}\{file}", 'rb')
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    #print(hash_md5.hexdigest())


if __name__ == "__main__":

    files_name1 = []
    for elem in DIR:
        files = os.listdir(elem)
        files_name1.append(files)

    files_name = []
    for i in range(200):
        files_name.extend(files_name1)

    

    '''print("Время выполнения 1 потока =", end=' ')
    start = time.time()
    for i in range(len(DIR)):
        for f in files_name[i]:
            try:
                file = open(f"{DIR[i]}\{f}", 'rb')
                r = file.read()
                hash_work()
            except OSError:
                print("Файл не может быть открыт на чтение")
                #sys.exit()
    print(time.time()-start)'''

    all = 0
    for elem in files_name:
        all += len(elem)
    print("Кол-во файлов =", all)
    n_mas = [1,2,3,4,5,6,7,8, 9,10,11,12,13,14,15,16]
    function = [read_f, hash_work]

    for func in function:
        if func == read_f:
            print("ЧТЕНИЕ ФАЙЛА")
        else:
            print("ХЕШ СУММА ФАЙЛА")
        for n in n_mas:
            work = division_work_to_threads(n)
            threads = []
            for i in range(n):
                threads.append(threading.Thread(target=func, args=(work[i],), name=f"thr-{i}", daemon = False))

            print(f"Время выполнения {n} потоков =", end=' ')

            start = time.time()
            for thr in threads:
                thr.start()
            for thr in threads:
                thr.join()
            print(time.time()-start)

        print("================================")
    





    
        