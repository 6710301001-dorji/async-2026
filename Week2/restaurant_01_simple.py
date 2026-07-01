from time import sleep, ctime, time


# 1. Greet customers
def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")


# 2. Take order
def take_orders(customer):
    print(f"{ctime()} Taking Order for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Taking Order for Customer-{customer} ...Done!")


# 3. Cook food
def do_cooking(customer):
    print(f"{ctime()} Cooking for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Cooking for Customer-{customer} ...Done!")


# 4. Prepare drinks
def mini_bar(customer):
    print(f"{ctime()} Mini Bar for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Mini Bar for Customer-{customer} ...Done!")
    print(f"{ctime()} Customer-{customer} All served!\n")


if __name__ == "__main__":

    customers = ["A", "B", "C"]

    start_time = time()

    # Everything runs sequentially
    for customer in customers:
        greet_diners(customer)
        take_orders(customer)
        do_cooking(customer)
        mini_bar(customer)

    duration = time() - start_time
    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")