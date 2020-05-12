# keyboard-practice

This package produces a keyboard practice string for 10fastfingers.com's  custom typing practice section. It supports raw string input from text
or md file, shell or any wikipedia article's summary section.

The text is run through a rudimentary typo search and replace
before being returned. Script also copies the produced practice string 
to the clipboard, removing the hassle of copying the text from the shell interface.

## Usage

You can run the script in the following ways:

Inside the package folder:
```
./run.py [options]
```

One level above the package folder:
```
python3 keyboard-practice [options]
```

### Options

#### Sources

The script can retrieve raw text from 3 sources:

--file or -f: This retrieves the raw string from the specified 
text file
```
./run.py --file [file path]
./run.py -f [file path]
```

--string or -s: Uses the raw string provided in the shell interface.
```
./run.py --string "raw string here"
./run.py -s "raw string here"
```

--wikipedia or -w: Uses the summary section of the article that is
returned for the specified page name
```
./run.py --wikipedia [page name]
./run.py -w [page name]
```

#### Modifiers

-d or --divide: accepts a number to be used as the wpm measure to divide
the output text into 10 minute sections for the given wpm number. So, 
for 70 words per minute input, the text would be divided into sections 
of 700 words each.

-n or --no-clipboard: normally the script copies the produced string to 
the clipboard. This option prevents that behavior

## Issues

- Wikipedia page returns currently only work for exact matches. In case
your page name input leads to a disambiguation page, the script will not
notify you of this. It will simply tell you that the search did not 
lead to any summary content