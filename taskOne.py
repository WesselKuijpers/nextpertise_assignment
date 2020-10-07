class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
        
    def __sub__(self, other):
        return self.value + other.value


a = Number(1)
b = Number(1)

print(a) # prints 1
print(b) # prints 1
print(a-b) # prints 2