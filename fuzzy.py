import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st

# Input variables
occurrence = ctrl.Antecedent(np.arange(0, 10, 1), 'Probability_of_occurrence')
severity = ctrl.Antecedent(np.arange(0, 10, 1), 'Severity')
detectability = ctrl.Antecedent(np.arange(0, 10), 'Detectability')

# Output variable
rpn = ctrl.Consequent(np.arange(0, 10, 1), 'RPN')

# Define membership functions
occurrence['low'] = fuzz.trimf(occurrence.universe, [0, 0, 5])
occurrence['medium'] = fuzz.trimf(occurrence.universe, [0, 5, 10])
occurrence['high'] = fuzz.trimf(occurrence.universe, [5, 10, 10])

severity['low'] = fuzz.trimf(severity.universe, [0, 0, 5])
severity['medium'] = fuzz.trimf(severity.universe, [0, 5, 10])
severity['high'] = fuzz.trimf(severity.universe, [5, 10, 10])

detectability['low'] = fuzz.trimf(detectability.universe, [0, 0, 5])
detectability['medium'] = fuzz.trimf(detectability.universe, [0, 5, 10])
detectability['high'] = fuzz.trimf(detectability.universe, [5, 10, 10])

rpn['very_low'] = fuzz.trimf(rpn.universe, [0, 0, 2.5])
rpn['medium'] = fuzz.trimf(rpn.universe, [2.5, 5, 7.5])
rpn['low'] = fuzz.trimf(rpn.universe, [0, 2.5, 5])
rpn['high'] = fuzz.trimf(rpn.universe, [5, 7.5, 10])
rpn['very_high'] = fuzz.trimf(rpn.universe, [7.5, 10, 10])

# Rules
rules1 =ctrl.Rule((severity['low'] & occurrence['low'] & detectability['low']), rpn['very_low'])
rules2 =ctrl.Rule((severity['low'] & occurrence['low'] & detectability['medium']), rpn['very_low'])
rules3 =ctrl.Rule((severity['low'] & occurrence['low'] & detectability['high']), rpn['low'])
rules4 =ctrl.Rule((severity['low'] & occurrence['medium'] & detectability['low']), rpn['low'])
rules5 =ctrl.Rule((severity['low'] & occurrence['medium'] & detectability['medium']), rpn['low'])
rules6 =ctrl.Rule((severity['low'] & occurrence['medium'] & detectability['high']), rpn['medium'])
rules7 =ctrl.Rule((severity['low'] & occurrence['high'] & detectability['low']), rpn['medium'])
rules8 =ctrl.Rule((severity['low'] & occurrence['high'] & detectability['medium']), rpn['medium'])
rules9 =ctrl.Rule((severity['low'] & occurrence['high'] & detectability['high']), rpn['high'])
rules10 =ctrl.Rule((severity['medium'] & occurrence['low'] & detectability['low']), rpn['low'])
rules11 =ctrl.Rule((severity['medium'] & occurrence['low'] & detectability['medium']), rpn['low'])
rules12 =ctrl.Rule((severity['medium'] & occurrence['low'] & detectability['high']), rpn['medium'])
rules13 =ctrl.Rule((severity['medium'] & occurrence['medium'] & detectability['low']), rpn['medium'])
rules14 =ctrl.Rule((severity['medium'] & occurrence['medium'] & detectability['medium']), rpn['medium'])
rules15 =ctrl.Rule((severity['medium'] & occurrence['medium'] & detectability['high']), rpn['high'])
rules16 =ctrl.Rule((severity['medium'] & occurrence['high'] & detectability['low']), rpn['medium'])
rules17 =ctrl.Rule((severity['medium'] & occurrence['high'] & detectability['medium']), rpn['high'])
rules18 =ctrl.Rule((severity['medium'] & occurrence['high'] & detectability['high']), rpn['high'])
rules19 =ctrl.Rule((severity['high'] & occurrence['low'] & detectability['low']), rpn['medium'])
rules20 =ctrl.Rule((severity['high'] & occurrence['low'] & detectability['medium']), rpn['medium'])
rules21 =ctrl.Rule((severity['high'] & occurrence['low'] & detectability['high']), rpn['high'])
rules22 =ctrl.Rule((severity['high'] & occurrence['medium'] & detectability['low']), rpn['high'])
rules23 =ctrl.Rule((severity['high'] & occurrence['medium'] & detectability['medium']), rpn['high'])
rules24 =ctrl.Rule((severity['high'] & occurrence['medium'] & detectability['high']), rpn['very_high'])
rules25 =ctrl.Rule((severity['high'] & occurrence['high'] & detectability['low']), rpn['high'])
rules26 =ctrl.Rule((severity['high'] & occurrence['high'] & detectability['medium']), rpn['very_high'])
rules27 =ctrl.Rule((severity['high'] & occurrence['high'] & detectability['high']), rpn['very_high'])

# Create control system
fuzzy_ctrl = ctrl.ControlSystem([rules1,rules2,rules3,rules4,rules5,rules6,rules7,rules8,rules9,rules10,rules11,rules12,rules13,rules14,rules15,rules16,rules17,rules18,rules19,rules20,rules21,rules22,rules23,rules24,rules25,rules26,rules27])
fuzzy_system = ctrl.ControlSystemSimulation(fuzzy_ctrl)

# Set input values
fuzzy_system.input['Probability_of_occurrence'] = st.number_input('masukan nilai O', 0)
fuzzy_system.input['Severity'] = st.number_input('masukan nilai S', 0)
fuzzy_system.input['Detectability'] = st.number_input('masukan nilai D', 0)

# Perform fuzzy inference
fuzzy_system.compute()

# Print the output
print("Fuzzy RPN:", fuzzy_system.output['RPN'])

# Visualize the results (optional)
o = occurrence.view(sim=fuzzy_system)
s = severity.view(sim=fuzzy_system)
d = detectability.view(sim=fuzzy_system)
rpn = rpn.view(sim=fuzzy_system)

# Show the plots
import matplotlib.pyplot as plt
st.pyplot(o)
st.pyplot(s)
st.pyplot(d)
st.pyplot(rpn)
