import asyncio
from dataclasses import dataclass
from typing import List

@dataclass
class Climber:
    name: str
    food: int
    position: int = 0
    drop_at: int | None = None
    done: bool = False

    async def step(self, ivan: 'Climber') -> List[str]:
        """Move one stage and perform drop if needed."""
        log: List[str] = []
        if self.done:
            return log
        if self.food <= 0:
            raise RuntimeError(f"{self.name} has no food to move")
        prev = self.position
        await asyncio.sleep(0)  # allow context switch
        self.position += 1
        self.food -= 1
        log.append(
            f"{self.name}: P{prev}-P{self.position}, -1 еда. Объем еды в рюкзаке {self.food}."
        )
        if self.drop_at is not None and self.position == self.drop_at:
            if self.food > 0:
                ivan.food += self.food
                log.append(
                    f"{self.name}: P{self.position}, -{self.food} еда -> Иван. Объем еды в рюкзаке 0."
                )
                log.append(
                    f"Иван: P{ivan.position}, +{self.food} еда. Объем еды в рюкзаке {ivan.food}."
                )
                self.food = 0
            self.done = True
        return log

async def simulate_climb(n: int) -> List[str]:
    """Simulate climb to summit n using minimal sherpas.

    Returns a log of daily movements."""
    if n < 1:
        raise ValueError("n must be >=1")
    ivan = Climber(name="Иван", food=1)
    sherpas = [Climber(name=f"Шерп{i}", food=i + 1, drop_at=i) for i in range(1, n)]
    log: List[str] = []

    for day in range(1, n + 1):
        log.append(f"День {day}")
        results = await asyncio.gather(
            ivan.step(ivan), *(s.step(ivan) for s in sherpas)
        )
        for entry in results:
            log.extend(entry)
    if ivan.position != n:
        raise RuntimeError("Ivan failed to reach the summit")
    # ensure no sherpa reached the summit
    for s in sherpas:
        if s.position >= n:
            raise RuntimeError("A sherpa reached the summit")
    return log

def minimal_sherpas(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >=1")
    return max(0, n - 1)

async def _async_main(n: int) -> None:
    log = await simulate_climb(n)
    for line in log:
        print(line)


def main(argv: List[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Simulate Ivan's climb")
    parser.add_argument("N", type=int, help="number of stages to the summit (<=8)")
    args = parser.parse_args(argv)
    if args.N > 8 or args.N < 1:
        parser.error("N must be between 1 and 8")
    asyncio.run(_async_main(args.N))


if __name__ == "__main__":
    main()
