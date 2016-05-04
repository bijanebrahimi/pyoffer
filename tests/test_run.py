import os
from unittest import TestCase, main, skip

class TestRun(TestCase):
    def setUp(self):
        pass

    def test_read_config(self):
        from pyoffer import run
        assert run.main != None


if __name__ == '__main__':
    main()
