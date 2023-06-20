import threading
import time
import numpy as np
import scipy.integrate as integrate


def f(x):
  return (x+1)**(1/2) + np.log(x)*x/5


def integral(f, x, a : int, b : int): # по формуле левых прямоугольников
  global ans
  global locker
  c = True
  delta = abs(x[2]-x[1])
  
  for point in x:
    if (point >= a) and (point <= b):
      locker.acquire()
      if c:
        pred = point
        c = False
      else:
        ans += delta*f(pred)
        pred = point
      locker.release()


def integral2(f, x, a : int, b : int): # по формуле левых прямоугольников
  global ans
  global locker
  c = True
  delta = abs(x[2]-x[1])
  locate = 0

  for point in x:
    if (point >= a) and (point <= b):
      if c:
        pred = point
        c = False
      else:
        locate += delta*f(pred)
        pred = point
      
  locker.acquire()
  ans += locate
  locker.release()

    

if __name__ == "__main__":
    x = np.linspace(1, 100, 10**6)
    ans = 0.0
    locker = threading.RLock()
    
    res = integrate.quad(f, 1, 100)
    time.sleep(2)
    print(f"Истинное значение интеграла равно = {res[0]}")
    print()

    start = time.time()
    integral(f, x, 1, 100)
    print(f"Время выполнения одного потока = {time.time()-start}")
    print(f"Результат выполнения одного потока = {ans}")
    print()
    
    
    n_mas = [3, 5, 10]
    functions = [integral, integral2]

    for func in functions:
        if func == integral:
           print("-----------------------------------------------")
           print("СКОРОСТЬ ВЫЧИСЛЕНИЙ, КОГДА ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ(РЕЗУЛЬТАТ ИНТЕГРИРОВАНИЯ) ЯВЛЯЕТСЯ ОБЩЕЙ ДЛЯ ВСЕХ ПОТОКОВ")
           print()
        elif func == integral2:
           print("-----------------------------------------------")
           print("СКОРОСТЬ ВЫЧИСЛЕНИЙ, КОГДА СОЗДАЕТСЯ ЛОКАЛЬНАЯ ПЕРЕМЕННАЯ(РЕЗУЛЬТАТ ИНТЕГРИРОВАНИЯ) ДЛЯ КАЖДОГО ПОТОКА, И ЗАТЕМ ПОСЛЕ ВЫПОЛНЕНИЯ ЕЕ ЗНАЧЕНИЕ ПРИБАВЛЯЕТСЯ К ГЛОБАЛЬНОЙ ПЕРЕМЕННОЙ(ИТОГОВОМУ РКЗУЛЬТАТУ ИНТЕГРИРОВАНИЯ)")
           print()
        for n in n_mas:
            ans = 0.0
            mas_threads = []
            length = 100 // n
            b = 1
            for i in range(n):
                if i == (n-1):
                    mas_threads.append(threading.Thread(target=func, args=(f, x, b, 100), name=f"thr-{i}", daemon=False))
                else:
                    buf = b
                    b += length
                    mas_threads.append(threading.Thread(target=func, args=(f, x, buf, b), name=f"thr-{i}", daemon=False))

            start = time.time()
            for thr in mas_threads:
                thr.start()
            for thr in mas_threads:
                thr.join()
            print(f"Время выполнения {n} потоков = {time.time()-start}")
            print(f"Результат выполнения {n} потоков = {ans}")
            print()



