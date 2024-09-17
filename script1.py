import inspect

def onefunction():
    print('this is a function from script1')


def twofunction():
    print('this is a function from script1')


def threefunction(argumentOne, argumentTwo):
    print('this is a function from script1' + argumentOne + " " + argumentTwo)


def check_func_parameters(f):
    sig = inspect.signature(f)
    all_parameters = sig.parameters

    for each in all_parameters:
        print(each)




