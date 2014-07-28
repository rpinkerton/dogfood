### iste.py The Incredibly Simple Text Editor
### A python command-line text editor implemented with the curses library
### Riley Pinkerton, Last Edit: 7/25/14

import curses
import curses.ascii
import argparse

QUIT_CMD = curses.ascii.ctrl(ord('e'))

def display_line(screen, line, line_num):
  '''Display a single line on the screen'''
  max_width = params['width']
  screen.addstr(line_num, 0, line[:max_width])

def display_text_file(screen, serialized_file):
  '''Display a file on the screen'''
  line_num = 0
  for line in ser_file:
    display_line(screen, line, line_num)
    line_num += 1
  screen.refresh()

def get_params(screen, params):
  '''Gets all the relevant parameters to editor operation'''
  params['height'], params['width'] = screen.getmaxyx()
  params['cursor_y'], params['cursor_x'] = (0, 0)

def input_loop(screen):
  '''The main input loop for the editor'''
  while True:

    # Get the user's input
    c = screen.getch()

    # Handle exiting the program
    if c == QUIT_CMD:
      return

    # Handle directional input
    elif c == curses.KEY_LEFT:
      # Don't move off the screen to the left
      if params['cursor_x'] > 0:
        params['cursor_x'] -= 1
        screen.move(params['cursor_y'], params['cursor_x'])
    elif c == curses.KEY_RIGHT:
      # Don't move off the screen to the right, or past the end of a line
      if params['cursor_x'] < params['width'] and\
         params['cursor_x'] < len(ser_file[params['cursor_y']]):
        params['cursor_x'] += 1
        screen.move(params['cursor_y'], params['cursor_x'])
    elif c == curses.KEY_UP:
      # Don't move up through the top of the screen
      if params['cursor_y'] > 0:
        params['cursor_y'] -= 1
        # Drop to ending of new line, if it's shorter than the current line
        params['cursor_x'] = min(params['cursor_x'],
                                len(ser_file[params['cursor_y']]))
        screen.move(params['cursor_y'], params['cursor_x'])
    elif c == curses.KEY_DOWN:
      # Don't move through the bottom of the screen, or past the end of the file
      if params['cursor_y'] < params['height'] and\
         params['cursor_y'] < len(ser_file) - 1:
        params['cursor_y'] += 1
        # Drop to ending of new line, if it's shorter than the current line
        params['cursor_x'] = min(params['cursor_x'],
                                len(ser_file[params['cursor_y']]))
        screen.move(params['cursor_y'], params['cursor_x'])


    # Otherwise we're writing characters to the buffer
    else:
      # Get a copy of the current line to mutate
      edit_line = list(ser_file[params['cursor_y']])
      # If we're at the end of the line, just append, O(1)
      if len(edit_line) == params['cursor_x']:
        edit_line.append(curses.ascii.unctrl(c))
      # Otherwise just append it to the previous character. (Insertion is
      # O(n), but this is O(1))
      else:
        edit_line[params['cursor_x']] = curses.ascii.unctrl(c) +\
                                        edit_line[params['cursor_x']]
      # Replace the old line with the new line, and update the screen
      ser_file[params['cursor_y']] = ''.join(edit_line)
      screen.insch(c)
      params['cursor_x'] += 1
      screen.move(params['cursor_y'], params['cursor_x'])

if __name__ == '__main__':

  # Parse arguments
  parser = argparse.ArgumentParser(description = "A simple text-editor")
  parser.add_argument("file", help="The document to edit")
  args = parser.parse_args()

  # Serialize the file in memory
  file = open(args.file, "rb")
  ser_file = []
  for line in file:
    ser_file.append(line.strip("\n"))
  # Close the file so that we can open it again later for clobbered writing
  file.close()


  # Initialize the curses screen
  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)
  params = {}
  get_params(stdscr, params)
  display_text_file(stdscr, ser_file)
  stdscr.move(0, 0)

  # Things happen here
  input_loop(stdscr)

  # Write the edited buffer back to the file
  file = open(args.file, "wb")
  for line in ser_file:
    file.write(''.join([line, "\n"]))
  file.close()

  # Exit the curses instance
  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()
