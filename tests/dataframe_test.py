import unittest

from trackframe import DataFrame


class DataFrameTest(unittest.TestCase):

    def test_setitem(self):
        df = DataFrame({"a": [1, 2, 3]})
        self.assertEqual(df.modified, [])

        df.a += 1
        self.assertEqual(df.modified, ["a"])

        df["b"] = df.a * 2
        self.assertEqual(df.modified, ["a", "b"])

    def test_loc(self):
        df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

        df.loc[df.a > 1, "b"] *= 2
        self.assertEqual(df.modified, ["b"])

    def test_iloc(self):
        df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

        df.iloc[:2] *= 2
        self.assertEqual(df.modified, ["a", "b"])


if __name__ == "__main__":
    unittest.main()