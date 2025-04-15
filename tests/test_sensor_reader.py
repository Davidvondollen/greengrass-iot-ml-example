import unittest
from unittest.mock import patch
from device.sensor_reader import read_sensor

class TestSensorReader(unittest.TestCase):
    def test_read_sensor_structure(self):
        data = read_sensor()
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
        self.assertIn('timestamp', data)
        self.assertTrue(20 <= data['temperature'] <= 30)
        self.assertTrue(40 <= data['humidity'] <= 60)

if __name__ == '__main__':
    unittest.main()

