from time import sleep, ctime, time
from multiprocessing import Process


def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")


def customer_private_workflow(customer):

    print(f"{ctime()}   [Process-{customer}] Taking Order ...")
    sleep(1)
    print(f"{ctime()}   [Process-{customer}] Taking Order ...Done!")

    print(f"{ctime()}   [Process-{customer}] Cooking Spaghetti ...")
    sleep(1)
    print(f"{ctime()}   [Process-{customer}] Cooking Spaghetti ...Done!")

    print(f"{ctime()}   [Process-{customer}] Manage Bar for Drink ...")
    sleep(1)
    print(f"{ctime()}   [Process-{customer}] Manage Bar for Drink ...Done!")
    print(f"{ctime()}   [Process-{customer}] All served!\n")


if __name__ == "__main__":

    customers = ["A", "B", "C"]
    start_time = time()

    # Phase 1: Sequential greeting
    for customer in customers:
        greet_diners(customer)

    print(f"\n{ctime()} --- All customers greeted. Spawning Processes! ---\n")

    # Phase 2: Concurrent workflow
    customer_processes = []

    for customer in customers:
        p = Process(
            target=customer_private_workflow,
            args=(customer,)
        )

        customer_processes.append(p)
        p.start()

    for p in customer_processes:
        p.join()

    duration = time() - start_time

    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")