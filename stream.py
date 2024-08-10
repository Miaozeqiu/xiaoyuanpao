import sys
import time

def main(name, account, password):
    print("Starting the simulation...")
    sys.stdout.flush()  # 立即刷新输出缓冲区
    time.sleep(1)
    
    print(f"Processing user: {name}")
    sys.stdout.flush()
    time.sleep(1)
    
    print(f"Account: {account}")
    sys.stdout.flush()
    time.sleep(1)
    
    print(f"Password: {password}")
    sys.stdout.flush()
    time.sleep(1)
    
    print("Simulation complete.")
    sys.stdout.flush()

if __name__ == "__main__":
    name = 'name'
    account = 'account'
    password = 'password'
    
    main(name, account, password)