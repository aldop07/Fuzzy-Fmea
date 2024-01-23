import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Inisialisasi variabel FMEA
nilai_occurrence = ctrl.Antecedent(np.arange(0, 10), 'nilai_occurrence')
nilai_severity = ctrl.Antecedent(np.arange(0, 10), 'nilai_severity')
nilai_detectability = ctrl.Antecedent(np.arange(0, 10), 'nilai_detectability')
nilai_rpn = ctrl.Consequent(np.arange(0, 10), 'nilai_rpn')

# Fungsi keanggotaan untuk variabel input1 (Probability of occurrence)
nilai_occurrence['low'] = fuzz.trimf(nilai_occurrence.universe, [0, 0, 5])
nilai_occurrence['medium'] = fuzz.trimf(nilai_occurrence.universe, [0, 5, 10])
nilai_occurrence['high'] = fuzz.trimf(nilai_occurrence.universe, [5, 10, 10])

# Fungsi keanggotaan untuk variabel input2 (Severity)
nilai_severity['low'] = fuzz.trimf(nilai_severity.universe, [0, 0, 5])
nilai_severity['medium'] = fuzz.trimf(nilai_severity.universe, [0, 5, 10])
nilai_severity['high'] = fuzz.trimf(nilai_severity.universe, [5, 10, 10])

# Fungsi keanggotaan untuk variabel input3 (Detectability)
nilai_detectability['low'] = fuzz.trimf(nilai_detectability.universe, [0, 0, 5])
nilai_detectability['medium'] = fuzz.trimf(nilai_detectability.universe, [0, 5, 10])
nilai_detectability['high'] = fuzz.trimf(nilai_detectability.universe, [5, 10, 10])

# Fungsi keanggotaan untuk variabel output1 (RPN)
nilai_rpn['very_low'] = fuzz.trimf(nilai_rpn.universe, [0, 0, 2.5])
nilai_rpn['low'] = fuzz.trimf(nilai_rpn.universe, [0, 2.5, 5])
nilai_rpn['medium'] = fuzz.trimf(nilai_rpn.universe, [2.5, 5, 7.5])
nilai_rpn['high'] = fuzz.trimf(nilai_rpn.universe, [5, 7.5, 10])
nilai_rpn['very_high'] = fuzz.trimf(nilai_rpn.universe, [7.5, 10, 10])

# Atur aturan fuzzy menggunakan IF-THEN
# Aturan 1-27
rules1 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['low'] & nilai_detectability['low']), nilai_rpn['very_low'])
rules2 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['low'] & nilai_detectability['medium']), nilai_rpn['very_low'])
rules3 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['low'] & nilai_detectability['high']), nilai_rpn['low'])
rules4 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['medium'] & nilai_detectability['low']), nilai_rpn['low'])
rules5 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['medium'] & nilai_detectability['medium']), nilai_rpn['low'])
rules6 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['medium'] & nilai_detectability['high']), nilai_rpn['medium'])
rules7 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['high'] & nilai_detectability['low']), nilai_rpn['medium'])
rules8 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['high'] & nilai_detectability['medium']), nilai_rpn['medium'])
rules9 =ctrl.Rule((nilai_severity['low'] & nilai_occurrence['high'] & nilai_detectability['high']), nilai_rpn['high'])
rules10 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['low'] & nilai_detectability['low']), nilai_rpn['low'])
rules11 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['low'] & nilai_detectability['medium']), nilai_rpn['low'])
rules12 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['low'] & nilai_detectability['high']), nilai_rpn['medium'])
rules13 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['medium'] & nilai_detectability['low']), nilai_rpn['medium'])
rules14 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['medium'] & nilai_detectability['medium']), nilai_rpn['medium'])
rules15 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['medium'] & nilai_detectability['high']), nilai_rpn['high'])
rules16 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['high'] & nilai_detectability['low']), nilai_rpn['medium'])
rules17 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['high'] & nilai_detectability['medium']), nilai_rpn['high'])
rules18 =ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['high'] & nilai_detectability['high']), nilai_rpn['high'])
rules19 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['low'] & nilai_detectability['low']), nilai_rpn['medium'])
rules20 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['low'] & nilai_detectability['medium']), nilai_rpn['medium'])
rules21 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['low'] & nilai_detectability['high']), nilai_rpn['high'])
rules22 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['medium'] & nilai_detectability['low']), nilai_rpn['high'])
rules23 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['medium'] & nilai_detectability['medium']), nilai_rpn['high'])
rules24 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['medium'] & nilai_detectability['high']), nilai_rpn['very_high'])
rules25 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['high'] & nilai_detectability['low']), nilai_rpn['high'])
rules26 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['high'] & nilai_detectability['medium']), nilai_rpn['very_high'])
rules27 =ctrl.Rule((nilai_severity['high'] & nilai_occurrence['high'] & nilai_detectability['high']), nilai_rpn['very_high'])

# Tambahkan aturan-atur ini ke sistem kontrol
nilai_fmea_ctrl = ctrl.ControlSystem([rules1,rules2,rules3,rules4,rules5,rules6,rules7,rules8,rules9,rules10,rules11,rules12,rules13,rules14,rules15,rules16,rules17,rules18,rules19,rules20,rules21,rules22,rules23,rules24,rules25,rules26,rules27])

# Buat objek sistem kontrol dan simulasi
nilai_fmea = ctrl.ControlSystemSimulation(nilai_fmea_ctrl)

# Masukkan nilai-nilai FMEA yang ingin Anda fuzzifikasi
nilai_occurrence_value = st.number_input('masukan nilai O', 0)
nilai_severity_value = st.number_input('masukan nilai S', 0)
nilai_detectability_value = st.number_input('masukan nilai D', 0)

# Set nilai input pada sistem kontrol dan simulasi
nilai_fmea.input['nilai_occurrence'] = nilai_occurrence_value
nilai_fmea.input['nilai_severity'] = nilai_severity_value
nilai_fmea.input['nilai_detectability'] = nilai_detectability_value

# Dapatkan hasil fuzzifikasi
nilai_fmea.compute()

# Tampilkan hasil fuzzifikasi
st.write("Nilai RPN setelah fuzzifikasi:", nilai_fmea.output['nilai_rpn'])


# Defuzzifikasi
#hasil_defuzzifikasi = fuzz.defuzz(nilai_rpn.universe, nilai_fmea.output['nilai_rpn'].values, 'mean_of_maximum')

# Tampilkan hasil defuzzifikasi
#st.write("Hasil defuzzifikasi:", hasil_defuzzifikasi)


