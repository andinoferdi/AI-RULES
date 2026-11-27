import unittest

from unitconv import to_celsius, to_fahrenheit


class TemperatureTest(unittest.TestCase):
    def test_freezing(self):
        self.assertEqual(to_fahrenheit(0), 32)

    def test_boiling(self):
        self.assertEqual(to_fahrenheit(100), 212)

    def test_body_temperature_rounds(self):
        self.assertEqual(to_fahrenheit(36.6), 97.88)

    def test_back_to_celsius(self):
        self.assertEqual(to_celsius(212), 100)


if __name__ == "__main__":
    unittest.main()
