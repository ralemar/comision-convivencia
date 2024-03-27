import src.readers.local as reader
import src.preprocess as pp
import src.tardies as tardies
import src.colors as colors
import src.proceedings as proceedings
import src.writers.local as writer

input_data = reader.read_data()
pp.preprocess_data(input_data)

all_tardies = tardies.process_all_students(input_data)
#all_colors = colors.process_all_students(input_data)
#all_proceedings = proceedings.process_all_students(input_data)
#
writer.export_tardies(all_tardies)
#writer.export_colors(all_colors)
#writer.export_proceedings(all_proceedings)