import unittest
import asyncio

from everest.climb import simulate_climb, minimal_sherpas

class TestClimb(unittest.TestCase):
    def test_minimal_sherpas(self):
        for n in range(1, 6):
            self.assertEqual(minimal_sherpas(n), n - 1)

    def test_simulate_climb_reaches_summit(self):
        for n in range(1, 6):
            log = asyncio.run(simulate_climb(n))
            self.assertEqual(len(log), n)
            self.assertIn(f"Ivan@{n}", log[-1])
            for day in range(n - 1):
                self.assertIn("(done)", log[day])

if __name__ == "__main__":
    unittest.main()
