class Roll:
    def _init_(self, pins: int):
        self.pins = pins

class Frame:
    def _init_(self):
        self.rolls = []

    def add_roll(self, pins: int):
        self.rolls.append(Roll(pins))

    def score(self) -> int:
        raise NotImplementedError

class NormalFrame(Frame):
    def score(self) -> int:
        return sum(roll.pins for roll in self.rolls)

class TenthFrame(Frame):
    def _init_(self):
        super()._init_()
        self.extra_roll = None

    def add_roll(self, pins: int):
        if self.rolls:
            if len(self.rolls) == 3:
                raise ValueError("Cannot add more than 3 rolls to a TenthFrame")
            if self.extra_roll:
                self.rolls.append(self.extra_roll)
                self.extra_roll = None
        self.rolls.append(Roll(pins))

    def score(self) -> int:
        if len(self.rolls) == 3:
            return sum(roll.pins for roll in self.rolls)
        elif len(self.rolls) == 2:
            return sum(roll.pins for roll in self.rolls) + self.extra_roll.pins
        else:
            raise ValueError("Invalid number of rolls in a TenthFrame")

class BowlingGame:
    def _init_(self):
        self.frames = []
        self.frame_scores = []

    def add_roll(self, pins: int):
        if not self.frames:
            self.frames.append(NormalFrame())
        elif isinstance(self.frames[-1], TenthFrame) and len(self.frames[-1].rolls) < 3:
            self.frames[-1].add_roll(pins)
        elif isinstance(self.frames[-1], NormalFrame) and len(self.frames[-1].rolls) == 2:
            self.frames[-1].add_roll(pins)
            self.frames.append(NormalFrame())
        else:
            self.frames[-1].add_roll(pins)

    def score(self) -> int:
        return sum(self.frame_scores)

    def input_frame_scores(self):
        for i, frame in enumerate(self.frames):
            if isinstance(frame, NormalFrame):
                roll1 = None
                while roll1 is None or roll1 < 0 or roll1 > 10:
                    try:
                        print(f"Frame {i + 1}: Ingrese el puntaje del primer tiro (entre 0 y 10)")
                        roll1 = int(input())
                    except ValueError:
                        print("Entrada no válida. Por favor, ingrese un número entero.")

                frame.add_roll(roll1)

                # Si el primer tiro es menor que 10, permitir un segundo tiro
                if roll1 < 10:
                    roll2 = None
                    while roll2 is None or roll2 < 0 or roll2 > (10 - roll1):
                        try:
                            print(f"Frame {i + 1}: Ingrese el puntaje del segundo tiro (entre 0 y {10 - roll1})")
                            roll2 = int(input())
                        except ValueError:
                            print("Entrada no válida. Por favor, ingrese un número entero.")

                    frame.add_roll(roll2)

                # Calcular el puntaje del frame actual y agregarlo a self.frame_scores
                self.frame_scores.append(frame.score())

            else:  # Es un TenthFrame
                for j in range(2):  # Permitir dos tiros normales en el TenthFrame
                    roll = None
                    while roll is None or roll < 0 or roll > 10:
                        try:
                            print(
                                f"Frame {i + 1}: Ingrese el puntaje del {'primer' if j == 0 else 'segundo'} tiro (entre 0 y 10)")
                            roll = int(input())
                        except ValueError:
                            print("Entrada no válida. Por favor, ingrese un número entero.")

                    frame.add_roll(roll)

                # Calcular el puntaje del frame actual y agregarlo a self.frame_scores
                self.frame_scores.append(frame.score())

        # Calcular el puntaje total del juego después de ingresar todos los puntajes
        self.total_score = sum(self.frame_scores)


def main():
    game = BowlingGame()
    # Solicitar al usuario el puntaje de cada frame
    for i in range(10):  # 10 frames en un juego de bolos
        print(f"Frame {i + 1}:")
        while True:
            try:
                roll = int(input("Ingrese el puntaje del primer tiro (10 pines, 5 pines, etc.): "))
                game.add_roll(roll)
                break
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número entero.")

        # Permitir el segundo tiro si no es un strike o es el décimo frame
        if i < 9 or roll != 10:
            while True:
                try:
                    roll = int(input("Ingrese el puntaje del segundo tiro: "))
                    game.add_roll(roll)
                    break
                except ValueError:
                    print("Entrada no válida. Por favor, ingrese un número entero.")

        # En el décimo frame, permitir un tercer tiro si es un strike o un spare
        if i == 9 and (game.frames[-1].rolls[0].pins == 10 or sum(roll.pins for roll in game.frames[-1].rolls) == 10):
            while True:
                try:
                    roll = int(input("Ingrese el puntaje del tercer tiro: "))
                    game.add_roll(roll)
                    break
                except ValueError:
                    print("Entrada no válida. Por favor, ingrese un número entero.")

    # Calcular el puntaje total del juego
    game.calculate_frame_scores()

    # Mostrar el puntaje total del juego
    print(f"El puntaje total del juego es: {game.score()}")

if __name__ == "__bolos__":
    bolos()