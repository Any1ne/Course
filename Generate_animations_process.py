import subprocess
import json
import time
import os
import newton_method

def write_PMFL():
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Get project directory
    file_path = os.path.join(project_dir, 'media/videos/example_manim/480p15/partial_movie_files/PointMovingOnShapes/partial_movie_file_list.txt')

    with open(file_path, 'r') as partial_list_file, \
            open('PMFL.txt', 'a') as pmfl_file:
            for line in partial_list_file:
                if line.startswith('file \'file:'):
                    pmfl_file.write(line[11:-2]+ '\n')

def gap_run():
    with open('PMFL.txt', 'w') as f:
        f.write('')
    
    #newton_method.upload_value_derivative()

    stopCriteria = False
    while not stopCriteria :
        command_animation = ["manim", "-ql", "example_manim.py", "PointMovingOnShapes"]
        process_animation = subprocess.Popen(command_animation)
        process_animation.wait()
        write_PMFL()

        command_calculation = ["python", "newton_method.py"]
        process_calculation = subprocess.Popen(command_calculation)
        process_calculation.wait()

        with open('config.json') as f:
            config = json.load(f)

        stopCriteria = config["Stop_Criteria"] or (config["Iteration"]>=config["Number of Iteration"])

        #time.sleep(5)

gap_run()