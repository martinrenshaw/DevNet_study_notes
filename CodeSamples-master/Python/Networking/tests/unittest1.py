import unittest

def add5(v):
    myval = v + 5
    return myval

class tests_add5(unittest.TestCase):
    def test_add5(self):
        self.assertEqual(add5(1),6)
        self.assertEqual(add5(5),10)
        self.assertEqual(add5(10.102645),15.102645)

if __name__ == '__main__':
    unittest.main()