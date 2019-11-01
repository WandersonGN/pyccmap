from pyccmap import Directory

__all__ = ["main"]

def main():
    directory = Directory()
    print(f"[+] Displaying data for {len(directory.currencies)} different Crypto Currencies in {len(directory.apis)} different Crypto Exchanges.")
    for exchange, data in directory.dict.items():
        print(f" -  {exchange.ljust(11)}", end = "")
        for currency, info in data.items():
            print(f"{currency.ljust(4)}: " + "\t".join("= ".join((key.ljust(4), str(value).ljust(8))) for key, value in sorted(info.items(), key = lambda x: x[0])), end = ("\n" + (" " * 15)))
        print("")
    last, ask = directory.last(), directory.ask()
    print("        Min. Ask\tMax. Ask\tMin. Last\tMax. Last")
    for currency in directory.currencies:
        print(f"[{currency.ljust(5)}] {str(min(ask[currency])).ljust(8)}\t{str(max(ask[currency])).ljust(8)}\t{str(min(last[currency])).ljust(8)}\t{str(max(last[currency])).ljust(8)}")

if __name__ == "__main__":
    main()
