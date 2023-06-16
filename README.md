# Pebbles Calendar: A Customizable PDF Calendar Generator

<img src=doc_images/animated.gif>

## Overview
Pebbles Calendar is a Python script designed to generate customizable, printable PDF calendars. With a range of options such as adjustable years, custom month names, and the ability to mark specific days in bold or italics (e.g., holidays).

## Functionality
The script delivers two outputs:

* A PDF calendar with graphical elements such as a background and 'pebbles', each pebble possessing randomized attributes. The total number of displayed pebbles corresponds to the month.
* A report.txt file that records the dates highlighted in bold and italics, and the seed used for the image generation.

## Library Installations
The script uses third-party python libraries holidays and reportlab. The versions used are listed in the requirements.txt file.

## Running the Project
The script to create example calendar is run from the main.py file. This main.py hosts general settings, additional settings related to specific classes are hosted in respective files.

## Structure
* main.py - contains the setup for the example calendar and functionality for writing report.txt
* pebble_classes.py - contains classes, functions and optional settings for the image
* calendar_classes.py - contains classes, functions and optional settings for the calendar graphics

## Example of the Project Use
The calendar with Slovak month names and Czech holidays in bold font printed on A4 format.

<img src=doc_images/my_calendar.jpg width="400">

## Attribution
This project utilizes [Łukasz Dziedzic's font Lato](https://www.latofonts.com/) under Open Font License.
