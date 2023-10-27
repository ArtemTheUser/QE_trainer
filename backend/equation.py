import random
import math


class QuadraticEquation:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.a = None
        self.b = None
        self.c = None
        self.d = None

    def _create_multipliers_for_easy_equation(self):
        # (ax + b)(cx + d)
        self.a = self.c = 1
        while not self.b:
            self.b = random.randint(-8, 8)
        while not self.d:
            self.d = random.randint(-8, 8)

    def _create_multipliers_for_normal_equation(self):
        for_ac = [1] * 83 + [random.randint(2, 5) for _ in range(17)]
        self.a = random.choice(for_ac)
        self.c = random.choice(for_ac)

        while not self.b:
            self.b = random.randint(-8, 8)
        while not self.d:
            self.d = random.randint(-8, 8)

    def _create_multipliers_for_harder_equation(self):
        for_ac = [1] * 14 + [random.randint(2, 10) for _ in range(86)]
        self.a = random.choice(for_ac)
        self.c = random.choice(for_ac)

        while not self.b:
            self.b = random.randint(-10, 10)
        while not self.d:
            self.d = random.randint(-10, 10)

    def _reduce(self, d_inclued: bool):
        if d_inclued:
            gcd = math.gcd(self.a, self.b)
            self.a //= gcd
            self.b //= gcd

            gcd = math.gcd(self.c, self.d)
            self.c //= gcd
            self.d //= gcd
        else:
            gcd = math.gcd(self.a, self.b, self.c)

            self.a //= gcd
            self.b //= gcd
            self.c //= gcd

    def _create_coefficients(self):
        self._choose_func_by_difficulty()

        # this time a, b and c are *equation coefficients* itself
        a = self.a * self.c
        b = self.a*self.d + self.b*self.c
        c = self.b * self.d

        while not b:
            self.b = b
            self._choose_func_by_difficulty()
            a = self.a * self.c
            b = self.a*self.d + self.b*self.c
            c = self.b * self.d

        self._reduce(d_inclued=True)
        self.solutions = [
            f"{-self.b}" + (f"/{self.a}" if self.a != 1 else ''),
            f"{-self.d}" + (f"/{self.c}" if self.c != 1 else '')
        ]

        self.a = a
        self.b = b
        self.c = c

        self._reduce(d_inclued=False)

    def _choose_func_by_difficulty(self):
        while self._are_identical_solutions():
            self.b = self.d = None  # to make while loops work again
            match self.difficulty:
                case 1:
                    self._create_multipliers_for_easy_equation()
                case 2:
                    self._create_multipliers_for_normal_equation()
                case 3:
                    self._create_multipliers_for_harder_equation()

    def _are_identical_solutions(self):
        if self.a is None or self.b == 0:
            return True
        return -self.b / self.a == -self.d / self.c
    
    def __str__(self):
        self._create_coefficients()

        a_part = f"{self.a if self.a != 1 else ''}𝑥²"
        b_part = (
            f"{'-' if self.b < 0 else '+'} "
            f"{abs(self.b) if abs(self.b) != 1 else ''}𝑥"
        )
        c_part = f"{'-' if self.c < 0 else '+'} {abs(self.c)}"

        return f"{a_part} {b_part} {c_part} = 0"
    

def main():
    print()

    eq = QuadraticEquation(1)
    print(eq)
    print(eq.solutions)


if __name__ == '__main__':
    main()
