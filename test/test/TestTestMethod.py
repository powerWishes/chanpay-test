import unittest


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        print("set_up is Running")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO', 'test_upper测试未通过')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper(), 'test_isupper测试未通过')
        self.assertFalse('Foo'.isupper(), 'test_isupper测试未通过')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'], 'test_split测试未通过')
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def tearDown(self):
        print("tear_down is Running")

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
