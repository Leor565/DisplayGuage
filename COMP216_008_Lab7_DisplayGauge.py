
import tkinter as tk
from tkinter import Canvas, messagebox
from math import cos, sin, radians

# Constants for the temperature gauge
MIN_TEMP = 15.0  # Minimum temperature in degrees Celsius
NORMAL_TEMP_LOW = 20.0  # Normal low temperature in degrees Celsius
NORMAL_TEMP_HIGH = 23.0  # Normal high temperature in degrees Celsius
MAX_TEMP = 30.0  # Maximum temperature in degrees Celsius
RANGE_TEMP = MAX_TEMP - MIN_TEMP
GAUGE_BACKGROUND_COLOR = "light gray"
GAUGE_NORMAL_RANGE_COLOR = "light green"
POINTER_COLOR = "blue"

def draw_gauge(canvas, temperature):
    # Clear the previous gauge
    canvas.delete("all")

    # Draw the gauge background
    canvas.create_oval(10, 10, 210, 210, fill=GAUGE_BACKGROUND_COLOR)

    # Draw the normal temperature range arc
    normal_start_angle = -150 + (NORMAL_TEMP_LOW - MIN_TEMP) / RANGE_TEMP * 300
    normal_extent_angle = (NORMAL_TEMP_HIGH - NORMAL_TEMP_LOW) / RANGE_TEMP * 300
    canvas.create_arc(20, 20, 200, 200, start=normal_start_angle, extent=normal_extent_angle, fill=GAUGE_NORMAL_RANGE_COLOR, outline="")

    # Draw temperature markings and labels
    # Loop over the temperature range, creating marks for each degree
    for temp in range(int(MIN_TEMP), int(MAX_TEMP) + 1, 1):  # Increment by 1 degree
        # Calculate the angle for each mark based on the temperature relative to the range
        angle = -150 + (temp - MIN_TEMP) / RANGE_TEMP * 300
        radian = radians(angle)  # Convert angle to radians for the cos and sin functions

        # Calculate the starting point of the marking line
        x_start = 110 + 80 * cos(radian)  # Horizontal start position based on the radius of 80 units
        y_start = 110 - 80 * sin(radian)  # Vertical start position based on the radius of 80 units

        # Calculate the ending point of the marking line
        x_end = 110 + 90 * cos(radian)  # Horizontal end position based on the radius of 90 units
        y_end = 110 - 90 * sin(radian)  # Vertical end position based on the radius of 90 units

        # Determine the width of the line: thin for every degree, thick for every 3 degrees
        line_width = 1 if temp % 3 else 2
        # Draw the marking line on the canvas
        canvas.create_line(x_start, y_start, x_end, y_end, width=line_width)

        # For every third degree, add numeric labels indicating the temperature
        if temp % 3 == 0:
            # Calculate the position for the label, slightly further out than the end of the marking line
            x_text = 110 + 100 * cos(radian)  # Horizontal position for the text label
            y_text = 110 - 100 * sin(radian)  # Vertical position for the text label
            # Create the text label on the canvas
            canvas.create_text(x_text, y_text, text=str(temp))

    # Calculate the angle for the gauge pointer
    angle = -150 + (temperature - MIN_TEMP) / RANGE_TEMP * 300

    # Draw the gauge pointer
    canvas.create_line(110, 110, 110 + 80 * cos(radians(angle)), 110 - 80 * sin(radians(angle)), width=2, fill=POINTER_COLOR)

    # Update the gauge label
    gauge_value_label.config(text=f"Gauge Value: {temperature}°C")

def update_gauge():
    # Error checking for input
    try:
        # Get the value from the Entry widget
        value = float(entry.get())
        # Validate if the temperature is within the range
        if MIN_TEMP <= value <= MAX_TEMP:
            draw_gauge(canvas, value)
        else:
            messagebox.showerror("Input Error", f"Please enter a value between {MIN_TEMP} and {MAX_TEMP}.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")
    finally:
        # Clear the entry after update or error
        entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Room Temperature Gauge")

# Label for the Entry
entry_label = tk.Label(root, text="Enter temperature value (°C):")
entry_label.pack()

# Canvas for drawing the gauge
canvas = Canvas(root, width=220, height=220, bg="white")
canvas.pack()

# Entry widget for temperature input
entry = tk.Entry(root)
entry.pack()

# Button to update the gauge
update_button = tk.Button(root, text="Update Gauge", command=update_gauge)
update_button.pack()

# Label to display the gauge value
gauge_value_label = tk.Label(root, text="Gauge Value: --°C")
gauge_value_label.pack()

# Initialize the gauge to a default value
draw_gauge(canvas, NORMAL_TEMP_LOW)

root.mainloop()
