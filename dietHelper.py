import tkinter as tk
import customtkinter as ctk
import threading
from time import sleep
from tkinter import messagebox
import ctypes
import json
from math import floor


class FoodInformation:
	def __init__(self, name: str, amount: float, calories_in_amount: float,
	             protein_in_amount: float, fat_in_amount: float, carbs_in_amount: float, amount_unit: str = ""):
		# we need calories (and others) per 1g, remove the need for the user
		# to calculate it by doing it here with calories (and others) devided by
		# amount, information about this available on the web
		# e.g: 100 calories in 200grams of the food = 100/200 = 100/200 = 0.5
		# calories in 1 gram
		self.name = name
		self.calories = calories_in_amount / amount
		self.protein = protein_in_amount / amount
		self.fat = fat_in_amount / amount
		self.carbs = carbs_in_amount / amount
		self.amount_unit = amount_unit  # grams or litres or 1s


class FoodServing:
	def __init__(self, food_info: FoodInformation, serving_size: int):
		self.name = food_info.name
		self.calories = food_info.calories * serving_size
		self.protein = food_info.protein * serving_size
		self.fat = food_info.fat * serving_size
		self.carbs = food_info.carbs * serving_size
		self.unit = food_info.amount_unit
		if any(unit == unit.lower() for unit in ["gr", "gram", "grams"]):
			if serving_size >= 1000:
				serving_size /= 1000
				self.unit = "Kg"

		self.serving_size = f"{serving_size} {self.unit}"

	def serving_info(self):

		return {"Name": self.name, "Amount": self.serving_size, "Calories": self.calories, "Protein": self.protein,
		        "Fat": self.fat,
		        "Carbs": self.carbs}


class Meal:
	# class meal that takes a list of foods
	def __init__(self, name, foods: [FoodServing]):
		self.name = name
		self.foods = foods

	def meal_info(self):
		return {"Meal": self.name, "Servings": self.foods}


class Diet:
	# class diet that takes a list of meals
	def __init__(self, meals: [Meal]):
		self.meals = meals


# needs to be automated
eggs = FoodInformation("Eggs", 1, 86.4, 7.56, 5.76, 0.48)
eggs_serving = FoodServing(eggs, 5)

rice = FoodInformation("Rice", 150, 116, 9, 0.4, 20, amount_unit="Grams")
rice_serving = FoodServing(rice, 200)

chicken = FoodInformation("Chicken", 450, 198, 37, 4.3, 0, amount_unit="Grams")
chicken_serving = FoodServing(chicken, 350)

breakfast = Meal("Breakfast", [eggs_serving])
dinner = Meal("Dinner", [rice_serving, chicken_serving])

diet = Diet([breakfast, dinner])


def display_info_activity():
	messagebox.showinfo("Activity Level",
	                    "1: Sedentary: little or no exercise, desk job.\n\n"
	                    "2: Light Exercise: light exercise/ sports 1-3 days/week.\n\n"
	                    "3: Moderate: moderate exercise/ sports 6-7 days/week.\n\n"
	                    "4: Active: hard exercise every day, or exercising 2x/day.\n\n"
	                    "5: Very Active: hard exercise 2 or more times per day, or training for "
	                    "marathon, or triathlon, etc.")


def display_info_plan():
	messagebox.showinfo("Plan",
	                    "1. Extreme weight gain 125%of needed calories\n\n"
	                    "2. Weight gain {wg} 117%of needed calories\n\n"
	                    "3. Moderate weight gain 108% of needed calories (recommended)\n\n"
	                    "4. Calories needed to maintain weight 100% of needed calories\n\n"
	                    "5. Moderate weight loss 92% of needed calories (recommended)\n\n"
	                    "6. Weight loss 83% of needed calories\n\n"
	                    "7. Extreme weight loss 68% of needed calories")


def display_info_method():
	messagebox.showinfo("Plan",
	                    "1. Extreme weight gain 125%of needed calories\n\n"
	                    "2. Weight gain {wg} 117%of needed calories\n\n"
	                    "3. Moderate weight gain 108% of needed calories (recommended)\n\n"
	                    "4. Calories needed to maintain weight 100% of needed calories\n\n"
	                    "5. Moderate weight loss 92% of needed calories (recommended)\n\n"
	                    "6. Weight loss 83% of needed calories\n\n"
	                    "7. Extreme weight loss 68% of needed calories")


def invert_hex_color(hex_color):
	rgb = int(hex_color.lstrip('#'), 16)
	inverted_rgb = 0xFFFFFF - rgb
	return f'#{inverted_rgb:06x}'


def add_hue(hex_color):
	rgb = int(hex_color.lstrip('#'), 16)
	if rgb == "#232324":
		added = -1253944
	else:
		added = 16773854
	print(hex_color, added)
	return f'#{added:06x}'.replace("-", "")


class App:

	def __init__(self, window: tk.Tk, theme):
		# Make application DPI aware (Windows 10)
		self.dpi_aware = False
		try:
			self.dpi_aware = True
			ctypes.windll.shcore.SetProcessDpiAwareness(1)
		except:

			pass  # Fails on non-Windows 10 systems
		self.root = window
		self.root.wm_iconbitmap('icon.ico')
		self.root.title("Diet Helper")
		if self.dpi_aware:
			self.root.geometry("600x750")
		else:
			self.root.geometry("600x650")
		self.root.wm_minsize(500, 500)
		self.root.configure(border=4)

		self.font_bold = ("Lato", 25, "bold")
		self.font = ("Lato", 20)
		self.font_small = ("Lato", 14)

		self.current_theme = theme

		self.initial_frame = tk.Frame(background=self.current_theme)
		self.initial_frame.pack(fill="both", expand=True)

		self.create_diet_button = ctk.CTkButton(self.initial_frame, text="New Diet", bg_color=self.current_theme,
		                                        fg_color="#C2FFA5",
		                                        corner_radius=5, width=200,
		                                        height=80,
		                                        text_color="black",
		                                        font=self.font_bold, hover_color="#638254",
		                                        command=self.create_diet_button_func)

		self.label1 = tk.Label(self.initial_frame, text="Target Calories:", background=self.current_theme,
		                       foreground=invert_hex_color(self.current_theme),
		                       font=self.font)
		self.label2 = tk.Label(self.initial_frame, text="Or Enter a Target", background=self.current_theme,
		                       foreground=invert_hex_color(self.current_theme),
		                       font=self.font_small)

		self.calculate_target_calories = ctk.CTkButton(self.initial_frame, text="Calculate",
		                                               bg_color=self.current_theme,
		                                               fg_color="#C2FFA5",
		                                               corner_radius=5, width=200,
		                                               height=80,
		                                               text_color="black",
		                                               font=self.font_bold, hover_color="#638254",
		                                               command=self.get_target_calories)
		self.create_diet_button.pack(anchor='center', pady=30)

		self.target_calories_entry = ctk.CTkEntry(self.initial_frame, fg_color=add_hue(self.current_theme),
		                                          text_color="black")

		self.go = ctk.CTkButton(self.initial_frame, text="Next", bg_color=self.current_theme, fg_color="#C2FFA5",
		                        corner_radius=5, width=150,
		                        height=50,
		                        text_color="black",
		                        font=self.font_bold, hover_color="#638254",
		                        command=self.set_target_calories)

		self.target_calories = 0

		self.calculate_frame = tk.Frame(background=self.current_theme)

		# each row has a label, entry/optionsMenu, button(s) if needed

		self.weight_label, self.height_label, self.age_label, self.gender_label, self.activity_label, self.plan_label, self.method_label = (
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Weight (Kg)", bg_color=self.current_theme,
			             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
			             ),
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Height (Cm)", bg_color=self.current_theme,
			             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
			             ),
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Age", bg_color=self.current_theme,
			             fg_color=self.current_theme,
			             text_color=invert_hex_color(self.current_theme), width=100
			             ),
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Gender", bg_color=self.current_theme,
			             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
			             ),
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Activity Level", bg_color=self.current_theme,
			             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
			             ),
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Diet Plan", bg_color=self.current_theme,
			             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
			             ),
			ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="Method", bg_color=self.current_theme,
			             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
			             )
		)

		self.weight_entry, self.height_entry, self.age_entry, self.plan_entry = (
			ctk.CTkEntry(self.calculate_frame, fg_color=add_hue(self.current_theme),
			             text_color="black"),
			ctk.CTkEntry(self.calculate_frame, fg_color=add_hue(self.current_theme),
			             text_color="black"),
			ctk.CTkEntry(self.calculate_frame, fg_color=add_hue(self.current_theme),
			             text_color="black"),
			ctk.CTkEntry(self.calculate_frame, fg_color=add_hue(self.current_theme),
			             text_color="black"))

		self.selected_gender = tk.StringVar(self.root)
		self.selected_gender.set("Male")
		options = ["Male", "Female"]
		self.gender_entry = ctk.CTkOptionMenu(self.calculate_frame, corner_radius=5, bg_color=self.current_theme,
		                                      fg_color=add_hue(self.current_theme), button_color="#C2FFA5",
		                                      text_color="black",
		                                      values=options, command=self.update_gender)

		self.activity_info_button, self.plan_info_button = (
			ctk.CTkButton(self.calculate_frame, width=30, text="?", fg_color=invert_hex_color(self.current_theme),
			              text_color=self.current_theme,
			              command=display_info_activity),

			ctk.CTkButton(self.calculate_frame, width=30, text="?", fg_color=invert_hex_color(self.current_theme),
			              text_color=self.current_theme,
			              command=display_info_plan))

		self.selected_activity = tk.StringVar(self.root)
		self.selected_activity.set("1")
		options_activity = [str(i) for i in range(1, 6)]
		self.activity_entry = [ctk.CTkOptionMenu(self.calculate_frame, corner_radius=5, bg_color=self.current_theme,
		                                         fg_color=add_hue(self.current_theme), button_color="#C2FFA5",
		                                         text_color="black",
		                                         values=options_activity, command=self.update_activity),
		                       self.activity_info_button]

		self.selected_plan = tk.StringVar(self.root)
		self.selected_plan.set("1")
		options_plan = [str(i) for i in range(1, 8)]
		self.plan_entry = [ctk.CTkOptionMenu(self.calculate_frame, corner_radius=5, bg_color=self.current_theme,
		                                     fg_color=add_hue(self.current_theme), button_color="#C2FFA5",
		                                     text_color="black",
		                                     values=options_plan, command=self.update_plan),
		                   self.plan_info_button]

		self.result_text_label = ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="",
		                                      bg_color=self.current_theme,
		                                      fg_color=self.current_theme,
		                                      text_color=invert_hex_color(self.current_theme), width=100
		                                      )
		self.result_label = ctk.CTkLabel(self.calculate_frame, font=self.font_bold, text="",
		                                 bg_color=self.current_theme,
		                                 fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme),
		                                 width=100
		                                 )

		self.additional_info_canvas = tk.Canvas(self.root, background=self.current_theme)
		self.protein_value = tk.StringVar(self.root)
		self.protein_value.set("1.0")

	def start(self):
		self.root.mainloop()

	def update_gender(self, value):
		self.selected_gender.set(value)
		print("Selected gender:", self.selected_gender.get())

	def update_activity(self, value):
		self.selected_activity.set(value)
		print("Selected activity:", self.selected_activity.get())

	def update_plan(self, value):
		self.selected_plan.set(value)
		print("Selected plan:", self.selected_plan.get())

	def update_pr(self, value):
		self.protein_value.set(value)
		print("Selected pr:", self.protein_value.get())

	def create_diet_button_func(self):
		self.create_diet_button.pack_forget()
		self.label1.pack(anchor='center', pady=20)

		self.calculate_target_calories.pack(anchor="center", pady=20)

		ctk.CTkLabel(self.initial_frame, text="<hr>", bg_color=self.current_theme, fg_color=self.current_theme,
		             text_color=self.current_theme,
		             ).pack(anchor='center')

		self.label2.pack(anchor='center', pady=20)
		self.target_calories_entry.pack(anchor='center', pady=10)
		self.go.pack(anchor='center', pady=20)

	def get_target_calories(self):
		self.initial_frame.pack_forget()
		self.calculate_frame.pack(fill="both", expand=True)

		entries = [self.weight_entry, self.height_entry, self.age_entry,
		           self.gender_entry, self.activity_entry, self.plan_entry]
		labels = [self.weight_label, self.height_label, self.age_label,
		          self.gender_label, self.activity_label, self.plan_label]

		self.calculate_frame.grid_columnconfigure(0, weight=1)
		self.calculate_frame.grid_columnconfigure(1, weight=1)
		self.calculate_frame.grid_columnconfigure(2, weight=1)
		self.calculate_frame.grid_columnconfigure(3, weight=1)

		j = 0
		for i, (entry, label) in enumerate(zip(entries, labels)):
			label.grid(row=i, column=0, pady=20, sticky='e')
			if i < 4:
				entry.grid(row=i, column=2, pady=5, sticky='w')
			else:
				# elements 4 and 5 are a list of entry, butto
				entry[0].grid(row=i, column=2, pady=5, sticky='w')
				entry[1].grid(row=i, column=3, pady=5, sticky='w')
			j = i

		ctk.CTkLabel(self.calculate_frame, font=self.font_small, text="(Mifflin-St Jeor\n Equation)",
		             bg_color=self.current_theme,
		             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
		             ).grid(row=j + 3, column=0, pady=5, sticky='e')
		ctk.CTkButton(self.calculate_frame, text="Calculate",
		              bg_color=self.current_theme, fg_color=invert_hex_color(self.current_theme),
		              corner_radius=5, width=125,
		              height=40,
		              text_color=self.current_theme,
		              font=self.font, hover_color="#638254",
		              command=self.calculate_target_calories_func).grid(row=j + 3, column=2, pady=5, sticky='w')

		self.result_text_label.grid(row=j + 4, column=0, pady=25, sticky='e')
		self.result_label.grid(row=j + 4, column=2, pady=25, sticky='w')

	def calculate_target_calories_func(self):
		activity_value = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
		print("activity", self.selected_activity.get(), activity_value[int(self.selected_activity.get())])
		activity_coefficient = activity_value[int(self.selected_activity.get())]
		if self.gender_entry.get() == "Female":
			gender = 1
		else:
			gender = 0
		try:
			BMR = int(
				((10 * int(self.weight_entry.get())) + (6.25 * int(self.height_entry.get())) - (
						5 * int(self.age_entry.get())) + 5 * (not gender) - 161 * gender) * activity_coefficient)
		except ValueError:
			messagebox.showerror("Missing Value", "Missing Fields or Invalid Input")
			return
		ewg = int(BMR * 1.25)
		wg = int(BMR * 1.17)
		mwg = int(BMR * 1.08)
		# maintenance = calories*1
		mwl = int(BMR * 0.92)
		wl = int(BMR * 0.83)
		ewl = int(BMR * 0.68)
		plan_value = {1: ewg, 2: wg, 3: mwg, 4: BMR, 5: mwl, 6: wl, 7: ewl}
		self.target_calories = plan_value[int(self.selected_plan.get())]

		self.result_text_label.configure(text="Target Calories:")
		self.result_label.configure(text=str(self.target_calories))
		ctk.CTkButton(self.calculate_frame, text="Next", bg_color=self.current_theme, fg_color="#C2FFA5",
		              corner_radius=5, width=125,
		              height=40,
		              text_color="black",
		              font=self.font_bold, hover_color="#638254",
		              command=self.additional_info_func).grid(row=10, column=2, pady=0, sticky='w')
		print(self.target_calories)

	def additional_info_func(self):
		self.calculate_frame.pack_forget()

		self.additional_info_canvas.grid_columnconfigure(0, weight=1)
		self.additional_info_canvas.grid_columnconfigure(1, weight=1)
		self.additional_info_canvas.grid_columnconfigure(2, weight=1)
		self.additional_info_canvas.grid_columnconfigure(3, weight=1)

		hc1 = ctk.CTkLabel(self.additional_info_canvas, text="Nutrient", font=self.font_small)
		hc2 = ctk.CTkLabel(self.additional_info_canvas, text="Calories", font=self.font_small)
		hc3 = ctk.CTkLabel(self.additional_info_canvas, text="Grams", font=self.font_small)

		# Table data
		_ = ctk.CTkLabel(self.additional_info_canvas, text="Protein", font=self.font_small)
		r1c2 = ctk.CTkLabel(self.additional_info_canvas, text="Calories", font=self.font_small)
		r1c3 = ctk.CTkLabel(self.additional_info_canvas, text="Grams", font=self.font_small)

		__ = ctk.CTkLabel(self.additional_info_canvas, text="Fat", font=self.font_small)
		r2c2 = ctk.CTkLabel(self.additional_info_canvas, text="Calories", font=self.font_small)
		r2c3 = ctk.CTkLabel(self.additional_info_canvas, text="Grams", font=self.font_small)

		___ = ctk.CTkLabel(self.additional_info_canvas, text="Carbs", font=self.font_small)
		r3c2 = ctk.CTkLabel(self.additional_info_canvas, text="Calories", font=self.font_small)
		r3c3 = ctk.CTkLabel(self.additional_info_canvas, text="Grams", font=self.font_small)

		____ = ctk.CTkLabel(self.additional_info_canvas, text="Total", font=self.font_small)
		r4c2 = ctk.CTkLabel(self.additional_info_canvas, text="Calories", font=self.font_small)
		r4c3 = ctk.CTkLabel(self.additional_info_canvas, text="Grams", font=self.font_small)

		protein_values = [str(i / 10) for i in range(10, 42, 2)]

		ctk.CTkLabel(self.additional_info_canvas, font=self.font_small, text="Protein gr/1kg body weight",
		             bg_color=self.current_theme,
		             fg_color=self.current_theme, text_color=invert_hex_color(self.current_theme), width=100
		             ).grid(row=0, column=1, pady=20, sticky='e')

		protein_val = ctk.CTkOptionMenu(self.additional_info_canvas, corner_radius=5, bg_color=self.current_theme,
		                                fg_color=add_hue(self.current_theme), button_color="#C2FFA5",
		                                text_color="black",
		                                values=protein_values, command=self.update_pr)

		protein_val.grid(row=0, column=2, pady=20, sticky='e')

		def update_table():

			if self.gender_entry.get() == "Female":
				gender = 1
			else:
				gender = 0

			protein_gr = floor(
				float(self.protein_value.get()) * int(self.weight_entry.get()) * (not gender) + 0.8 * int(
					self.weight_entry.get()) * gender)

			protein_cal = floor(protein_gr * 4)

			fat_coef = ((35 - (3.25 * int(self.selected_plan.get()))) / 100) * (not gender) + (
					(28 - (3.25 * int(self.selected_plan.get()))) / 100) * gender

			fat_cal = floor(self.target_calories * fat_coef)
			fat_gr = floor(fat_cal / 9)

			carbs_cal = floor(self.target_calories - (fat_cal + protein_cal))
			carbs_gr = floor(carbs_cal / 4)

			r1c2.configure(text=str(protein_cal))
			r1c3.configure(text=str(protein_gr))

			r2c2.configure(text=str(fat_cal))
			r2c3.configure(text=str(fat_gr))

			r3c2.configure(text=str(carbs_cal))
			r3c3.configure(text=str(carbs_gr))

			r4c2.configure(text=str(protein_cal + fat_cal + carbs_cal))
			r4c3.configure(text=str(protein_gr + fat_gr + carbs_gr))

			hc1.grid(row=2, column=0, pady=20, sticky='e')
			hc2.grid(row=2, column=1, pady=20, sticky='e')
			hc3.grid(row=2, column=2, pady=20, sticky='e')

			_.grid(row=3, column=0, pady=20, sticky='e')
			r1c2.grid(row=3, column=1, pady=20, sticky='e')
			r1c3.grid(row=3, column=2, pady=20, sticky='e')

			__.grid(row=4, column=0, pady=20, sticky='e')
			r2c2.grid(row=4, column=1, pady=20, sticky='e')
			r2c3.grid(row=4, column=2, pady=20, sticky='e')

			___.grid(row=5, column=0, pady=20, sticky='e')
			r3c2.grid(row=5, column=1, pady=20, sticky='e')
			r3c3.grid(row=5, column=2, pady=20, sticky='e')

			____.grid(row=6, column=0, pady=30, sticky='e')
			r4c2.grid(row=6, column=1, pady=30, sticky='e')
			r4c3.grid(row=6, column=2, pady=30, sticky='e')

			table_button.configure(text="Update")

			next_button.grid(row=7, column=2, pady=30, sticky='e')

		table_button = ctk.CTkButton(self.additional_info_canvas, text="Table",
		                             bg_color=self.current_theme,
		                             fg_color="#C2FFA5",
		                             corner_radius=5,
		                             text_color="black",
		                             font=self.font, hover_color="#638254",
		                             command=update_table)
		table_button.grid(row=1, column=2, pady=20, sticky='e')

		def save_data_to_json():
			# Retrieve data from widgets
			data = {
				"Protein": {
					"Calories": r1c2.cget("text"),
					"Grams": r1c3.cget("text")
				},
				"Fat": {
					"Calories": r2c2.cget("text"),
					"Grams": r2c3.cget("text")
				},
				"Carbs": {
					"Calories": r3c2.cget("text"),
					"Grams": r3c3.cget("text")
				},
				"Total": {
					"Calories": r4c2.cget("text"),
					"Grams": r4c3.cget("text")
				}
			}

			# Write the data to a JSON file
			with open("nutrition_data.json", "w") as file:
				json.dump(data, file, indent=4)

			self.choose_food()

		next_button = ctk.CTkButton(self.additional_info_canvas, text="Next", bg_color=self.current_theme, fg_color="#C2FFA5",
		              corner_radius=5,
		              text_color="black",
		              font=self.font, hover_color="#638254",
		              command=save_data_to_json)

		self.additional_info_canvas.pack(fill=tk.BOTH, expand=True)

		pass

	def choose_food(self):

		self.additional_info_canvas.pack_forget()
	def set_target_calories(self):
		def display_error():
			error = ctk.CTkLabel(self.initial_frame, text="Enter a Number", bg_color=self.current_theme,
			                     fg_color=self.current_theme,
			                     text_color="red", font=self.font_small
			                     )
			error.pack(anchor='center')
			sleep(2)
			error.pack_forget()
			return

		target = self.target_calories_entry.get()
		if not target or not target.isnumeric():
			threading.Thread(target=display_error).start()
			return
		self.target_calories = int(target)
		self.initial_frame.pack_forget()
		self.additional_info_func()


file_path = 'color_theme.json'

# Read from the file
with open(file_path, 'r') as file:
	color_theme = json.load(file)

# Accessing data
is_dark = color_theme["dark"]

root = App(tk.Tk(), "#232324" if bool(int(is_dark)) else "#EFF1F2")
root.start()
