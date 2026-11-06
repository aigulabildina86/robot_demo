import json
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Роботтың келесі әрекеті", page_icon="🤖")
st.title("🤖 Робот тоқтай ма, әлде солға бұрыла ма?")
st.write("Алдымен өз болжамыңызды айтыңыз. Содан кейін модельдің жауабын ашыңыз.")

model_path = Path(__file__).with_name("robot_model.json")
feature_names = ["Алдыңғы қашықтық", "Сол жақтағы бос орын"]

with st.form("robot_inputs"):
    front = st.slider("Алдыңғы кедергіге дейінгі қашықтық (см)", 5, 45, 18)
    left = st.slider("Сол жақтағы бос орын (см)", 5, 45, 8)
    submitted = st.form_submit_button("Модельдің болжамын көрсету")

if submitted:
    node = json.loads(model_path.read_text(encoding="utf-8"))
    values = [front, left]
    steps = []

    while "action" not in node:
        feature = node["feature"]
        threshold = node["threshold"]
        value = values[feature]
        take_left = value <= threshold
        comparison = "≤" if take_left else ">"
        steps.append(
            f"{feature_names[feature]} — {value} см {comparison} {threshold:g} см"
        )
        node = node["left" if take_left else "right"]

    st.success(f"Модельдің болжамы — **{node['action']}**")

    with st.expander("Модель қай көрсеткіштерге сүйенді?"):
        for step in steps:
            st.write(step)

st.caption("Модель оқу мақсатында құрастырылған жасанды деректермен үйретілді.")
