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

    async def step(self, ivan: 'Climber') -> None:
        if self.done:
            return
        if self.food <= 0:
            raise RuntimeError(f"{self.name} has no food to move")
        await asyncio.sleep(0)  # allow context switch
        self.position += 1
        self.food -= 1
        if self.drop_at is not None and self.position == self.drop_at:
            # pass all remaining food to Ivan
            ivan.food += self.food
            self.food = 0
            self.done = True

async def simulate_climb(n: int) -> List[str]:
    """Simulate climb to summit n using minimal sherpas.

    Returns a log of daily movements."""
    if n < 1:
        raise ValueError("n must be >=1")
    ivan = Climber(name="Ivan", food=1)
    sherpas = [Climber(name=f"Sherpa{i}", food=i+1, drop_at=i) for i in range(1, n)]
    log: List[str] = []

    for day in range(1, n + 1):
        await asyncio.gather(
            ivan.step(ivan),
            *(s.step(ivan) for s in sherpas),
        )
        positions = [f"{c.name}@{c.position}{' (done)' if c.done else ''}" for c in [ivan] + sherpas]
        log.append(f"Day {day}: " + ", ".join(positions))
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
