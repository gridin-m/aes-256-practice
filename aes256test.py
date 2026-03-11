import unittest
from utils import *


class Test(unittest.TestCase):
    def test_bytes_to_state(self):
        data = bytes(range(16))
        state = bytes_to_state(data)
        # проверяем что байты правильно разложились по столбцам
        self.assertEqual(state[0][0], 0)  # байт 0
        self.assertEqual(state[1][0], 1)  # байт 1
        self.assertEqual(state[2][0], 2)  # байт 2
        self.assertEqual(state[3][0], 3)  # байт 3
        self.assertEqual(state[0][1], 4)  # байт 4

    def test_state_to_bytes(self):
        data = bytes(range(16))
        state = bytes_to_state(data)
        back = state_to_bytes(state)
        self.assertEqual(data, back)

    def test_sub_bytes_inv(self):
        state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        original = [row[:] for row in state]
        sub_bytes(state)
        inv_sub_bytes(state)
        self.assertEqual(state, original)

if __name__ == '__main__':
    unittest.main()