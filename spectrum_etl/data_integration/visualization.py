'''
Created on March 26, 2020

@author: limj@mskcc.org
'''
import matplotlib.pyplot as plt
from spectrum_etl.data_integration.transform import Transformation

class Visualization():

    def __init__(self):
        pass

    def visualize(self, elab_file_name, redcap_file_name, plot_file_name):
        transform = Transformation(elab_file_name, redcap_file_name)
        final_df = transform.transform()
        final_df.reset_index(inplace=True)

        explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        colors = ['cyan', 'red', 'blue', 'green', 'gold', 'purple', 'pink', 'silver', 'magenta', 'yellow', 'orange', 'grey']
        final_df['Specimen Site'].value_counts().plot.pie(autopct='%1.1f%%',
                startangle=90, shadow=True, explode=explode, colors=colors, legend=False, fontsize=7)

        plt.title('Specimen Sites Collected', fontweight='bold', color='blue', fontsize=15)
        plt.axis('equal')
        plt.ylabel("")
        plt.tight_layout()

        plt.savefig(fname=plot_file_name, bbox_inches="tight")
        plt.show()

if __name__ == '__main__':
    viz = Visualization()
    viz.visualize("filtered_elab_sample_data", "hne_metadata", "Specimen Sites Collected")