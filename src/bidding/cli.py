from bidding import Bidding, rules


def main():
    bidding = Bidding(rules)

    while True:
        print(bidding.knowledge)
        print(bidding.possible_calls)

        print("> ", end="")
        call = input()
        if call == "Back":
            bidding.pop()
            continue

        bidding.push(call)


if __name__ == '__main__':
    main()
