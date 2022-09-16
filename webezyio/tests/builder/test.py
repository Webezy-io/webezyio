from webezyio import WebezyBuilder,WebezyPy,WebezyTs

def main():
    wzcoder = WebezyBuilder(path='/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/architect/webezy.json')
    wzcoder.InitProjectStructure()
    wzcoder.BuildProtos()

if __name__ == "__main__":
    main()