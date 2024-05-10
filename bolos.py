class Roll:
    def __init__(self, pins: int):
        self.pins = pins

class Frame:
    def __init__(self):
        self.rolls = []

    def add_roll(self, pins: int):
        self.rolls.append(Roll(pins))

    def score(self) -> int:
        raise NotImplementedError

class NormalFrame(Frame):
    def score(self) -> int:
        return sum(roll.pins for roll in self.rolls)

class TenthFrame(Frame):
    def __init__(self):
        super().__init__()
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
    def __init__(self):
        self.frames = []

    def add_roll(self, pins: int):
        if not self.frames:
            self.frames.append(NormalFrame())
        if len(self.frames[-1].rolls) == 2:
            if isinstance(self.frames[-1], NormalFrame):
                self.frames.append(TenthFrame())
            elif isinstance(self.frames[-1], TenthFrame) and self.frames[-1].extra_roll is None:
                self.frames[-1].extra_roll = Roll(pins)
                return
        self.frames[-1].add_roll(pins)

    def score(self) -> int:
        return sum(frame.score() for frame in self.frames)