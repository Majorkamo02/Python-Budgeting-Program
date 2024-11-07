class A:
    def __init__(self):
        self.set_i(20)

    def set_i(self,i):
        self.i = 2*i

class B(A):
    def __init__(self):
        super().__init__()
        print(f"i from B is {self.i}")


    def set_i(self, i):
        self.i = 3*i


b = B()