#!/usr/bin/env python3

import os
import getopt
import wikipedia
import subprocess

def init(args):
    """
    Entrypoint for the keyboard_practice script.

    Parameters:
        args: sys.argv arguments
    
    Returns:
        print (string): Processed string to be used with 10fastfingers

    Exceptions:
        Exception: if the args length is less than 3
    """
    if len(args) < 3:
        exp_message = [
            "You need to provide at least one flag and one param",
            "",
            "Usage:",
            "python3 ./keyboard_practice <flag> <param>",
            "",
            "Possible flags:",
            "-f or --file: get text from a txt or md file",
            "-w or --wikipedia: get the summary section of a wikipedia page"
        ]
        raise Exception("\n".join(exp_message))

    opts, args = getopt.getopt(args[1:], "f:w:s:", 
        ["file=", "wikipedia=", "string="])
    
    kp = KeyboardPractice()
    
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            lines = kp.get_text_from_file(arg)
        elif opt in ("-w", "--wikipedia"):
            lines = kp.get_text_from_wikipedia(arg)
        elif opt in ("-s", "--string"):
            lines = kp.get_text_from_string(arg)

    # TODO clipboard pasting
    print("\n{}\n".format(lines))

class KeyboardPractice:

    def __check_file_exists(self, path):
        """
        Checks if the given file path leads to a file.

        Parameters:
            path (string): path to be checked 
        
        Returns:
            none
        
        Exceptions:
            FileNotFountError: In case the file does not exist
        """
        if not os.path.isfile(path):
            err_msg = "There is no file at path:\n{}"
            raise FileNotFoundError(err_msg.format(path))
    
    def __check_file_type(self, path, types):
        """
        Raises a ValueError if the path param doesn't end with an 
        accepted type.

        Parameters:
            path (string): path to be tested
            types (list): list of accepted extensions

        Exceptions:
            ValueError: if the path does not match with any of the 
            expected types.
        """
        type_match = any(map(lambda t: path.lower().endswith("." + t), types))
        if not type_match:
            err_text = "File has to be one of the following types: {}"
            raise ValueError(err_text.format(", ".join(types)))

    def get_text_from_file(self, path, processed=True, stats=True):
        """
        Retrieves the file contents from the specified path.

        Parameters:
            path (string): path for the text file
            processed (boolean): sets if the return will contain processes 
            between words
        """
        self.__check_file_exists(path)
        self.__check_file_type(path, ["md", "txt"])

        try:
            with open(path) as f:
                text = " ".join([l.strip() for l in f.readlines()])
        except Exception as ex:
            err_msg = "Somethign went wrong with file:\n{}"
            print(err_msg.format(ex))
        return processed and self.__process_string(text, stats) or text
            
    def get_text_from_wikipedia(self, page_name, processed=True, stats=True):
        """
        Retrieves the wikipedia summary section of the specified page.

        Parameters:
            page_name (string): name for the page to return summary from

        Returns:
            Wikipedia summary or a string that clarifies that no summary
            was found
        """
        try:
            text = wikipedia.summary(page_name)
            return processed and self.__process_string(text, stats) or text
        except:
            err_msg = "Wikipedia did not return a summary for {}"
            return err_msg.format(page_name)
    
    def get_text_from_string(self, string, processed=True, stats=True):
        """
        Returns param string in the preferred format.

        This method is an identity function if the processed value is False.
        If processed is true, it cleans the line breaks and uses 
        __process_string
        
        Parameters:
            string (string): Input string to process
            processed (boolean): sets if the return will contain processes 
            between words
        
        Returns:
            Processed or regular string
        """
        if len(string) == 0:
            raise ValueError("The provided string is empty")

        # no_linebreak = " ".join(string.split("\n"))
        return processed and self.__process_string(string, stats) or string

    def __process_string(self, text, stats=True):
        """
        Converts the string in the format that 10fastfingers expects.

        It also fixes some typos in the source text

        Parameters:
            text (string): regular string
            stats (boolean): true includes the output of __produce_text_stats
        
        Returns:
            processed string as 10fastfingers expects it
        """
        process_set = [
            ("-", " - "),
            ("\n\n", " "),
            ("\n", " "),
            ("\t", " "),
            ("   ", " "),
            ("  ", " "),
            (" ", "|"),
            (".(", ". ("),
            (".[", ". ["),
        ]
        for find, replace in process_set:
            text = replace.join(text.split(find))

        if stats:
            text = "{}\n\n{}".format(text, self.__produce_text_stats(text))

        return text

    def __produce_text_stats(self, text):
        """
        Produces char count, word count and other stats for the processed
        text

        Parameters:
            text (string): string to process
        """

        char_count = len(text)
        # next line works because stats are only built for strings that are
        # piped. 
        word_count = len(text.split("|"))
        speed_required = word_count // 10 + 1

        stat_msg = "Char count: {}\n"
        stat_msg += "Word count: {}\n" 
        stat_msg += "WPM required for 10 mins: {}"

        return stat_msg.format(char_count, word_count, speed_required)
