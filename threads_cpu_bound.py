import threading
import time
import numpy as np
import scipy.integrate as integrate
import multiprocessing
from concurrent.futures import ThreadPoolExecutor


def f(x):
  #return (x+1)**(1/2) + np.log(x)*x/5
  return (x**5+x**4+1)**(1/8) + x/5*np.log(x**3+2*x**2) - np.exp(x/(x**2+x))


def integral(f, a : int, b : int): # по формуле левых прямоугольников
  global ans
  global locker
  global delta
  c = True
  n = int((b-a)/delta)

  x = np.linspace(a, b, n)
  
  for point in x:
    locker.acquire()
    if c:
      pred = point
      c = False
    else:
      ans += delta*f(pred)
      pred = point
    locker.release()



def integral2(f, a : int, b : int): # по формуле левых прямоугольников
  global ans
  global section
  global delta
  c = True

  n = int((b-a)/delta)
  x = np.linspace(a, b, n)
  locate = 0

  for point in x:
    if c:
      pred = point
      c = False
    else:
      ans += delta*f(pred)
      pred = point
      
  name  = threading.current_thread().name
  section[int(name[-1])] += locate


    

if __name__ == "__main__":
    N = 10**3
    delta = 0.001
    ans = 0.0
    locker = threading.RLock()
    
    print("Максимальное число потоков = ", multiprocessing.cpu_count())

    res = integrate.quad(f, 1, N)
    time.sleep(2)
    print(f"Истинное значение интеграла равно = {res[0]}")
  

    #start = time.time()
    #integral2(f, 1, N)
    #print(f"Время выполнения 1 потока = {time.time() - start}")
    
    
    n_mas = [1, 8, 16]
    functions = [integral, integral2]

    for func in functions:
        if func == integral:
           print("-----------------------------------------------")
           print("СКОРОСТЬ ВЫЧИСЛЕНИЙ, КОГДА ГЛОБАЛЬНАЯ ПЕРЕМЕННАЯ(РЕЗУЛЬТАТ ИНТЕГРИРОВАНИЯ) ЯВЛЯЕТСЯ ОБЩЕЙ ДЛЯ ВСЕХ ПОТОКОВ")
           print()
        elif func == integral2:
           print("-----------------------------------------------")
           print("СКОРОСТЬ ВЫЧИСЛЕНИЙ, КОГДА СОЗДАЕТСЯ ЛОКАЛЬНАЯ ПЕРЕМЕННАЯ(РЕЗУЛЬТАТ ИНТЕГРИРОВАНИЯ) ДЛЯ КАЖДОГО ПОТОКА, И ЗАТЕМ ПОСЛЕ ВЫПОЛНЕНИЯ ЕЕ ЗНАЧЕНИЕ ПРИБАВЛЯЕТСЯ К ГЛОБАЛЬНОЙ ПЕРЕМЕННОЙ(ИТОГОВОМУ РЕЗУЛЬТАТУ ИНТЕГРИРОВАНИЯ)")
           print()
        for n in n_mas:
            section = [0]*n
            ans = 0.0
            mas_threads = []
            length = N // n
            b = 1
            for i in range(n):
                if i == (n-1):
                    mas_threads.append(threading.Thread(target=func, args=(f, b, N), name=f"thr-{i}", daemon=False))
                else:
                    buf = b
                    b += length
                    mas_threads.append(threading.Thread(target=func, args=(f, buf, b), name=f"thr-{i}", daemon=False))

            start = time.time()
            for thr in mas_threads:
                thr.start()
            for thr in mas_threads:
                thr.join()
            print(f"Время выполнения {n} потоков = {time.time()-start}")
            if func == integral:
              print(f"Результат выполнения {n} потоков = {ans}")
            else:
               print(f"Результат выполнения {n} потоков = {sum(section)}")
            print()



