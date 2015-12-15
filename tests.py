import unittest
from world import World

class TestWorld(unittest.TestCase):
    def test_init(self):
        w = World((10, 2))
        self.assertEquals(len(w.cells), 10)
        for row in w.cells:
            self.assertEquals(len(row), 2)
            for cell in row:
                self.assertIsNone(cell)

    def test_random_populate(self):
        w = World((2,30))
        w.randomly_populate_cells()
        [[self.assertIsNotNone(cell) for cell in row] for row in w.cells]

suite = unittest.TestLoader().loadTestsFromTestCase(TestWorld)
unittest.TextTestRunner(verbosity=2).run(suite)
