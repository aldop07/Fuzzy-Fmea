#import numpy as np
#import skfuzzy as fuzz
#from skfuzzy import control as ctrl
#import streamlit as st

# Input variables
#occurrence = ctrl.Antecedent(np.arange(0, 10, 1), 'Probability_of_occurrence')
#severity = ctrl.Antecedent(np.arange(0, 10, 1), 'Severity')
#detectability = ctrl.Antecedent(np.arange(0, 10), 'Detectability')

# Output variable
#rpn = ctrl.Consequent(np.arange(0, 10, 1), 'RPN')

# Define membership functions
#occurrence['low'] = fuzz.trimf(occurrence.universe, [0, 0, 5])
#occurrence['medium'] = fuzz.trimf(occurrence.universe, [0, 5, 10])
#occurrence['high'] = fuzz.trimf(occurrence.universe, [5, 10, 10])

#severity['low'] = fuzz.trimf(severity.universe, [0, 0, 5])
#severity['medium'] = fuzz.trimf(severity.universe, [0, 5, 10])
#severity['high'] = fuzz.trimf(severity.universe, [5, 10, 10])

#detectability['low'] = fuzz.trimf(detectability.universe, [0, 0, 5])
#detectability['medium'] = fuzz.trimf(detectability.universe, [0, 5, 10])
#detectability['high'] = fuzz.trimf(detectability.universe, [5, 10, 10])

#rpn['very_low'] = fuzz.trimf(rpn.universe, [0, 0, 2.5])
#rpn['medium'] = fuzz.trimf(rpn.universe, [2.5, 5, 7.5])
#rpn['low'] = fuzz.trimf(rpn.universe, [0, 2.5, 5])
#rpn['high'] = fuzz.trimf(rpn.universe, [5, 7.5, 10])
#rpn['very_high'] = fuzz.trimf(rpn.universe, [7.5, 10, 10])

# Rules
#rules1 =ctrl.Rule((severity['low'] & occurrence['low'] & detectability['low']), rpn['very_low'])
#rules2 =ctrl.Rule((severity['low'] & occurrence['low'] & detectability['medium']), rpn['very_low'])
#rules3 =ctrl.Rule((severity['low'] & occurrence['low'] & detectability['high']), rpn['low'])
#rules4 =ctrl.Rule((severity['low'] & occurrence['medium'] & detectability['low']), rpn['low'])
#rules5 =ctrl.Rule((severity['low'] & occurrence['medium'] & detectability['medium']), rpn['low'])
#rules6 =ctrl.Rule((severity['low'] & occurrence['medium'] & detectability['high']), rpn['medium'])
#rules7 =ctrl.Rule((severity['low'] & occurrence['high'] & detectability['low']), rpn['medium'])
#rules8 =ctrl.Rule((severity['low'] & occurrence['high'] & detectability['medium']), rpn['medium'])
#rules9 =ctrl.Rule((severity['low'] & occurrence['high'] & detectability['high']), rpn['high'])
#rules10 =ctrl.Rule((severity['medium'] & occurrence['low'] & detectability['low']), rpn['low'])
#rules11 =ctrl.Rule((severity['medium'] & occurrence['low'] & detectability['medium']), rpn['low'])
#rules12 =ctrl.Rule((severity['medium'] & occurrence['low'] & detectability['high']), rpn['medium'])
#rules13 =ctrl.Rule((severity['medium'] & occurrence['medium'] & detectability['low']), rpn['medium'])
#rules14 =ctrl.Rule((severity['medium'] & occurrence['medium'] & detectability['medium']), rpn['medium'])
#rules15 =ctrl.Rule((severity['medium'] & occurrence['medium'] & detectability['high']), rpn['high'])
#rules16 =ctrl.Rule((severity['medium'] & occurrence['high'] & detectability['low']), rpn['medium'])
#rules17 =ctrl.Rule((severity['medium'] & occurrence['high'] & detectability['medium']), rpn['high'])
#rules18 =ctrl.Rule((severity['medium'] & occurrence['high'] & detectability['high']), rpn['high'])
#rules19 =ctrl.Rule((severity['high'] & occurrence['low'] & detectability['low']), rpn['medium'])
#rules20 =ctrl.Rule((severity['high'] & occurrence['low'] & detectability['medium']), rpn['medium'])
#rules21 =ctrl.Rule((severity['high'] & occurrence['low'] & detectability['high']), rpn['high'])
#rules22 =ctrl.Rule((severity['high'] & occurrence['medium'] & detectability['low']), rpn['high'])
#rules23 =ctrl.Rule((severity['high'] & occurrence['medium'] & detectability['medium']), rpn['high'])
#rules24 =ctrl.Rule((severity['high'] & occurrence['medium'] & detectability['high']), rpn['very_high'])
#rules25 =ctrl.Rule((severity['high'] & occurrence['high'] & detectability['low']), rpn['high'])
#rules26 =ctrl.Rule((severity['high'] & occurrence['high'] & detectability['medium']), rpn['very_high'])
#rules27 =ctrl.Rule((severity['high'] & occurrence['high'] & detectability['high']), rpn['very_high'])

# Create control system
#fuzzy_ctrl = ctrl.ControlSystem([rules1,rules2,rules3,rules4,rules5,rules6,rules7,rules8,rules9,rules10,rules11,rules12,rules13,rules14,rules15,rules16,rules17,rules18,rules19,rules20,rules21,rules22,rules23,rules24,rules25,rules26,rules27])
#fuzzy_system = ctrl.ControlSystemSimulation(fuzzy_ctrl)

# Set input values
#fuzzy_system.input['Probability_of_occurrence'] = st.number_input('masukan nilai O', 0)
#fuzzy_system.input['Severity'] = st.number_input('masukan nilai S', 0)
#fuzzy_system.input['Detectability'] = st.number_input('masukan nilai D', 0)

# Perform fuzzy inference
#fuzzy_system.compute()

# Print the output
#print("Fuzzy RPN:", fuzzy_system.output['RPN'])

# Visualize the results (optional)
#o = occurrence.view(sim=fuzzy_system)
#s = severity.view(sim=fuzzy_system)
#d = detectability.view(sim=fuzzy_system)
#rpn = rpn.view(sim=fuzzy_system)

# Show the plots
#import matplotlib.pyplot as plt
#st.pyplot(o)
#st.pyplot(s)
#st.pyplot(d)
#st.pyplot(rpn)

import numpy as np
import streamlit as st
import pandas as pd
import math
# HITUNG VOLUME YANG HARUS DIPOTONG DAN KEBUTUHAN CUTTING DISC
CCALCULATE = st.selectbox('CONSUMABLE CALCULATE', ['CUTTING DISC','GRINDING DISC', 'FLAP DISC', 'FILLER WELD', 'ARGON', 'COATING'])

if CCALCULATE == 'CUTTING DISC':

    JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate','UNP','WF','H BEAM'])

    if JMATERIAL == 'Pipe':

        NPS = st.selectbox('NPS', [
            '1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
            '3 1/2','4','5','6','8','10','12','14','16','18','20','22',
            '24','26','28','30'
        ])

        SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])

        JPOTONG = st.number_input('Jumlah Pipe Dipotong', min_value=0)

        if st.button('HITUNG'):

            KERF = 3  # tebal cutting disc tetap 3 mm

            data_pipe = {
                "1/4": {"OD":13.7,"30":10,"40":9.22,"80":7.66},
                "3/8": {"OD":17.1,"30":13.4,"40":12.48,"80":10.7},
                "1/2": {"OD":21.3,"10":17.08,"40":15.76,"80":13.84},
                "3/4": {"OD":26.7,"10":22.48,"40":20.96,"80":18.88},
                "1": {"OD":33.4,"10":27.86,"40":26.64,"80":24.3},
                "1 1/4": {"OD":42.2,"10":36.66,"40":35.08,"80":32.5},
                "1 1/2": {"OD":48.3,"10":42.76,"40":40.94,"80":38.14},
                "2": {"OD":60.3,"10":54.76,"40":52.48,"80":49.22},
                "2 1/2": {"OD":73,"10":66.9,"40":62.68,"80":58.98},
                "3": {"OD":88.9,"10":82.8,"40":77.92,"80":73.66},
                "4": {"OD":114.3,"10":108.2,"40":102.26,"80":97.18},
                "5": {"OD":141.3,"40":128.2,"80":122.24},
                "6": {"OD":168.3,"40":154.08,"80":146.36}
            }

            pipe = data_pipe.get(NPS)

            if pipe and SCH in pipe:

                OD = pipe["OD"]
                ID = pipe[SCH]

                volume_cut = (math.pi/4) * (OD**2 - ID**2) * KERF
                total_volume = volume_cut * JPOTONG

                volume_disc = 12280.77

                kebutuhan_disc = total_volume / volume_disc
                kebutuhan_disc_bulat = math.ceil(kebutuhan_disc)

                st.write(f"Total volume potong : {total_volume:,.2f} mm3")
                st.write(f"Kebutuhan cutting disc : {kebutuhan_disc:,.2f} pcs")
                st.write(f"Kebutuhan aktual : {kebutuhan_disc_bulat} pcs")

            else:
                st.warning("Data SCH tidak tersedia untuk ukuran ini")

elif CCALCULATE == 'GRINDING DISC':

    JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe'])

    if JMATERIAL == 'Pipe':

        NPS = st.selectbox('NPS', [
        '1/4','3/8','1/2','3/4','1','1 1/4','1 1/2','2','2 1/2','3',
        '3 1/2','4','5','6','8','10','12','14','16','18','20','22',
        '24','26','28','30'
        ])

        SCH = st.selectbox('SCH', ['10','20','30','40','60','80'])

        JJOINT = st.number_input('Jumlah Joint Beveling', min_value=0)

        if st.button('HITUNG'):

            # DATABASE PIPE (dari tabel)
            pipe_data = {
            "1/4":{"OD":13.7,"30":10,"40":9.22,"80":7.66},
            "3/8":{"OD":17.1,"30":13.4,"40":12.48,"80":10.7},
            "1/2":{"OD":21.3,"10":17.08,"40":15.76,"80":13.84},
            "3/4":{"OD":26.7,"10":22.48,"40":20.96,"80":18.88},
            "1":{"OD":33.4,"10":27.86,"40":26.64,"80":24.3},
            "1 1/4":{"OD":42.2,"10":36.66,"40":35.08,"80":32.5},
            "1 1/2":{"OD":48.3,"10":42.76,"40":40.94,"80":38.14},
            "2":{"OD":60.3,"10":54.76,"40":52.48,"80":49.22},
            "2 1/2":{"OD":73,"10":66.9,"40":62.68,"80":58.98},
            "3":{"OD":88.9,"10":82.8,"40":77.92,"80":73.66},
            "3 1/2":{"OD":101.6,"10":95.5,"40":90.12,"80":85.44},
            "4":{"OD":114.3,"10":108.2,"40":102.26,"80":97.18},
            "5":{"OD":141.3,"10":134.5,"40":128.2,"80":122.24},
            "6":{"OD":168.3,"10":161.5,"40":154.08,"80":146.36},
            "8":{"OD":219.1,"10":211.58,"20":206.4,"30":205.02,"40":202.74,"60":198.48,"80":193.7},
            "10":{"OD":273,"10":264.62,"20":260.3,"30":257.4,"40":254.46,"60":247.6,"80":242.82},
            "12":{"OD":323.8,"10":314.66,"20":311.1,"30":307.04,"40":303.18,"60":295.26,"80":288.84},
            "14":{"OD":355.5,"10":342.9,"20":339.76,"30":336.54,"40":333.34,"60":325.42,"80":317.5},
            "16":{"OD":406.4,"10":393.7,"20":390.56,"30":387.34,"40":381,"60":373.08,"80":363.52}
            }

            pipe = pipe_data.get(NPS)

            if pipe and SCH in pipe:

                OD = pipe["OD"]
                ID = pipe[SCH]

                # thickness
                t = (OD - ID)/2

                # bevel angle 60°
                h = t / math.tan(math.radians(30))

                R = OD/2
                r = ID/2

                # volume bevel
                volume_bevel = (math.pi*h/3)*(R**2 + R*r + r**2)

                total_volume = volume_bevel * JJOINT

                disc_capacity = 5
                kebutuhan_disc = JJOINT / disc_capacity
                kebutuhan_disc_bulat = math.ceil(kebutuhan_disc)

                volume_disc = volume_bevel * disc_capacity

                st.write(f"Volume Bevel per Joint : {volume_bevel:,.2f} mm³")
                st.write(f"Total Volume Bevel : {total_volume:,.2f} mm³")


                st.write(f"Kebutuhan Grinding Disc : {kebutuhan_disc:,.2f} pcs")
                st.write(f"Kebutuhan Aktual : {kebutuhan_disc_bulat} pcs")

            else:
                st.warning("Data SCH tidak tersedia untuk ukuran ini")

elif CCALCULATE == 'FLAP DISC':
    # HITUNG VOLUME YANG HARUS DIPOTONG DAN KEBUTUHAN CUTTING DISC
    JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate', 'UNP', 'WF', 'H BEAM'])
    
elif CCALCULATE == 'FILLER WELD':
    # HITUNG VOLUME YANG HARUS DIPOTONG DAN KEBUTUHAN CUTTING DISC
    JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate', 'UNP', 'WF', 'H BEAM'])
    
elif CCALCULATE == 'ARGON':
    # HITUNG VOLUME YANG HARUS DIPOTONG DAN KEBUTUHAN CUTTING DISC
    JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate', 'UNP', 'WF', 'H BEAM'])
    
elif CCALCULATE == 'COATING':

    JMATERIAL = st.selectbox('JENIS MATERIAL', ['Pipe','Plate','UNP','WF','H BEAM'])

    if JMATERIAL == 'Pipe':

        JCOATING = st.selectbox(
            'JENIS CAT',
            ['Cat jotun futura classic clay brown ral 8003','Cat Jotun Solvalit Black','Cat jotun easy prime grey ral 38']
        )

        NPS = st.selectbox('NPS', ['1/2"','1"','1 1/2"','2"','2 1/2"','3"','4"'])
        JPANJANG = st.number_input('Masukan panjang pipe yang akan di coating (mm)', min_value=0)

        if st.button('HITUNG'):

            keliling_data = {
                '1/2"'  : 66.882,
                '1"'    : 108.876,
                '1 1/2"': 151.662,
                '2"'    : 189.342,
                '2 1/2"': 229.2,
                '3"'    : 279.146,
                '4"'    : 358.902
            }

            keliling_pipe = keliling_data.get(NPS)
            
            coating_data = {
                'Cat jotun futura classic clay brown ral 8003'  : 1633140,
                'Cat jotun easy prime grey ral 38'  : 3408156,
                'Cat Jotun Solvalit Black'    : 3190240
            }
            coating = coating_data.get(JCOATING,0)


            if keliling_pipe:

                total_luas = JPANJANG * keliling_pipe
                kebutuhan_cat = total_luas / coating
                kebutuhan_coating = math.ceil(kebutuhan_cat)
                
                st.write(f"Total Luas Coating : {total_luas:,.2f} mm2")
                st.write(f"Kebutuhan Coating : {kebutuhan_cat:,.2f} kg")
                st.write(f"Kebutuhan Aktual (dibulatkan) : {kebutuhan_coating} kg")

            else:
                st.warning("Data ukuran pipe tidak tersedia")


