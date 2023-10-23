

class Example:
    counter = 0

    def cubed(self, x):
        return x ** 3

    def increment_counter_by(self, x):
        self.counter += x
        return self.counter



print(Example().cubed(3))
print(Example().increment_counter_by(10))
