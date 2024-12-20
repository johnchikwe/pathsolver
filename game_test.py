import unittest
from llstack import LLStack
from game import OutOfBoundaries, InvalidCoordinateError, Map


grid2 = [['ocean', 'grass', 'grass', 'grass'],
        ['grass', 'grass', 'grass', 'grass', 'grass'],
        ['grass', 'grass', 'grass', 'ocean', 'grass'],
        ['grass', 'ocean', 'grass', 'ocean', 'grass', 'grass'],
        ['ocean', 'grass', 'grass', 'grass', 'grass'],
        ['grass', 'grass', 'ocean', 'grass']]

class testGame(unittest.TestCase):
    # def __init__(self, grid: List[List[str]],
    # start_loc: tuple, end_loc: tuple):

    def testNoneHead(self):  # testing raise IndexError
        lls = LLStack()
        with self.assertRaises(IndexError):
            lls.pop()

    def testSize(self):
        lls = LLStack()
        lls.push((1, 0))
        lls.push((2, 0))
        self.assertEqual(lls.size, 2)

    def test_PushPopSize(self):
        lls = LLStack()
        lls.push((2, 0))
        lls.push((3, 3))
        lls.pop()
        self.assertEqual(lls.size, 1)

    def testPushType(self):
        lls = LLStack()
        with self.assertRaises(TypeError):
            lls.push(1)

    def testStrInTuple(self):
        lls = LLStack()
        with self.assertRaises(TypeError):
            lls.push((1, 'dog'))

    def testWrongLenTuple(self):  # tuple length can only be length of 2
        lls = LLStack()
        with self.assertRaises(ValueError):
            lls.push((1, 2, 3))

    def testBadValTuple(self):
        lls = LLStack()
        with self.assertRaises(ValueError):
            lls.push((-1, 2))

    def testNormalStr(self):
        lls = LLStack()
        lls.push((0, 0))
        lls.push((0, 1))
        lls.push((1, 1))
        self.assertEqual(lls.__str__(), "(0,0) -> (0,1) -> (1,1)")


    def testArrowedEnd(self):
        lls = LLStack()
        lls.push((0, 0))
        lls.push((1, 1))
        self.assertNotEqual(lls.__str__(), "(0,0) -> (1,1) -> ")

    def testWrongOrdered(self):
        lls = LLStack()
        lls.push((0, 0))
        lls.push((1, 2))
        self.assertNotEqual(lls.__str__(), "(1,2) -> (0,0)")

    def test_startEndType(self):
        grid = [['ocean', 'grass', 'ocean']]
        start = [0, 1]
        end = [1, 2]
        with self.assertRaises(TypeError):
            Map(grid, start, end)


    def testCoordValues(self):
        grid = [['ocean', 'grass', 'ocean']]
        start = ('0', 1)
        end = ('1', 2)
        with self.assertRaises(TypeError):
            Map(grid, start, end)

    def testCoordLen(self):
        grid = [['ocean', 'grass', 'ocean']]
        start = (1, 5, 7)
        end = (2, 4, 5)
        with self.assertRaises(ValueError):
            Map(grid, start, end)


    def testCoordPosNeg(self):
        grid = [['ocean', 'grass', 'ocean']]
        start = (-9, 0)
        end = (-4, 0)
        with self.assertRaises(ValueError):
            Map(grid, start, end)

    def testBoundaries(self):
        grid = [['ocean', 'grass', 'ocean']]
        start = (0, 1)
        end = (1, 2)
        with self.assertRaises(OutOfBoundaries):
            Map(grid, start, end)

    def testInvalidCoordinates(self):
        grid = [['ocean', 'grass', 'ocean']]
        start = (0, 0)
        end = (0, 2)
        with self.assertRaises(InvalidCoordinateError):
            Map(grid, start, end)

    def testEndNotStart(self):  # testing if ending coords are different compared to starting coordinates
        with self.assertRaises(ValueError):
            grid = [['ocean', 'grass', 'ocean']]
            start = (0, 0)
            end = (0, 0)
            Map(grid, start, end)



    def testNoPath(self):
        grid = [['grass', 'ocean', 'grass']]
        start = (0, 0)
        end = (0, 2)
        m = Map(grid, start, end)
        self.assertEqual(m.find_path(), None)

    def testPath(self):
        m = Map(grid2, (1, 0), (1, 4))
        self.assertEqual(str(m.find_path()), "(1,0) -> (2,0) -> (2,1) -> (2,2) -> (3,2) -> "
                                             "(4,2) -> (4,3) -> (4,4) -> (3,4) -> (2,4) -> (1,4)")


    def testPathOneRow(self):
        grid = [['grass', 'grass', 'grass']]
        m = Map(grid, (0, 0), (0, 2))
        self.assertEqual(str(m.find_path()), "(0,0) -> (0,1) -> (0,2)")

    def testNoGrid(self):
        grid = [[]]
        with self.assertRaises(OutOfBoundaries):
            Map(grid, (0, 0), (2, 1))

