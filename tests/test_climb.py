import asyncio
import unittest

from everest.climb import minimal_sherpas, simulate_climb

class TestClimb(unittest.TestCase):
    def test_minimal_sherpas(self):
        for n in range(1, 6):
            self.assertEqual(minimal_sherpas(n), n - 1)

    def test_simulate_climb_reaches_summit(self):
        for n in range(1, 6):
            log = asyncio.run(simulate_climb(n))
            joined = "\n".join(log)
            self.assertIn(f"P{n}", joined)
            self.assertNotIn("Шерп{}: P{}".format(n, n), joined)

    def test_log_format(self):
        log = asyncio.run(simulate_climb(2))
        self.assertTrue(log[0].startswith("День 1"))
        self.assertIn("Иван: P0-P1", log[1])

if __name__ == "__main__":
    unittest.main()
