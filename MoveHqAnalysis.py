import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import PyPDF2
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#------ Functions ---------
def Analyse ():
    custom_style = {
    'figure.facecolor': '#221F1F',
    'axes.facecolor': '#221F1F',
    'axes.labelcolor': '#FFFFFF',
    'xtick.color': '#FFFFFF',
    'ytick.color': '#FFFFFF',
    'axes.labelweight': 'bold',
    'font.weight': 'bold',
    'text.color': '#FFFFFF',
    'grid.color': '#FFFFFF',
    'lines.marker': 'X',
    'lines.markersize': 10,
    'lines.markerfacecolor': '#FFE000',
    'lines.color': '#FF4500'
}

    # Apply the custom style
    plt.style.use(custom_style)
    #set the theme as darkgrid
    #plt.style.use('dark_background')



    performance_dict =  {
        "10m Acceleration": {
            "Male": {
                "Avg_Cricketer": 1.884,
                "Avg_Footballer": 1.932,
                "Avg_Basketballer": 1.854,
                "Usain Bolt - WR": 1.685
            },
            "Female": {
                "Avg_Cricketer": 2.059,
                "Avg_Footballer": 2.139,
                "Avg_Netballer": 1.968,
                "Flo-Jo - WR": 1.780
            }
        },
        "505": {
            "Male": {
                "General Avg time": 2.75,  # Replace None with the median time for males
            },
            "Female": {
                "General Avg time": 3.05,  # Replace None with the median time for females
            }
        },

        "Counter-movement Jump - Height":{
            "Male": {
                "General Avg height": 42                # Replace None with the median height for males
            },
            "Female": {
                " General Avg height": 28                # Replace None with the median height for females
            }

        },
        "Counter-movement Jump - W per KG":{
            "Male": {
                "General Avg W per Kg": 50.47,            # Replace None with the median watts/kg for males
            },
            "Female": {
                "General Avg W per Kg": 44.65,            # Replace None with the median watts/kg for females
            }

        },
        "Counter-movement Jump": {
            "Male": {
                "General Avg Peak Power": 3800,        # Replace None with the median peak power for males
            },
            "Female": {
                "General Peak Power Watts": 2500,        # Replace None with the median peak power for females
            }
        },
        "Hop Test": {
            "Male": {
                "median_RSI": None,  # Replace None with the median Reactive Strength Index for males
            },
            "Female": {
                "median_RSI": None,  # Replace None with the median Reactive Strength Index for females
            }
        }
    }

    def get_data():
        root = os.path.dirname(os.path.abspath(__file__))

        df = pd.read_csv(root + '/move_hq.csv')
        return df

    def make_event_plot(event_df):
        # make 2 plots, split by M/F
        event = event_df['Event'].iloc[0]
        event_dict = performance_dict[event]

        count = 0
        for units in event_df['Unit'].unique():
            count += 1
            unit_df = event_df[event_df['Unit'] == units]
            fig = plt.figure(figsize=(8.5, 11),facecolor='#221F1F')
            male_df = unit_df[unit_df['Sex'] == 'Male'].copy()
            male_event_dict = event_dict['Male']

            female_df = unit_df[unit_df['Sex'] == 'Female'].copy()
            female_event_dict = event_dict['Female']
            ax1 = fig.add_subplot(211)
            ax1.set_title(male_df['Event'].iloc[0])
            for attempt in male_df['Attempt'].unique():
                attempt_df = male_df[male_df['Attempt'] == attempt].sort_values('Value')
                ax1.scatter(attempt_df['Name'], attempt_df['Value'], label=attempt, marker='X', color='#FFE000')
            # get the values to plot from the event_dict
            colour_range = ['lime', 'orange', 'red', 'purple', 'cyan', 'yellow', 'pink', 'blue', 'green', 'white']
            for key, value in male_event_dict.items():
                if value:
                    ax1.axhline(value, linestyle='--', alpha=0.5, label=key, 
                                color=colour_range.pop(0))

            ax1.legend()
            # y title
            ax1.set_ylabel(f"{units}")
            ax1.grid(True, which='both', axis='y', alpha=0.5)
            for spine in ['top', 'right', 'bottom']:
                ax1.spines[spine].set_visible(False)


            ax2 = fig.add_subplot(212)
            for attempt in female_df['Attempt'].unique():
                attempt_df = female_df[female_df['Attempt'] == attempt].sort_values('Value')
                ax2.scatter(attempt_df['Name'], attempt_df['Value'], label=attempt, marker='X')
            colour_range = ['lime', 'orange', 'red', 'purple', 'cyan', 'yellow', 'pink', 'blue', 'green', 'white']
            for key, value in female_event_dict.items():
                if value:
                    ax2.axhline(value, linestyle='--', alpha=0.5, label=key, 
                            color=colour_range.pop(0))
            ax2.legend()
            # y title
            ax2.set_ylabel(f"{units}")
            # y grid
            ax2.grid(True, which='both', axis='y', alpha=0.5)
            for spine in ['top', 'right', 'bottom']:
                ax2.spines[spine].set_visible(False)

            fig.savefig(f"{event}_{count}.pdf")
            plt.close(fig)        

    if __name__ == '__main__':
        df = get_data()
    
        for event in df['Event'].unique():
            event_df = df[df['Event'] == event]
            make_event_plot(event_df)
            print(event)


def Merge():
    def create_cover_page(title, subtitle=None, author=None):
        packet = io.BytesIO()
        # Create a new PDF with ReportLab for the cover page
        can = canvas.Canvas(packet, pagesize=letter)

        # Set background color
        can.setFillColorRGB(34 / 255, 31 / 255, 31 / 255)  # RGB values for #221F1F
        can.rect(0, 0, letter[0], letter[1], fill=1)

        # Set title font color
        can.setFillColorRGB(255 / 255, 224 / 255, 0 / 255)  # RGB values for #FFE000
        can.setFont("Helvetica-Bold", 20)
        can.drawString(100, 500, title)

        # Set subtitle font color
        can.setFillColorRGB(255 / 255, 224 / 255, 0 / 255)  # RGB values for #FFE000
        if subtitle:
            can.setFont("Helvetica", 14)
            can.drawString(100, 480, subtitle)

        # Set author font color
        #can.setFillColorRGB(255 / 255, 224 / 255, 0 / 255)  # RGB values for #FFE000
        #if author:
            #can.setFont("Helvetica", 12)
            #can.drawString(100, 460, f"By: {author}")

        can.save()

        packet.seek(0)
        # Return PdfReader directly
        return PyPDF2.PdfReader(packet)

    def merge_pdfs_with_cover(input_pdfs, output_pdf, cover_page):
        pdf_merger = PyPDF2.PdfMerger()

        # Add cover page
        pdf_merger.append(cover_page)

        # Add each input PDF to the merger
        for pdf in input_pdfs:
            pdf_merger.append(pdf)

        # Write the merged PDF to the output file
        with open(output_pdf, 'wb') as output_file:
            pdf_merger.write(output_file)

    if __name__ == "__main__":
        # Replace these file paths with your actual file paths
        pdf_files = ['10m Acceleration_1.pdf', '505_1.pdf', 'Counter-movement Jump_1.pdf',
                     'Counter-movement Jump - Height_1.pdf','Counter-movement Jump - W per KG_1.pdf', 
                     'Hop Test_1.pdf']
        output_file = 'MoveHQ_Analysis_.pdf'
        cover_title = "MoveHQ Analysis Report"
        cover_subtitle = "Analysis of MoveHQ Performance Tests"
        #cover_author = "Kieran Shah"

        # Create the cover page
        cover_page = create_cover_page(cover_title, cover_subtitle)

        # Merge the PDFs with the cover page
        merge_pdfs_with_cover(pdf_files, output_file, cover_page)

        print(f"Front page and content pages added to: {output_file}")
    

#------ Window ------------
window = tk.Tk()
window.title("MoveHQ Analysis")
window.geometry('620x300+0+0')
window.configure(background='#221F1F')
window.resizable(False, False)
#------ Labels ------------
title = tk.Label(font=('arial', 35, 'bold'), text='MoveHQ Analysis',
                 justify='center', padx=2, pady=2, bd=2, fg="#FFE000", background='#221F1F').place(x=120)
#-----Entry Fields -------

#----- Buttons ---------
tk.Button(text="Analyse",command=Analyse, font="arial 15", width=12).place(x=250, y=95)
tk.Button(window, text="Merge", command=Merge, font="arial 15", width=12).place(x=250, y=160)

window.mainloop()