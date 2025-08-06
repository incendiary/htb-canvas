import os
import pandas as pd
from datetime import datetime
class DLComparison:
    """
    Class to compare dedicated lab license logs, 
    comparison is done between the current and previous logs.
    """
    def __init__(self, licenses: list[dict]):
        self.licenses = licenses
        self.log_dir = self.create_log_directory()
        self.curr = self.export_dedicated_lab()
        self.latest_log = self.get_latest_log()

    def create_log_directory(self):
        log_dir = "./log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def export_dedicated_lab(self):
        
        timestamp = (datetime.now().strftime("%Y%m%d%H%M%S"))
        filename = f"{self.log_dir}/{timestamp}_DL_licenses.csv"

        with open(filename, "w") as f:
            f.write("Username,Email\n")
        for lic in self.licenses:
            if lic['id'] == 11095:
                with open(filename, "a") as f:
                    for user in lic.get("users", []):
                        f.write(f"{user['name']},{user['email']}\n")
        return filename

    def get_latest_log(self):
        files = os.listdir(self.log_dir)
        files.sort(reverse=True)
        if files:
            prev = os.path.join(self.log_dir, files[1])
            print(prev)
            # prev = os.path.join(log_dir, files[1]) if len(files) > 1 else None
            # return curr, prev
            return prev
        else:
            print("No log files found.")
            return None
    
    def compare_logs(self):
        previous_file = self.latest_log
        
        # Read the latest log file
        current_data = pd.read_csv(self.curr, header=None, names=["Username", "Email"])
        print(f"Comparing current log: {self.curr} with previous log: {previous_file}")

        # Read the previous log file
        previous_data = pd.read_csv(previous_file, header=None, names=["Username", "Email"])
        if previous_data.empty:
            print("No previous log file to compare against.")
            return
        
        # Compare the two dataframes
        new_entries = current_data[~current_data['Username'].isin(previous_data['Username'])]
        removed_entries = previous_data[~previous_data['Username'].isin(current_data['Username'])]
        
        print("New Entries:")
        print(new_entries)
        print("Removed Entries:")
        print(removed_entries)