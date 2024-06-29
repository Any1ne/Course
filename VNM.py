from gui import VNM
import os
import shutil

def main():
    app = VNM()
    # global master
    # master = test
    
    app.mainloop()
    
    ###close program
    try:
        os.remove("PMFL_Newtons.txt")
        os.remove("result.csv")
        os.remove("memory_analysis.csv")
        os.remove("cprofile_results")
        os.remove("cprofile_results.txt")
        os.remove("config.json")
    except FileNotFoundError:
        print("One of the deleting file not found.")

    try:
        current_dir = os.path.dirname(__file__)
        media_folder = os.path.join(current_dir, "media")   
        shutil.rmtree(media_folder)
    except OSError:
        print("Deleting dir not found.")

if __name__ == "__main__":
    main()
