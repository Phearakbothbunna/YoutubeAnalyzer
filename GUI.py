# Run tkinter GUI by using 'python GUI.py' command in terminal

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from pymongo import MongoClient
from aggregations import (
    calculate_view_statistics,
    calculate_avg_rating_by_category,
    calculate_total_comments_and_ratings_by_category,
    calculate_avg_length_by_category,
    avg_views_per_video_by_category,
    most_viewed_videos,
    most_viewed_video_in_each_category,
    top_uploader_by_views,
    top_commented_videos
)
import time

# MongoDB connection setup
uri = 'mongodb://localhost:27017/'
client = MongoClient(uri)
db = client["youtubedb"]
collection = db["youtube_vids"]

# Helper function to measure execution time and display results
def execute_and_time(func, *args, description=""):
    start_time = time.time()
    result = list(func(*args))
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


# Main GUI window
class YouTubeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Analyzer")
        self.root.geometry("800x600")

        # Title label
        tk.Label(root, text="YouTube Analyzer", font=("Arial", 16)).pack(pady=10)

        # Dropdown for selecting analysis option
        self.analysis_var = tk.StringVar()
        self.analysis_options = [
            "Total View Statistics",
            "Average Rating by Category",
            "Total Comments and Ratings by Category",
            "Average Video Length by Category",
            "Average Views per Video by Category",
            "Most Viewed Videos",
            "Most Viewed Video in Each Category",
            "Top Uploader by Views",
            "Top Commented Videos"
        ]
        tk.Label(root, text="Select Analysis:").pack()
        self.analysis_menu = ttk.Combobox(
            root, 
            textvariable=self.analysis_var, 
            values=self.analysis_options, 
            width=30
        )
        self.analysis_menu.pack(pady=5)

        # Button to execute analysis
        self.run_button = tk.Button(root, text="Run Analysis", command=self.run_analysis)
        self.run_button.pack(pady=10)

        # Text area for displaying results
        self.result_area = tk.Text(root, wrap=tk.WORD, height=20, width=70)
        self.result_area.pack(pady=10)

    def run_analysis(self):
        analysis = self.analysis_var.get()
        if not analysis:
            messagebox.showerror("Error", "Please select an analysis.")
            return
        
        self.result_area.delete("1.0", tk.END)

        try:
            if analysis == "Total View Statistics":
                stats, exec_time = execute_and_time(calculate_view_statistics, collection, description="Platform-Wide View Statistics")
                stats = stats[0]
                self.result_area.insert(tk.END, f"Average Views: {stats['avgViews']:.2f}\n")
                self.result_area.insert(tk.END, f"Maximum Views: {stats['maxViews']}\n")
                self.result_area.insert(tk.END, f"Minimum Views: {stats['minViews']}\n")
            elif analysis == "Average Rating by Category":
                results, exec_time = execute_and_time(calculate_avg_rating_by_category, collection)
                for res in results:
                    self.result_area.insert(tk.END, f"Category: {res['_id']}, Avg Rating: {res['avgRating']:.2f}\n")
            elif analysis == "Total Comments and Ratings by Category":
                results, exec_time = execute_and_time(calculate_total_comments_and_ratings_by_category, collection)
                for res in results:
                    self.result_area.insert(
                        tk.END,
                        f"Category: {res['_id']}, Total Comments: {res['totalComments']}, Total Ratings: {res['totalRatings']}\n"
                    )
            elif analysis == "Average Video Length by Category":
                results, exec_time = execute_and_time(calculate_avg_length_by_category, collection)
                for res in results:
                    self.result_area.insert(tk.END, f"Category: {res['_id']}, Avg Length: {res['avgLength']:.2f}\n")
            elif analysis == "Average Views per Video by Category":
                results, exec_time = execute_and_time(avg_views_per_video_by_category, collection)
                for res in results:
                    self.result_area.insert(tk.END, f"Category: {res['_id']}, Avg Views: {res['avgViews']:.2f}\n")
            elif analysis == "Most Viewed Videos":
                results, exec_time = execute_and_time(most_viewed_videos, collection, 5)
                for res in results:
                    self.result_area.insert(tk.END, f"Video ID: {res['videoID']}, Views: {res['views']}\n")
            elif analysis == "Most Viewed Video in Each Category":
                results, exec_time = execute_and_time(most_viewed_video_in_each_category, collection)
                for res in results:
                    self.result_area.insert(
                        tk.END, 
                        f"Category: {res['_id']}, Video ID: {res['videoID']}, Views: {res['views']}\n"
                    )
            elif analysis == "Top Uploader by Views":
                result, exec_time = execute_and_time(top_uploader_by_views, collection)
                result = result[0]
                self.result_area.insert(tk.END, f"Uploader: {result['_id']}, Total Views: {result['totalViews']}\n")
            elif analysis == "Top Commented Videos":
                results, exec_time = execute_and_time(top_commented_videos, collection)
                for res in results:
                    self.result_area.insert(
                        tk.END, 
                        f"Video ID: {res['videoID']}, Comments: {res['comments']}, Uploader: {res['uploader']}\n"
                    )
            
            # Display execution time
            self.result_area.insert(tk.END, f"\nExecution Time: {exec_time:.4f} seconds\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeAnalyzerApp(root)
    root.mainloop()
