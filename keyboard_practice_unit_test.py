#!/usr/bin/env python3

import unittest
from unittest.mock import patch, mock_open
from keyboard_practice import KeyboardPractice
from pytest_socket import disable_socket
import wikipedia
import pyperclip

class TestKeyboardPractice(unittest.TestCase):   

    # FILE RELATED TESTS
    @patch("os.path.isfile", lambda path : True)
    def test_check_if_correct_file_ext(self):
        """
        Tests if the script checks if the given path leads to a directory.

        The case where the file is of the right type is tested in 
        test_file_read method
        """
        MOCK_FILE_PATH = "path/to/mock.pdf"
        with self.assertRaises(ValueError):
            kp = KeyboardPractice()
            kp.get_text_from_file(MOCK_FILE_PATH, stats=False)

    def test_non_file_path_input(self):
        """
        Tests whether non-existent file of the right extension raises a 
        FileNotFoundError.
        """
        MOCK_PATH = "non/existent/path.txt"
        with self.assertRaises(FileNotFoundError):
            kp = KeyboardPractice()
            kp.get_text_from_file(MOCK_PATH, stats=False)

    @patch("os.path.isfile", lambda path : True)
    def test_file_read(self):
        """
        Tests file return with a mock file. 
        
        The for loop is there to check
        whether the code covers all the accepted file types.
        """
        for ext in ["txt", "md"]:
            MOCK_FILE_PATH = "path/to/mock." + ext
            with patch("builtins.open", mock_open(read_data="data1\ndata2")) as mock_file:
                kp = KeyboardPractice()
                lines = kp.get_text_from_file(MOCK_FILE_PATH, stats=False)
                self.assertEqual(lines, "data1|data2")
                mock_file.assert_called_with(MOCK_FILE_PATH)

    # STRING RELATED TESTS
    def test_empty_string_read(self):
        """
        Tests whether the empty input string is formatted and returned 
        as expected.
        """
        with self.assertRaises(ValueError):
            kp = KeyboardPractice()
            kp.get_text_from_string("", stats=False)

    # TEXT PROCESSING TESTS
    def test_text_with_typos(self):
        """
        Tests if the error corrections works as expected.
        """
        kp = KeyboardPractice()
        self.assertEqual(kp.get_text_from_string(".-|", stats=False), ".|-||")
        self.assertEqual(kp.get_text_from_string("a-a", stats=False), "a-a")

        self.assertEqual(kp.get_text_from_string("\n\n", stats=False), "|")
        self.assertEqual(kp.get_text_from_string("\n", stats=False), "|")
        self.assertEqual(kp.get_text_from_string("\t", stats=False), "|")

        self.assertEqual(kp.get_text_from_string("   ", stats=False), "|")
        self.assertEqual(kp.get_text_from_string("  ", stats=False), "|")
        self.assertEqual(kp.get_text_from_string(" ", stats=False), "|")

        self.assertEqual(kp.get_text_from_string(".a", stats=False), ".|a")
        self.assertEqual(kp.get_text_from_string(".A", stats=False), ".|A")
        self.assertEqual(kp.get_text_from_string(".(", stats=False), ".|(")
        self.assertEqual(kp.get_text_from_string(".[", stats=False), ".|[")
        self.assertEqual(kp.get_text_from_string(".{", stats=False), ".|{")

        self.assertEqual(kp.get_text_from_string(",a", stats=False), ",|a")
        self.assertEqual(kp.get_text_from_string(",A", stats=False), ",|A")
        self.assertEqual(kp.get_text_from_string(",(", stats=False), ",|(")
        self.assertEqual(kp.get_text_from_string(",[", stats=False), ",|[")
        self.assertEqual(kp.get_text_from_string(",{", stats=False), ",|{")

        self.assertEqual(kp.get_text_from_string(";a", stats=False), ";|a")
        self.assertEqual(kp.get_text_from_string(";A", stats=False), ";|A")
        self.assertEqual(kp.get_text_from_string(";(", stats=False), ";|(")
        self.assertEqual(kp.get_text_from_string(";[", stats=False), ";|[")
        self.assertEqual(kp.get_text_from_string(";{", stats=False), ";|{")

        self.assertEqual(kp.get_text_from_string(":a", stats=False), ":|a")
        self.assertEqual(kp.get_text_from_string(":A", stats=False), ":|A")
        self.assertEqual(kp.get_text_from_string(":(", stats=False), ":|(")
        self.assertEqual(kp.get_text_from_string(":[", stats=False), ":|[")
        self.assertEqual(kp.get_text_from_string(":{", stats=False), ":|{")

    # WIKIPEDIA TESTS
    @patch.object(wikipedia, "summary")
    def test_wikipedia_return(self, summary):
        """
        Tests wikipedia return by mocking wikipedia.summary

        Internet connection is disbled for this test
        """
        disable_socket()
        MOCK_INPUT_VALUE = "mock wikipedia return"
        MOCK_RETURN_VALUE = "mock|wikipedia|return"
        summary.return_value = MOCK_INPUT_VALUE
        kp = KeyboardPractice()
        lines = kp.get_text_from_wikipedia("NonexistentSearch", stats=False)
        self.assertEqual(MOCK_RETURN_VALUE, lines)

    # STATS TESTS
    def test_1_char_stats(self):
        """
        Tests the stats return with one character
        """
        kp = KeyboardPractice()
        WORD = "a"
        lines = kp.get_text_from_string(WORD)

        EXPECTED = "\n".join([
            WORD,
            "",
            "Char count: 1",
            "Word count: 1",
            "WPM required for 10 mins: 1",
        ])

        self.assertEqual(lines, EXPECTED)

    def test_10_char_stats(self):
        """
        Tests the stats return with one character
        """
        kp = KeyboardPractice()
        WORD = "a"*10
        lines = kp.get_text_from_string(WORD)

        EXPECTED = "\n".join([
            WORD,
            "",
            "Char count: 10",
            "Word count: 1",
            "WPM required for 10 mins: 1",
        ])

        self.assertEqual(lines, EXPECTED)
    
    def test_100_char_10_word_stats(self):
        """
        Tests the stats return with one character
        """
        kp = KeyboardPractice()
        WORD = " ".join(["a"*10]*10)
        WORD_PIPED = "|".join(WORD.split(" "))
        lines = kp.get_text_from_string(WORD)

        EXPECTED = "\n".join([
            WORD_PIPED,
            "",
            "Char count: 109",
            "Word count: 10",
            "WPM required for 10 mins: 2",
        ])

        self.assertEqual(lines, EXPECTED)

    def test_100_char_100_word_stats(self):
        """
        Tests the stats return with one character
        """
        kp = KeyboardPractice()
        WORD = " ".join(["a"*10]*100)
        WORD_PIPED = "|".join(WORD.split(" "))
        lines = kp.get_text_from_string(WORD)

        EXPECTED = "\n".join([
            WORD_PIPED,
            "",
            "Char count: 1099",
            "Word count: 100",
            "WPM required for 10 mins: 11",
        ])

        self.assertEqual(lines, EXPECTED)

    def test_100_char_1000_word_stats(self):
        """
        Tests the stats return with one character
        """
        kp = KeyboardPractice()
        WORD = " ".join(["a"*10]*1000)
        WORD_PIPED = "|".join(WORD.split(" "))
        lines = kp.get_text_from_string(WORD)

        EXPECTED = "\n".join([
            WORD_PIPED,
            "",
            "Char count: 10999",
            "Word count: 1000",
            "WPM required for 10 mins: 101",
        ])

        self.assertEqual(lines, EXPECTED)

unittest.main()