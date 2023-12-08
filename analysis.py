import sqlite3
import matplotlib.pyplot as plt
import math
from pathlib import Path
from collections import Counter
from time import sleep as sleep


def main():
	dirPath = Path(__file__).resolve().parent
	imgDirPath = create_image_folder(dirPath)

	# Connect to the SQLite database
	conn = sqlite3.connect("datu_sqlite_analysis_proper_format.db")
	cursor = conn.cursor()

	table_name = "datu_collection_30112023_unedited_utf8"

	# Get all column names
	cursor.execute(f"PRAGMA table_info({table_name})")
	columns = cursor.fetchall()
	select_query = [column[1] for column in columns]

	# Get the data
	for query in select_query:
		print(f"Current column: {query}")
		cursor.execute(f"SELECT `{query}` FROM {table_name}")
		data = cursor.fetchall()

		column_data = [row[0] for row in data if row[0] is not None]
		number_column_data = []
		text_column_data = []

		# Separate the data into numeric and text values, and check for dates
		for type_row in column_data:
			value = type_row
			if any(s in query.upper() for s in ["AIKA", "PÄIVÄMÄÄRÄ"]):
				text_column_data.append(value)
			elif any(s in query.upper() for s in ["VUOSI"]):
				try:
					numeric_value = float(value)
					number_column_data.append(numeric_value)
				except ValueError:
					print("NaN")

				text_column_data.append(value)
			else:
				try:
					# Try to convert the value to a float (for numeric data)
					try: 
						value = value.replace(",", ".")
						numeric_value = float(value)
					except:
						numeric_value = float(value)

					number_column_data.append(numeric_value)
				except ValueError:
					# If conversion to float fails, treat it as text
					text_column_data.append(value)

		fig_nb = None
		fig_tb = None
		fig_line = None
		fig_tp = None

		print("number_column_data", len(number_column_data))
		print(number_column_data)
		print("text_column_data", len(text_column_data))
		print(text_column_data)


		# Calculate the average of the column
		if len(number_column_data) > 0:
			fig_nb, plt_nb_name = number_averages(number_column_data, query)
			fig_line, plt_line_name = number_linecharts(number_column_data, query)
		if len(text_column_data) > 0:
			fig_tb, plt_tb_name = text_barcharts(text_column_data, query)
			fig_tp, plt_tp_name = text_piecharts(text_column_data, query)
		try:
			if fig_nb is not None:
				plt_nb_name = plt_nb_name.replace(":", "_").replace("/", "_").replace("\\", "_")
				nb_file_name = f"{plt_nb_name}.png"
				fig_nb.savefig(imgDirPath / nb_file_name, dpi=200)
				plt.close(fig_nb)

				print("Barchart")
				sleep(0.1)

			if fig_tb is not None:
				plt_tb_name = plt_tb_name.replace(":", "_").replace("/", "_").replace("\\", "_")
				tb_file_name = f"{plt_tb_name}.png"
				fig_tb.savefig(imgDirPath / tb_file_name, dpi=200)
				plt.close(fig_tb)

				print("Barchart")
				sleep(0.1)

			if fig_line is not None:
				plt_line_name = plt_line_name.replace(":", "_").replace("/", "_").replace("\\", "_")
				line_file_name = f"{plt_line_name}.png"
				fig_line.savefig(imgDirPath / line_file_name, dpi=200)
				plt.close(fig_line)

				print("Linechart")
				sleep(0.1)

			if fig_tp is not None:
				plt_tp_name = plt_tp_name.replace(":", "_").replace("/", "_").replace("\\", "_")
				tp_file_name = f"{plt_tp_name}.png"
				fig_tp.savefig(imgDirPath / tp_file_name, dpi=200)
				plt.close(fig_tp)

				print("Piechart")
				sleep(0.1)
				
			plt.clf()

		except Exception as e:
			print(f"Something went wrong: {e}")
			sleep(0.5)

	# Close the database connection
	conn.close()
	print("Program ran successfully")

def number_averages(number_column_data, query):
	# Reset the plot for every run
	fig, ax = plt.subplots(figsize=(13, 10))

	try:
		# Calculate the average of the column
		average = sum(number_column_data) / len(number_column_data)

		# Round the y axis to the nearest tenths
		max_value = max(number_column_data)
		min_value = min(number_column_data)
		ymax = math.ceil(max_value / 10) * 10.1
		ymin = math.floor(min_value / 10) * 10.1 if min_value < 0 else 0

		# Create a bar chart with the average value
		ax.bar([f"Average - {average:.2f}"], [average])
		ax.set_xlabel("Statistic")
		ax.set_ylabel("Value")
		plt_name = f"average_of_{query}"
		ax.set_title(plt_name)
		ax.set_ylim(ymin, ymax)

		print("Number barchart created")
		return fig, plt_name

	except Exception as e:
		plt.close(fig)
		plt.clf()
		print(e)
		return None, None

def number_linecharts(number_column_data, query):
	# Reset the plot for every run
	fig, ax = plt.subplots(figsize=(13, 10))

	try:
		# Round the y axis to the nearest tenths
		max_value = max(number_column_data)
		min_value = min(number_column_data)
		ymax = math.ceil(max_value / 10) * 10.1
		ymin = math.floor(min_value / 10) * 10.1 if min_value < 0 else 0

		# Create a line chart
		ax.plot(number_column_data, label = "Data Trend", color = "blue", marker = "o", linestyle = "-")

		ax.set_xlabel("Data Points")
		ax.set_ylabel("Values")
		plt_name = f"line_of_{query}"
		ax.set_title(plt_name)
		ax.set_ylim(ymin, ymax)
		ax.legend()
		ax.grid(True)

		print("Number linechart created")
		return fig, plt_name

	except Exception as e:
		plt.close(fig)
		plt.clf()
		print(e)
		return None, None

def text_barcharts(text_column_data, query):
	# Reset the plot for every run
	fig, ax = plt.subplots(figsize=(13, 10))

	# Calculate the amount of x
	try:
		x_data = [row[0] for row in text_column_data if row[0] == "x" or row[0] == "X"]
		if len(x_data) > 0:

			x_amount = len(x_data)
			ymax = math.ceil(x_amount / 10) * 10.1

			# Create a bar chart with the amount of x
			ax.bar([f"Amount of x - {x_amount:.2f}"], [x_amount])
			ax.set_xlabel("Statistic")
			ax.set_ylabel("Value")
			plt_name = f"amount_of_x_in_{query}"
			ax.set_title(plt_name)
			ax.set_ylim(0, ymax)

			print("X barchart created")
			return fig, plt_name

		elif any(s in query.upper() for s in ["AIKA", "PÄIVÄMÄÄRÄ"]):

			# Create a bar chart with the amount of dates
			data_amount = len(text_column_data)
			ymax = math.ceil(data_amount / 10) * 10.1

			ax.bar([f"Amount of date data - {data_amount:.2f}"], [data_amount])
			ax.set_xlabel("Statistic")
			ax.set_ylabel("Value")
			plt_name = f"amount_of_date_data_{query}"
			ax.set_title(plt_name)
			ax.set_ylim(0, ymax)

			print("Date barchart created")
			return fig, plt_name

		else:
			# Create a bar chart with the amount misc data
			data_amount = len(text_column_data)
			ymax = math.ceil(data_amount / 10) * 10.1

			ax.bar([f"Amount of miscellaneous data - {data_amount:.2f}"], [data_amount])
			ax.set_xlabel("Statistic")
			ax.set_ylabel("Value")
			plt_name = f"amount_of_misc_data_{query}"
			ax.set_title(plt_name)
			ax.set_ylim(0, ymax)

			print("Misc text barchart created")
			return fig, plt_name

	except Exception as e:
		plt.close(fig)
		plt.clf()
		print(e)
		return None, None

def text_piecharts(text_column_data, query):	
	# Reset the plot for every run
	fig, ax = plt.subplots(figsize=(13, 10))
	
	try:
		# Count each unique item
		data_count = Counter(text_column_data)

		# Prepare data for the pie chart
		labels = list(data_count.keys())
		sizes = list(data_count.values())

		ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
		# Equal aspect ratio ensures the pie chart is circular.
		ax.axis("equal")
		plt_name = f"piechart_of_{query}"
		ax.set_title(plt_name)

		print("Text piechart created")
		return fig, plt_name

	except Exception as e:
		plt.close(fig)
		plt.clf()
		print(e)
		return None, None


def create_image_folder(dirPath):
	# Create image folder if it does not exist
	imgDirPath = dirPath.joinpath("kohde_collection_analysis")

	if not imgDirPath.exists():
		imgDirPath.mkdir()

	return imgDirPath

if __name__ == "__main__":
	main()
