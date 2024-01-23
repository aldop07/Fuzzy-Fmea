import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

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
nilai_rpn['medium'] = fuzz.trimf(nilai_rpn.universe, [2.5, 5, 7.5])
nilai_rpn['low'] = fuzz.trimf(nilai_rpn.universe, [0, 2.5, 5])
nilai_rpn['high'] = fuzz.trimf(nilai_rpn.universe, [5, 7.5, 10])
nilai_rpn['very_high'] = fuzz.trimf(nilai_rpn.universe, [7.5, 10, 10])

# Atur aturan fuzzy menggunakan IF-THEN
# Aturan 1-27
rules = [
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['low'] & nilai_detectability['low']), nilai_rpn['very_low']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['low'] & nilai_detectability['medium']), nilai_rpn['very_low']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['low'] & nilai_detectability['high']), nilai_rpn['low']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['medium'] & nilai_detectability['low']), nilai_rpn['low']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['medium'] & nilai_detectability['medium']), nilai_rpn['low']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['medium'] & nilai_detectability['high']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['high'] & nilai_detectability['low']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['high'] & nilai_detectability['medium']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['low'] & nilai_occurrence['high'] & nilai_detectability['high']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['low'] & nilai_detectability['low']), nilai_rpn['low']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['low'] & nilai_detectability['medium']), nilai_rpn['low']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['low'] & nilai_detectability['high']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['medium'] & nilai_detectability['low']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['medium'] & nilai_detectability['medium']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['medium'] & nilai_detectability['high']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['high'] & nilai_detectability['low']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['high'] & nilai_detectability['medium']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['medium'] & nilai_occurrence['high'] & nilai_detectability['high']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['low'] & nilai_detectability['low']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['low'] & nilai_detectability['medium']), nilai_rpn['medium']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['low'] & nilai_detectability['high']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['medium'] & nilai_detectability['low']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['medium'] & nilai_detectability['medium']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['medium'] & nilai_detectability['high']), nilai_rpn['very_high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['high'] & nilai_detectability['low']), nilai_rpn['high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['high'] & nilai_detectability['medium']), nilai_rpn['very_high']),
    ctrl.Rule((nilai_severity['high'] & nilai_occurrence['high'] & nilai_detectability['high']), nilai_rpn['very_high']),
]

# Tambahkan aturan-atur ini ke sistem kontrol
nilai_fmea_ctrl = ctrl.ControlSystem(rules)

# Buat objek sistem kontrol dan simulasi
nilai_fmea = ctrl.ControlSystemSimulation(nilai_fmea_ctrl)

# Masukkan nilai-nilai FMEA yang ingin Anda fuzzifikasi
nilai_fmea.input['nilai_occurrence'] = st.number_input(0)
nilai_fmea.input['nilai_severity'] = st.number_input(0)
nilai_fmea.input['nilai_detectability'] = st.number_input(0)

# Jalankan simulasi
nilai_fmea.compute()

# Dapatkan hasil fuzzifikasi
print("Nilai RPN setelah fuzzifikasi:", nilai_fmea.output['nilai_rpn'])
o = nilai_occurrence.view()
st.pyplot(0)
