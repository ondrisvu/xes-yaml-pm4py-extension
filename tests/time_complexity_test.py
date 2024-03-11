from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

from pm4py.objects.log.importer.yaml import importer as yaml_importer
from pm4py.objects.log.exporter.yaml import exporter as yaml_exporter

from pm4py.write import append_yaml, append_xes
import shutil


from tests.constants import (
    INPUT_DATA_DIR,
    OUTPUT_DATA_DIR,
)

import unittest
import os
import time



def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        return end_time - start_time, result

    return wrapper  

class TimeComplexityMeasurements(unittest.TestCase):
    def create_new_log_via_append(self, base, appended):
        yaml_to_be_appended_log = yaml_importer.apply(
            os.path.join(INPUT_DATA_DIR, f"{appended}.xes.yaml")
        )

        og_yaml_output_path = os.path.join(INPUT_DATA_DIR, f"{base}.xes.yaml")
        copy_yaml_output_path = os.path.join(
            OUTPUT_DATA_DIR, f"{base}_create.xes.yaml"
        )
        shutil.copyfile(og_yaml_output_path, copy_yaml_output_path)
        append_yaml(
            yaml_to_be_appended_log, copy_yaml_output_path
        )
        new_log = yaml_importer.apply(copy_yaml_output_path)
        
        xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{base}_create.xes")
        xes_exporter.apply(new_log, xes_output_path)
    # ======================================== example tests ========================================
    def test_01_import_export_time_complexity(self):
        self.perform_XES_import_export_time_complexity("running-example")

    def test_02_import_export_time_complexity(self):
        self.perform_YAML_import_export_time_complexity("running-example")

    def test_03_append_time_complexity(self):
        self.perform_YAML_append_time_complexity("running-example", "running-example")

    # ======================================== Helper methods ========================================

    def perform_XES_import_export_time_complexity(self, log_file):
        log_path = os.path.join(INPUT_DATA_DIR, f"{log_file}.xes")
        xes_import_time, xes_log = measure_time(xes_importer.apply)(log_path)

        xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes")
        yaml_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes.yaml")

        yaml_export_time, _ = measure_time(yaml_exporter.apply)(
            xes_log, yaml_output_path
        )
        xes_export_time, _ = measure_time(xes_exporter.apply)(xes_log, xes_output_path)
        yaml_import_time, _ = measure_time(yaml_importer.apply)(yaml_output_path)

        del xes_log

        os.remove(xes_output_path)
        os.remove(yaml_output_path)
        print(f"[XES] [IMPORT/EXPORT TIME COMPLEXITY RESULTS] for {log_file}")
        print(f"[import XES]  Time Complexity: {xes_import_time}")
        print(f"[import YAML]  Time Complexity: {yaml_import_time}")
        print(f"[export XES]  Time Complexity: {xes_export_time}")
        print(f"[export YAML]  Time Complexity: {yaml_export_time}\n")

        print("=============================================================\n")

    def perform_YAML_import_export_time_complexity(self, log_file):
        log_path = os.path.join(INPUT_DATA_DIR, f"{log_file}.xes.yaml")
        yaml_import_time, yaml_log = measure_time(yaml_importer.apply)(log_path)

        xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes")
        yaml_output_path = os.path.join(OUTPUT_DATA_DIR, f"{log_file}.xes.yaml")

        xes_export_time, _ = measure_time(xes_exporter.apply)(yaml_log, xes_output_path)
        yaml_export_time, _ = measure_time(yaml_exporter.apply)(
            yaml_log, yaml_output_path
        )
        xes_import_time, _ = measure_time(xes_importer.apply)(xes_output_path)


        del yaml_log

        os.remove(xes_output_path)
        os.remove(yaml_output_path)

        print(f"[YAML] [IMPORT/EXPORT TIME COMPLEXITY RESULTS] for {log_file}")
        print(f"[import XES]  Time Complexity: {xes_import_time}")
        print(f"[import YAML]  Time Complexity: {yaml_import_time}")
        print(f"[export XES]  Time Complexity: {xes_export_time}")
        print(f"[export YAML]  Time Complexity: {yaml_export_time}\n")

        print("=============================================================\n")

    def perform_YAML_append_time_complexity(self, base_log_file, log_file):
        yaml_to_be_appended_log = yaml_importer.apply(
            os.path.join(INPUT_DATA_DIR, f"{log_file}.xes.yaml")
        )

        og_yaml_output_path = os.path.join(INPUT_DATA_DIR, f"{base_log_file}.xes.yaml")
        copy_yaml_output_path = os.path.join(
            OUTPUT_DATA_DIR, f"{base_log_file}.xes.yaml"
        )
        shutil.copyfile(og_yaml_output_path, copy_yaml_output_path)

        yaml_time, _ = measure_time(append_yaml)(
            yaml_to_be_appended_log, copy_yaml_output_path
        )

        og_xes_output_path = os.path.join(INPUT_DATA_DIR, f"{base_log_file}.xes")
        copy_xes_output_path = os.path.join(OUTPUT_DATA_DIR, f"{base_log_file}.xes")
        shutil.copyfile(og_xes_output_path, copy_xes_output_path)

        xes_time, _ = measure_time(append_xes)(
            copy_xes_output_path, yaml_to_be_appended_log
        )

        print(f"[APPEND TIME COMPLEXITY RESULTS] for base: {base_log_file} and appended: {log_file}")
        print(f"[append XES] Time Complexity: {xes_time}")
        print(f"[append YAML] Time Complexity: {yaml_time}\n")
        print("========================================\n")

        os.remove(copy_xes_output_path)
        os.remove(copy_yaml_output_path)
