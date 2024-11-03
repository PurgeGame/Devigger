import tkinter as tk
from tkinter import messagebox
from tkinter import font

def moneyline_to_probability(moneyline):
    if moneyline > 0:
        return 100 / (moneyline + 100)
    else:
        return -moneyline / (-moneyline + 100)

def devig(moneyline1, moneyline2):
    prob1 = moneyline_to_probability(moneyline1)
    prob2 = moneyline_to_probability(moneyline2)
    total_prob = prob1 + prob2
    devigged_prob1 = prob1 / total_prob
    devigged_prob2 = prob2 / total_prob
    return devigged_prob1, devigged_prob2

def probability_to_moneyline(probability):
    if probability >= 0.5:
        return round((probability / (1 - probability)) * 100)
    else:
        return round(-100 / (probability / (1 - probability)))

def format_number(num):
    if abs(num - round(num)) < 1e-9:  # Check if the number is very close to an integer
        return f"{int(round(num))}"
    else:
        return f"{num:.2f}"

def adjust_results_height():
    num_lines = int(results_text.index('end-1c').split('.')[0])
    new_height = min(max(10, num_lines), 60)
    results_text.config(height=new_height)
    current_height = root.winfo_height()
    new_window_height = 150 + new_height * 20  # Adjust the base height as needed
    if new_window_height > 1000:
        new_window_height = 1000
    if new_window_height > current_height:
        root.geometry(f"275x{new_window_height}")

def calculate_devig(event=None):
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        return
    try:
        parts = input_text.split()

        # Iterate through the parts and split any 6-digit number into two 3-digit numbers
        new_parts = []
        for part in parts:
            if part.isdigit() and len(part) == 6:
                new_parts.append(part[:3])
                new_parts.append(part[3:])
            else:
                new_parts.append(part)

        parts = new_parts

        if len(parts) % 2 != 0:
            raise ValueError("Odd number of values")
        
        results = []
        for i in range(0, len(parts), 2):
            moneyline1 = float(parts[i])
            moneyline2 = float(parts[i + 1])
            
            # Swap the larger one to negative if both are positive
            if moneyline1 > 0 and moneyline2 > 0:
                if moneyline1 > moneyline2:
                    moneyline1 = -moneyline1
                else:
                    moneyline2 = -moneyline2
            
            if moneyline1 == moneyline2:
                devigged_prob1 = devigged_prob2 = 0.5
                vig_free_ml1 = 100
                vig_free_ml2 = 100
            else:
                devigged_prob1, devigged_prob2 = devig(moneyline1, moneyline2)
                vig_free_ml1 = probability_to_moneyline(devigged_prob1)
                vig_free_ml2 = probability_to_moneyline(devigged_prob2)

            # Format the moneylines to align properly
            moneyline1_str = f"{'+' if moneyline1 > 0 else ''}{format_number(moneyline1)}"
            moneyline2_str = f"{'+' if moneyline2 > 0 else ''}{format_number(moneyline2)}"
            vig_free_ml1_str = f"{'+' if vig_free_ml1 > 0 else ''}{vig_free_ml1}"
            vig_free_ml2_str = f"{'+' if vig_free_ml2 > 0 else ''}{vig_free_ml2}"

            result_text = (f"{moneyline1_str} {format_number(devigged_prob1 * 100):>6}% {vig_free_ml1_str}\n"
                           f"{moneyline2_str} {format_number(devigged_prob2 * 100):>6}%")
            results.append(result_text)
            results.append("-" * 24)  # Add a separator after each pair
        
        results_text.insert("1.0", "\n".join(results) + "\n")
        adjust_results_height()  # Adjust the height of the results text widget and window size
        results_text.see("1.0")  # Scroll to the top
        
        text_input.delete("1.0", tk.END)  # Clear the input box
    except ValueError as e:
        messagebox.showerror("Input Error", f"Please enter valid moneyline values separated by a space or newline. Error: {e}")
        
def check_paste(event=None):
    root.after(100, calculate_devig)  # Delay to ensure the paste operation completes

def paste_and_calculate(event=None):
    try:
        text_input.event_generate("<<Paste>>")
        root.after(100, calculate_devig)  # Slightly longer delay to ensure the paste operation completes
    except Exception as e:
        messagebox.showerror("Paste Error", f"An error occurred while pasting: {e}")

# Create the main application window
root = tk.Tk()
root.title("Devig")

# Define a fixed-width font
fixed_width_font = font.Font(family="Courier", size=14)

# Define dark mode colors
bg_color = "#2e2e2e"
fg_color = "#ffffff"
button_bg_color = "#444444"
button_fg_color = "#ffffff"
entry_bg_color = "#3e3e3e"
entry_fg_color = "#ffffff"

# Apply dark mode to the main window
root.configure(bg=bg_color)

# Create and place the input Text widget with fixed-width font
text_input = tk.Text(root, height=2, width=20, font=fixed_width_font, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
text_input.pack(pady=5)
text_input.bind("<Return>", calculate_devig)  # Bind the Enter key to the calculate_devig function
text_input.bind("<<Paste>>", check_paste)  # Bind the Paste event to check_paste function
text_input.bind("<Button-3>", paste_and_calculate)  # Bind right-click to paste_and_calculate function

# Create and place the Calculate button with fixed-width font
calculate_button = tk.Button(root, text="Calculate", command=calculate_devig, font=fixed_width_font, bg=button_bg_color, fg=button_fg_color)
calculate_button.pack(pady=5)

# Create and place the results Text widget with fixed-width font
results_text = tk.Text(root, height=10, width=60, font=fixed_width_font, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
results_text.pack(pady=5)

# Set the initial window size to be smaller
root.geometry("275x125")

# Run the application
root.mainloop()