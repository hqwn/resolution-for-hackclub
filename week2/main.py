import requests
import sys
import argparse

#Parser Setup
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

weight = subparsers.add_parser("weight", help="Get the weight of a pokemon")
weight.add_argument("name", type=str, help="Name of the Pokemon")
height = subparsers.add_parser("height", help="Get the height of a pokemon")
height.add_argument("name", type=str, help="Name of the Pokemon")
type = subparsers.add_parser("type", help="Get the type of a pokemon")
type.add_argument("name", type=str, help="Name of the Pokemon")
compare = subparsers.add_parser("compare", help="Compare weight of 2 pokemons")
compare.add_argument("pokemon1", type=str, help="Name of the Pokemon")
compare.add_argument("pokemon2", type=str, help="Name of the second Pokemon")

group = parser.add_mutually_exclusive_group()
group.add_argument("--word", action="store_true")
group.add_argument("--raw", action="store_true")
args = parser.parse_args()

def main():
    def request(pokemon):
        req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        if req.status_code != 200:
            print("API returned with error")
            sys.exit(1)
        return req.json()

    if args.command == "weight":
        result = request(args.name)

        if args.raw:
            print(result['weight'])
            sys.exit(0)
        elif args.word:
            print(f"{args.name}'s weight is {result['weight']}")
            sys.exit(0)
        
        print(f"{args.name}'s weight is {result['weight']}")


    elif args.command == "height":
        result = request(args.name)

        if args.raw:
            print(result['height'])
            sys.exit(0)
        elif args.word:
            print(f"{args.name}'s height is {result['height']}")
            sys.exit(0)
        
        print(f"{args.name}'s height is {result['height']}")

    elif args.command == "type":
        result = request(args.name)
        types = []
        for i in result['types']:
            types.append(i['type']['name'])
        
        if args.raw:
            print(types)
            sys.exit(0)
        elif args.word:
            print(f"{args.name}'s type/s are {types}")
            sys.exit(0)

        print(f"{args.name}'s type/s are {types}")

    elif args.command == 'compare':
        result = request(args.pokemon1)
        result2 = request(args.pokemon2)

        if args.raw:
            print({f'{args.pokemon1} weight': result['weight'], f'{args.pokemon2} weight': result2['weight']})
            sys.exit(0)
        elif args.word:
            print(f"{args.pokemon1} wieghs: {result['weight']} comparative to {args.pokemon2}'s wieght: {result2['weight']}")
            sys.exit(0)

        print(f"{args.pokemon1} wieghs: {result['weight']} comparative to {args.pokemon2}'s wieght: {result2['weight']}")
        
if __name__ == "__main__":
    main()
