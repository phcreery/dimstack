class A:
    def __init__(self, name) -> None:
        self.name = name

    @property
    def B(self):
        return self._B(self)

    class _B:
        def __init__(self, parent: "A") -> None:
            self.parent = parent

        @property
        def pname(self):
            return self.parent.name


a = A("asdf")
print(a.name)
# b = a.B
# print(b.pname)
a.name = "qwer"
# print(b.pname)
print(a.B.pname)
