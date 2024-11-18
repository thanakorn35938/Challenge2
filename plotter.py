import pandas as pd
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(filename='plotter.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.info('Starting the plotting process')

try:
    # Read CSV file
    logging.info('Reading CSV file')
    data = pd.read_csv('plot_data.csv')

    # Sort data by the first column in ascending order
    logging.info('Sorting data by the first column')
    data = data.sort_values(by=data.columns[0])

    # Extract columns
    logging.info('Extracting columns')
    x = data.iloc[:, 0]
    y = data.iloc[:, 1]

    # Plot data
    logging.info('Plotting data')
    plt.plot(x, y)
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('Line Graph from CSV Data')

    # Save plot as JPG
    logging.info('Saving plot as JPG')
    plt.savefig('plot.jpg')

    # Show plot
    logging.info('Displaying plot')
    plt.show()

    logging.info('Plotting process completed successfully')

except Exception as e:
    logging.error(f'Error occurred: {e}')
    def save_plot_as_fhd_jpg(filename='plot_fhd.jpg'):
        """
        Save the current plot as a JPG file in Full HD resolution (1920x1080).
        """
        logging.info('Saving plot as FHD JPG')
        plt.gcf().set_size_inches(19.20, 10.80)
        plt.savefig(filename, dpi=1000)

    # Save plot as FHD JPG
    save_plot_as_fhd_jpg()