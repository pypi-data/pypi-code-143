import random
import time

from progress_table import ProgressTable

# Define the columns at the beginning
table = ProgressTable(
    columns=["step", "x", "x squared"],
    # Default values:
    refresh_rate=10,
    num_decimal_places=4,
    default_column_width=8,
    print_row_on_update=True,
    reprint_header_every_n_rows=30,
    custom_format=None,
    embedded_progress_bar=False,
)
table.add_column("x", width=3)
table.add_column("x root", color="red")
table.add_column("random average", color=["bright", "red"], aggregate="mean")

for step in range(10):
    x = random.randint(0, 200)

    # There are two equivalent ways to add new values
    # First:
    table["step"] = step
    table["x"] = x
    # Second:
    table.update("x root", x**0.5)
    table.update("x squared", x**2)

    # Display the progress bar by wrapping the iterator
    for _ in table(range(10)):
        # You can use weights for aggregated values
        table.update("random average", random.random(), weight=1)
        time.sleep(0.1)

    # Go to the next row when you're ready
    table.next_row()

# Close the table when it's ready
table.close()

# Export your data
data = table.to_list()
pandas_df = table.to_df()
np_array = table.to_numpy()
