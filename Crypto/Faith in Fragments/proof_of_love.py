from Crypto.Util.number import getPrime, inverse, bytes_to_long
import random
import string


def create_love_message(length=16):
    alphabet_of_us = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet_of_us) for _ in range(length))


def build_future_together():
    heart_a = getPrime(128)
    heart_b = getPrime(128)
    our_world = heart_a * heart_b
    promise = 65537
    forever = inverse(promise, (heart_a - 1) * (heart_b - 1))
    return our_world, promise, forever


def protect_our_love(message, promise, world):
    encoded_feelings = bytes_to_long(message.encode())
    return pow(encoded_feelings, promise, world)


def main():
    my_faith = create_love_message()
    our_world, promise, forever = build_future_together()

    sealed_love = protect_our_love(my_faith, promise, our_world)

    print("sealed_message:", sealed_love)
    print("forever_key:", forever)

    print("Prove you know my heart")
    her_answer = input(">> ").strip()

    if her_answer == my_faith:
        print("You truly know me.")
        with open("flag.txt") as memory:
            print(memory.read())
    else:
        print("You don't know my heart yet.")


if __name__ == "__main__":
    main()
