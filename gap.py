import subprocess
import json
import os

def write_PMFL():
    with open('config.json') as f:
            config = json.load(f)

    qualitys = {
      "l": "480p15",
      "m": "720p30",
      "h": "1080p60"
    }
    
    quality = qualitys.get(config["Quality"])
    method = config['Method']
    
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Get project directory

    file_path = os.path.join(project_dir, "media", "videos", "example_manim", quality, "partial_movie_files", method, "partial_movie_file_list.txt")

    with open(file_path, 'r') as partial_list_file, \
            open('PMFL_'+method+'.txt', 'a') as pmfl_file:
            for line in partial_list_file:
                if line.startswith('file \'file:'):
                    pmfl_file.write(line[11:-2]+ '\n')

def gap_run():
    with open('config.json') as f:
            config = json.load(f)
    method = config['Method']

    with open('PMFL_'+method+'.txt', 'w') as f:
        f.write('')

    stopCriteria = False
    while not stopCriteria :
        with open('config.json') as f:
            config = json.load(f)

        command_calculation = ["python", "methods.py"]
        process_calculation = subprocess.Popen(command_calculation)
        process_calculation.wait()

        command_animation = ["manim", "-v", "WARNING", "anim.py", config['Method'], "-q"+config['Quality']]
        process_animation = subprocess.Popen(command_animation)
        process_animation.wait()

        write_PMFL()

        stopCriteria = config["Stop_Criteria"] or (config["Iteration"]>=config["Number of Iteration"])

gap_run()