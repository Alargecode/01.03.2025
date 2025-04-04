import json


class JsonHandler:

    def dump_all(self, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces):
        if sample2.name == "":
            dic = {"Company Name:": sample1.company_name,
                   "Operator Name:": sample1.operator_name,
                   "Testing Weight(gr):": sample1.testing_weight,
                   "Sample Name:": sample1.name,
                   "Sample Width(mm)": float(sample1.width),
                   "Sample Height(mm):": float(sample1.height),
                   "Sample Age(months):": float(sample1.age),
                   "Max Static Coefficient of Friction:": max_static,
                   "Mean Static Coefficient of Friction:": mean_static,
                   "Max Dynamic Coefficient of Friction:": max_dynamic,
                   "Mean Dynamic Coefficient of Friction:": mean_dynamic,
                   "Forces:": forces
                   }
        else:
            dic = {"Company Name:": sample1.company_name,
                   "Operator Name:": sample1.operator_name,
                   "Testing Weight(gr):": sample1.testing_weight,
                   "First Sample Name:": sample1.name,
                   "First Sample Width(mm)": float(sample1.width),
                   "First Sample Height(mm):": float(sample1.height),
                   "First Sample Age(months):": float(sample1.age),
                   "Second Sample Name:": sample2.name,
                   "Second Sample Width(mm)": float(sample2.width),
                   "Second Sample Height(mm):": float(sample2.height),
                   "Second Sample Age(months):": float(sample2.age),
                   "Max Static Coefficient of Friction:": max_static,
                   "Mean Static Coefficient of Friction:": mean_static,
                   "Max Dynamic Coefficient of Friction:": max_dynamic,
                   "Mean Dynamic Coefficient of Friction:": mean_dynamic,
                   "Forces:": forces
                   }
        with open('/home/pi/Cof-Tabs/data.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=2)

    def dump_time(self, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, test_mode, forces,
                  date_and_time):
        if sample2.name == "":
            dic = {"Company Name:": sample1.company_name,
                   "Operator Name:": sample1.operator_name,
                   "Testing Weight(gr):": sample1.testing_weight,
                   "Sample Name:": sample1.name,
                   "Sample Width(mm)": float(sample1.width),
                   "Sample Height(mm):": float(sample1.height),
                   "Sample Age(months):": float(sample1.age),
                   "Max Static Coefficient of Friction:": max_static,
                   "Mean Static Coefficient of Friction:": mean_static,
                   "Max Dynamic Coefficient of Friction:": max_dynamic,
                   "Mean Dynamic Coefficient of Friction:": mean_dynamic,
                   "Test date:": date_and_time,
                   "Forces:": forces
                   }
        else:
            dic = {"Company Name:": sample1.company_name,
                   "Operator Name:": sample1.operator_name,
                   "Testing Weight(gr):": sample1.testing_weight,
                   "First Sample Name:": sample1.name,
                   "First Sample Width(mm)": float(sample1.width),
                   "First Sample Height(mm):": float(sample1.height),
                   "First Sample Age(months):": float(sample1.age),
                   "Second Sample Name:": sample2.name,
                   "Second Sample Width(mm)": float(sample2.width),
                   "Second Sample Height(mm):": float(sample2.height),
                   "Second Sample Age(months):": float(sample2.age),
                   "Max Static Coefficient of Friction:": max_static,
                   "Mean Static Coefficient of Friction:": mean_static,
                   "Max Dynamic Coefficient of Friction:": max_dynamic,
                   "Mean Dynamic Coefficient of Friction:": mean_dynamic,
                   "Test date:": date_and_time,
                   "Forces:": forces
                   }

        file_name = "/home/pi/Cof-Tabs/rapor/COF_Test_" + date_and_time + ".json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=2)

    def read_data(self, file):
        with open(file) as json_file:
            data = json.load(json_file)
            if len(data) == 17:
                return data["Company Name:"], \
                       data["Operator Name:"], \
                       data["Testing Weight(gr):"], \
                       data["First Sample Name:"], \
                       data["First Sample Width(mm)"], \
                       data["First Sample Height(mm):"], \
                       data["First Sample Age(months):"], \
                       data["Second Sample Name:"], \
                       data["Second Sample Width(mm)"], \
                       data["Second Sample Height(mm):"], \
                       data["Second Sample Age(months):"], \
                       data["Max Static Coefficient of Friction:"], \
                       data["Mean Static Coefficient of Friction:"], \
                       data["Max Dynamic Coefficient of Friction:"], \
                       data["Mean Dynamic Coefficient of Friction:"], \
                       data["Test date:"], \
                       data["Forces:"]
            else:
                return data["Company Name:"], \
                       data["Operator Name:"], \
                       data["Testing Weight(gr):"], \
                       data["Sample Name:"], \
                       data["Sample Width(mm)"], \
                       data["Sample Height(mm):"], \
                       data["Sample Age(months):"], \
                       0, \
                       0, \
                       0, \
                       0, \
                       data["Max Static Coefficient of Friction:"], \
                       data["Mean Static Coefficient of Friction:"], \
                       data["Max Dynamic Coefficient of Friction:"], \
                       data["Mean Dynamic Coefficient of Friction:"], \
                       data["Test date:"], \
                       data["Forces:"]

    def dump_calib_save(self, distance, speed, normal_force, sample_time, calib):
        dic = {"Distance:": distance,
               "Speed:": speed,
               "Normal_Force:": normal_force,
               "Sample_Time:": sample_time,
               "Calibration value:": calib,
               }

        file_name = "/home/pi/Cof-Tabs/calibration_save.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=2)

    def import_save(self):
        file_name = "/home/pi/Cof-Tabs/calibration_save.json"
        with open(file_name) as json_file:
            data = json.load(json_file)
            return data["Distance:"], data["Speed:"], data["Normal_Force:"], data["Sample_Time:"], data[
                "Calibration value:"]
