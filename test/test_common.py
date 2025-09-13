import unittest

from env.common import get_accumulated_stack_penalty

class TestCommon(unittest.TestCase):

    def test_accum_stack_penalties(self):
        self.assertEqual(get_accumulated_stack_penalty([(1, 3), (2, 6)] ), 9)


if __name__ == '__main__':
    unittest.main()
