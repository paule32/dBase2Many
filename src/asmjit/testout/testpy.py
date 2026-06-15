global BACKEND
BACKEND = "foo"

class Test:
    def __init__(self):
        BACKEND = "bar"
        print("BaCk:", BACKEND)   # give "bar"
 
    def fun(self):
        print("back:", BACKEND)

if __name__ == "__main__":
    print("BACK:", BACKEND)
    cls = Test();
    cls.fun()     # give "foo"
 