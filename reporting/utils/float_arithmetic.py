from decimal import Decimal


# Due to innaccuracies of float multiplication, the following muliplication method is used
def multiply_float(x, y):
    return float(Decimal(str(x)) * Decimal(str(y)))


# Due to innaccuracies of float multiplication, the following addition method is used
def add_float(x, y):
    return float(Decimal(str(x)) + Decimal(str(y)))

# Due to innaccuracies of float multiplication, the following subtraction method is used
def sub_float(x, y):
    return float(Decimal(str(x)) - Decimal(str(y)))