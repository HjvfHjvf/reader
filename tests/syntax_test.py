import unittest

from pyparsing import ParseException

import ..parser.syntax as sx


def parse_string(pattern, string):
    return pattern.parseString(string)[0]


class TestNamed(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parse_string(self, string):
        return (sx.named).parseString(string)[0]

    def test_case_1(self):
        text = "/named"
        result = sx.get_name(self.parse_string(text))
        self.assertEqual(result, 'named')

    def test_case_2(self):
        text = "/namED"
        self.assertEqual(sx.get_name(self.parse_string(text)), 'namED')

    def test_case_3(self):
        text = "/@na#m$ed^&*()"
        self.assertEqual(sx.get_name(self.parse_string(text)),
                         '@na#m$ed^&*()')


class TestBool(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_1(self):
        text = "true"
        self.assertTrue(sx.get_bool(parse_string(sx.boolean, text)))

    def test_case_2(self):
        text = "false"
        self.assertFalse(sx.get_bool(parse_string(sx.boolean, text)))


class TestInt(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_1(self):
        text = "123"
        self.assertEqual(sx.get_int(parse_string(sx.int_nums, text)), 123)

    def test_case_2(self):
        text = "-456"
        self.assertEqual(sx.get_int(parse_string(sx.int_nums, text)), -456)

    def test_case_3(self):
        text = "+4567"
        self.assertEqual(sx.get_int(parse_string(sx.int_nums, text)), 4567)


class TestFloat(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_1(self):
        text_1 = "34.6"
        text_2 = "+34.23"
        self.assertEqual(sx.get_float(parse_string(sx.real_nums, text_1)),
                         34.6)
        self.assertEqual(sx.get_float(parse_string(sx.real_nums, text_2)),
                         34.23)

    def test_case_2(self):
        text_1 = "-.8765"
        text_2 = "+.9780"
        self.assertEqual(sx.get_float(parse_string(sx.real_nums, text_1)),
                         -0.8765)
        self.assertEqual(sx.get_float(parse_string(sx.real_nums, text_2)),
                         0.978)

    def test_case_3(self):
        text = "987"
        with self.assertRaises(ParseException):
            parse_string(sx.real_nums, text)


class TestArray(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_empty(self):
        text = "[]"
        self.assertSequenceEqual(sx.build_array(text), [], list)

    def test_case_flat(self):
        text = "[123 45 +.87 /name1 false true]"
        self.assertSequenceEqual(sx.build_array(text),
                                 [123, 45, 0.87, 'name1', False, True], list)
        text = "[-.876 12 3 R 3 5 7]"
        self.assertSequenceEqual(sx.build_array(text),
                                 [-0.876, (12, 3, 'R'), 3, 5, 7], list)
        text = "[null null 89 0 R 76 0 R 65 0 R 876 0 R 34 45 0 R]"
        self.assertSequenceEqual(sx.build_array(text),
                                 [None, None, (89, 0, 'R'), (76, 0, 'R'),
                                  (65, 0, 'R'), (876, 0, 'R'), 34,
                                  (45, 0, 'R')], list)


class TestString(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_empty(self):
        text = "()"
        self.assertSequenceEqual(sx.build_string(text), [], list)

    def test_case_flat(self):
        pass


class TestDict(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_empty(self):
        text = "<<>>"
        self.assertSequenceEqual(sx.build_dict(text), {}, dict)

    def test_case_flat(self):
        text_1 = "<</key1 23 /key2 45.78>>"
        self.assertSequenceEqual(sx.build_dict(text_1),
                                 {'key1': 23, 'key2': 45.78}, dict)

    def test_case_nested(self):
        text_1 = "<</key1 98 /key2 <</subkey1 45>>>>"
        self.assertSequenceEqual(sx.build_dict(text_1),
                                 {'key1': 98, 'key2': {'subkey1': 45}},
                                 dict)


if __name__ == '__main__':
    unittest.main()
