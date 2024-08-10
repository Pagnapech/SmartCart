import time

def main():
    while True:
        start = time.time() 
        print(time.time())
        while time.time() < start + 2:
            pass
        print("hi christian")
        print(time.time())
    
if __name__ == '__main__':
  main()
  