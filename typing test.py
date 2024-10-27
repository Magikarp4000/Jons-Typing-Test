"""Jon's Typing Test"""

import tkinter as tk
from tkinter.font import Font

import os
import random
import time

# GUI root
root = tk.Tk()

# Base constants
WIDTH = min(1100, root.winfo_screenwidth())
HEIGHT = min(650, root.winfo_screenheight())
FPS = 60

# Colours
DARK_BLUE = "#00154f"
LIGHT_BLUE = "#9ecaff"
WHITE = "#FFFFFF"
LIME = "#14e04b"
RED = "#ed263d"
GREY = "#8a8a8a"

# Fonts
BASE_FONT_SIZE = HEIGHT // 30
TITLE_FONT = Font(family="Microsoft JhengHei Light",
                  size=BASE_FONT_SIZE * 3 // 2)
TEXT_FONT = Font(family="Microsoft JhengHei", size=BASE_FONT_SIZE)
TEXT_FONT_SMALL = Font(family="Microsoft JhengHei",
                       size=BASE_FONT_SIZE * 2 // 3)
TEXT_FONT_HEIGHT = TEXT_FONT.metrics("linespace")


def gui():
    """Create the GUI and display what is necessary.

    All information and canvas objects are initialised here.
    """
    global canvas, obj, info

    # Distance constants
    x_padding = WIDTH // 16
    y_padding = HEIGHT // 8
    center_x = WIDTH // 2
    quarter_x = WIDTH // 4
    center_y = HEIGHT // 2
    quarter_y = HEIGHT // 4
    text_padding = HEIGHT // 12
    btn_padding = WIDTH // 8

    # Size constants
    underline_height = TEXT_FONT_HEIGHT / 15
    slider_width = TEXT_FONT_HEIGHT / 2
    slider_length = TEXT_FONT_HEIGHT * 3 / 4

    # Initialise root
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title("Jon's Typing Test!")

    # Information dictionary
    info = {
        'default_text': "Click 'start' to begin! Use your mouse or tab + "
                        "space to interact!",
        'default_val': " -- ",
        'start_time': 0.0,
        'accuracy': 0.0,
        'total': 0,
        'correct': 0,
        'running': False,
        'char_limit': 15
    }

    # Create canvas
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=DARK_BLUE)
    canvas.pack()

    # Display title text
    canvas.create_text(center_x, y_padding, text="Jon's Typing Test!",
                       font=TITLE_FONT, fill=WHITE)

    # Display text for user to type
    # Initially this is replaced by the start text
    text_to_type = canvas.create_text(x_padding, quarter_y,
                                      text=info['default_text'], fill=WHITE,
                                      font=TEXT_FONT, anchor='nw')

    # Create underline rectangle
    underline = canvas.create_rectangle(x_padding, quarter_y +
                                        TEXT_FONT_HEIGHT, x_padding,
                                        quarter_y + TEXT_FONT_HEIGHT +
                                        underline_height, width=0,
                                        fill=LIME)
    # Hide underline initially
    canvas.itemconfig(underline, state='hidden')

    # Cover the end of the text for better aesthetics
    canvas.create_rectangle(WIDTH - x_padding, 0, WIDTH, HEIGHT,
                            fill=DARK_BLUE, outline=DARK_BLUE)

    # Display text box for user to type in
    text_box = tk.Entry(font=TEXT_FONT, state='disabled', fg=DARK_BLUE,
                        validate='key')
    canvas.create_window(x_padding, center_y - text_padding, window=text_box,
                         width=center_x - x_padding, height=y_padding,
                         anchor='nw')
    # Bind checker function to text box
    text_box['validatecommand'] = (text_box.register(check_input), '%d', '%P')

    # Display start button
    start_btn = tk.Button(text="Start", font=TEXT_FONT, command=start,
                          fg=DARK_BLUE)
    start_btn_window = canvas.create_window(x_padding,
                                            center_y + y_padding,
                                            window=start_btn, anchor='nw')

    # Create stop button
    stop_btn = tk.Button(text="Stop", font=TEXT_FONT, command=stop,
                         fg=DARK_BLUE)
    stop_btn_window = canvas.create_window(x_padding,
                                           center_y + y_padding,
                                           window=stop_btn, anchor='nw')
    # Hide stop button initially
    canvas.itemconfig(stop_btn_window, state='hidden')

    # Display help button
    help_btn = tk.Button(text="Help", font=TEXT_FONT, command=instructions,
                         fg=DARK_BLUE)
    canvas.create_window(x_padding + btn_padding, center_y + y_padding,
                         window=help_btn, anchor='nw')

    # Display quit button
    quit_btn = tk.Button(text="Quit", font=TEXT_FONT, command=quit_program,
                         fg=DARK_BLUE)
    canvas.create_window(x_padding + btn_padding * 2, center_y + y_padding,
                         window=quit_btn, anchor='nw')

    # Display information text
    timer_text = canvas.create_text(center_x + quarter_x, center_y -
                                    text_padding, font=TEXT_FONT, fill=WHITE,
                                    text=f"Time taken:{info['default_val']}s",
                                    anchor='n')

    speed_text = canvas.create_text(center_x + quarter_x, center_y,
                                    font=TEXT_FONT, fill=WHITE, anchor='n',
                                    text=f"Speed:{info['default_val']}wpm")

    accuracy_text = canvas.create_text(center_x + quarter_x, center_y +
                                       text_padding, font=TEXT_FONT,
                                       text=f"Accuracy:{info['default_val']}%",
                                       fill=WHITE, anchor='n')

    # Create help text
    raw_help_text = "Click 'start' to begin the typing test! Try to type " \
                    "the above passage as accurately and quickly as you " \
                    "can. You can change the number of words as well! " \
                    "The arrow keys work on the slider along with your " \
                    "mouse. Click 'help' again to hide this text!"
    help_text = canvas.create_text(x_padding, center_y + y_padding * 2,
                                   text=raw_help_text,
                                   width=(center_x - x_padding), fill=WHITE,
                                   font=TEXT_FONT_SMALL, anchor='nw')
    # Hide help text initially
    canvas.itemconfig(help_text, state='hidden')

    # Initialise number of words
    min_words = 10
    max_words = 40
    default_word_num = (min_words + max_words) // 2

    info['num_words'] = tk.IntVar(value=default_word_num)

    # Display number of words text
    num_words_text = canvas.create_text(center_x + quarter_x,
                                        center_y + 2 * y_padding,
                                        text=f"{info['num_words'].get()} "
                                             f"words",
                                        font=TEXT_FONT, fill=WHITE)

    # Display number of words slider
    num_slider = tk.Scale(from_=min_words, to=max_words, orient="horizontal",
                          variable=info['num_words'], bg=DARK_BLUE,
                          troughcolor=WHITE, showvalue=False, bd=0,
                          sliderrelief="flat", activebackground=LIGHT_BLUE,
                          command=update_num, width=slider_width,
                          sliderlength=slider_length, takefocus=1)
    num_slider.set(default_word_num)
    canvas.create_window(center_x + quarter_x, HEIGHT - quarter_y +
                         text_padding, window=num_slider, width=quarter_x)

    # Objects dictionary
    obj = {
        'text_to_type': text_to_type,
        'underline': underline,
        'text_box': text_box,
        'start_btn': start_btn,
        'start_btn_window': start_btn_window,
        'stop_btn': stop_btn,
        'stop_btn_window': stop_btn_window,
        'timer_text': timer_text,
        'speed_text': speed_text,
        'accuracy_text': accuracy_text,
        'help_text': help_text,
        'num_words_text': num_words_text,
        'num_num_slider': num_slider
    }

    # Run main loop
    root.mainloop()


def start():
    """Start the actual typing test and reset the GUI."""
    # Replace start button with stop button
    canvas.itemconfig(obj['start_btn_window'], state='hidden')
    canvas.itemconfig(obj['stop_btn_window'], state='normal')

    # Disable number of words slider
    obj['num_num_slider'].config(state='disabled', bg=GREY, takefocus=0)

    # Reset accuracy
    info['accuracy'] = 0
    info['total'] = 0
    info['correct'] = 0

    # Reset information text
    canvas.itemconfig(obj['timer_text'],
                      text=f"Time taken:{info['default_val']}s")
    canvas.itemconfig(obj['speed_text'],
                      text=f"Speed:{info['default_val']}wpm")
    canvas.itemconfig(obj['accuracy_text'],
                      text=f"Accuracy:{info['default_val']}%")

    # Generate words
    chosen_words = generate_text(info['num_words'].get())

    # Change text to type to generated words
    canvas.itemconfig(obj['text_to_type'], text=chosen_words, fill=LIGHT_BLUE)

    # Enable user to type in text box
    obj['text_box'].config(state='normal')
    obj['text_box'].focus()


def stop(action='stop'):
    """Stop the actual typing test.

    Congratulate the player if they finished, otherwise reset the text to type.

    :param str action: The type of action to be taken
    """
    # Replace stop button with start button
    canvas.itemconfig(obj['stop_btn_window'], state='hidden')
    canvas.itemconfig(obj['start_btn_window'], state='normal')

    # Enable number of words slider
    obj['num_num_slider'].config(state='normal', bg=DARK_BLUE, takefocus=1)

    # Reset text to type to the default text if stopped
    if action == 'stop':
        canvas.itemconfig(obj['text_to_type'], text=info['default_text'],
                          fill=WHITE)

    # Congratulate user if finished
    elif action == 'finish':
        congrats_text = "Congratulations! You finished!"
        canvas.itemconfig(obj['text_to_type'], text=congrats_text, fill=LIME)

    # Disable text box
    obj['text_box'].delete(0, tk.END)
    obj['text_box'].config(state='disabled')

    # Hide underline
    canvas.itemconfig(obj['underline'], state='hidden')

    # Stop the actual typing test
    info['running'] = False


def instructions():
    """Show/hide extra instructions."""
    # Get current state
    state = canvas.itemcget(obj['help_text'], 'state')

    # Show/hide extra instructions according to the state
    if state == 'hidden':
        canvas.itemconfig(obj['help_text'], state='normal')
    else:
        canvas.itemconfig(obj['help_text'], state='hidden')


def quit_program():
    """Exit the program."""
    root.destroy()


def update_num(num_words):
    """Update the number of words text.

    :param str num_words: The number of words to type
    """
    # Check for plural
    if num_words == '1':
        ending = ""
    else:
        ending = "s"

    # Update number of words
    canvas.itemconfig(obj['num_words_text'], text=f"{num_words} word{ending}")


def update_info():
    """Calculate and update the information text."""
    # Update accuracy
    canvas.itemconfig(obj['accuracy_text'],
                      text=f"Accuracy: {info['accuracy']:.1f}%")

    # Update time taken
    time_taken = time.time() - info['start_time']
    canvas.itemconfig(obj['timer_text'], text=f"Time taken: {time_taken:.1f}s")

    # Avoid division by zero error
    if time_taken > 0:
        # Calculate speed using WPM formula
        speed = info['correct'] / 5 / (time.time() - info['start_time']) * 60

        # Update speed
        canvas.itemconfig(obj['speed_text'], text=f"Speed: {speed:.0f} wpm")

    # Check if typing test finished
    if info['running']:
        root.after(1000 // FPS, update_info)


def generate_text(num_words):
    """Randomly generate words based on the number of words.

    :param int num_words: The number of words to generate.
    :return: String containing the generated words, separated by spaces. If
    text file does not exist, return an error message.
    """
    # Check if text file exists
    # Get list of words from text file
    # Convert to set to remove duplicates if any exist
    # Convert back to list for random.sample()
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        words_list = list(set(open(f"{dir_path}/words.txt").read().split()))
    except FileNotFoundError:
        error_msg = "Error: Text file not found. Please check the file name."
        return error_msg

    # Check for upper and lower bound in case the slider values are modified
    if num_words > len(words_list):
        num_words = len(words_list)
    elif num_words < 1:
        num_words = 1

    # Generate random words
    chosen_words = random.sample(words_list, num_words)

    return " ".join(chosen_words)


def check_input(change, user_input):
    """Check if the input matches the text to type.

    A green underline is displayed for currently correct and red for
    currently incorrect. Accuracy variables are updated and the next word is
    brought forward if the current word is correct. The amount of characters
    in the text box is limited.

    :param str change: Type of change in text box
    :param str user_input: The input in text box
    :return: False if character limit exceeded, True otherwise
    """
    # Check if actual typing test is running
    if not info['running']:
        # Start timer
        info['start_time'] = time.time()

        # Update typing test information
        info['running'] = True
        update_info()

    # Get current text to type and input
    current_text = canvas.itemcget(obj['text_to_type'], 'text')
    current_word = current_text.split()[0]
    input_len = len(user_input)
    word_len = len(current_word)

    # Add space to current word if not last word
    if len(current_text) > word_len:
        current_word = f"{current_word} "
        word_len += 1

    # Hide underline if text box is empty
    if input_len == 0:
        canvas.itemconfig(obj['underline'], state='hidden')
    else:
        canvas.itemconfig(obj['underline'], state='normal')

    # Change underline length based on how many characters are typed
    x0, y0, x1, y1 = canvas.coords(obj['underline'])
    length = TEXT_FONT.measure(current_word.strip()[:input_len])
    canvas.coords(obj['underline'], x0, y0, x0 + length, y1)

    # Disallow the change to be made if character limit is exceeded
    if input_len > max(info['char_limit'], word_len):
        return False

    # Check correct or not and modify underline colour
    if user_input == current_word[:input_len]:
        # Increment correct keystrokes if correct and the change is insertion
        if change == '1':
            info['correct'] += 1
        canvas.itemconfig(obj['underline'], fill=LIME)
    else:
        canvas.itemconfig(obj['underline'], fill=RED)

    # Increment total keystrokes if change is insertion
    if change == '1':
        info['total'] += 1

    # Calculate accuracy
    if info['total'] > 0:
        info['accuracy'] = info['correct'] / info['total'] * 100

    # Check if the current word has been typed correctly
    if user_input == current_word:
        # Reset objects
        obj['text_box'].delete(0, tk.END)
        obj['text_box'].after_idle(lambda: obj['text_box'].configure(
            validate='key'))
        canvas.itemconfig(obj['underline'], state='hidden')

        # Move on to next word
        canvas.itemconfig(obj['text_to_type'], text=current_text[len(
            current_word):])

    # Check if the text is finished
    if len(canvas.itemcget(obj['text_to_type'], 'text')) == 0:
        stop('finish')

    # Allow the change to be made
    return True


# Driver code
if __name__ == "__main__":
    gui()
