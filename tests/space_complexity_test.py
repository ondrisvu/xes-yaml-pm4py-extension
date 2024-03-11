from pm4py.write import append_yaml, append_xes

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

from pm4py.objects.log.importer.yaml import importer as yaml_importer
from pm4py.objects.log.exporter.yaml import exporter as yaml_exporter

from memory_profiler import profile as space_comp_profiler

from tests.constants import (
    INPUT_DATA_DIR,
    OUTPUT_DATA_DIR,
)

import unittest
import os
import shutil

    
class SpaceComplexityMeasurements(unittest.TestCase):
    # ======================================== example tests ========================================
    def test_01_import_export_xes(self):
        self.perform_XES_import_export("running-example")

    def test_02_import_export_yaml(self):
        self.perform_YAML_import_export("running-example")
    
    def test_03_append_yaml(self):
        self.perform_YAML_append_space_complexity("running-example", "running-example")

    # ======================================== helper methods ========================================
    def perform_XES_import_export(self, log_file):            
        print("=========================================")
        print(f"[XES - IMPORT/EXPORT SPACE COMPLEXITY RESULTS] for {log_file}")
        print("=========================================")

        xes_input_path = os.path.join(INPUT_DATA_DIR, f"{log_file}.xes")
        yaml_input_path = os.path.join(INPUT_DATA_DIR, f"{log_file}.xes.yaml")
        xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes")
        yaml_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes.yaml")

        print(f"[yaml_read] {log_file}")
        yaml_log = yaml_importer.apply(yaml_input_path)
        del yaml_log

        print(f"[xes_read] {log_file}")
        xes_log = xes_importer.apply(xes_input_path)

        print(f"[xes_write] {log_file}")
        xes_exporter.apply(xes_log, xes_output_path)
        os.remove(xes_output_path)

        print(f"[yaml_write] {log_file}")
        yaml_exporter.apply(xes_log, yaml_output_path)
        os.remove(yaml_output_path)
                    

    def perform_YAML_import_export(self, log_file):
        print("=========================================")
        print(f"[YAML - EXPORT SPACE COMPLEXITY RESULTS] for {log_file}")
        print("=========================================")

        xes_input_path = os.path.join(INPUT_DATA_DIR, f"{log_file}.xes")
        yaml_input_path = os.path.join(INPUT_DATA_DIR, f"{log_file}.xes.yaml")
        xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes")
        yaml_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes.yaml")

        print(f"[xes_read] {log_file}")
        xes_log = xes_importer.apply(xes_input_path)
        del xes_log

        print(f"[yaml_read] {log_file}")
        yaml_log = yaml_importer.apply(yaml_input_path)
        
        print(f"[xes_write] {log_file}")
        xes_exporter.apply(yaml_log, xes_output_path)
        os.remove(xes_output_path)
        
        print(f"[yaml_write] {log_file}")
        yaml_exporter.apply(yaml_log, yaml_output_path)
        os.remove(yaml_output_path)


    def perform_YAML_append_space_complexity(self, base_log_file, log_file):
        print(
            f"[APPEND SPACE COMPLEXITY RESULTS] for base: {base_log_file} and appended: {log_file}"
        )
        yaml_to_be_appended_log = yaml_importer.apply(
            os.path.join(INPUT_DATA_DIR, f"{log_file}.xes.yaml")
        )

        og_xes_output_path = os.path.join(INPUT_DATA_DIR, f"{base_log_file}.xes")
        copy_xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{base_log_file}.xes")
        shutil.copyfile(og_xes_output_path, copy_xes_output_path)
        space_comp_profiler(append_xes)(copy_xes_output_path, yaml_to_be_appended_log)
        
        og_yaml_output_path = os.path.join(INPUT_DATA_DIR, f"{base_log_file}.xes.yaml")
        copy_yaml_output_path = os.path.join(
            OUTPUT_DATA_DIR, f"{base_log_file}.xes.yaml"
        )
        shutil.copyfile(og_yaml_output_path, copy_yaml_output_path)
        space_comp_profiler(append_yaml)(yaml_to_be_appended_log, copy_yaml_output_path)

        os.remove(copy_xes_output_path)
        os.remove(copy_yaml_output_path)