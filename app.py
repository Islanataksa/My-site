
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="EduMind AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduMind AI")
st.subheader("Интеллектуальная система анализа образования")

st.write(
    "Система анализирует успеваемость и посещаемость "
    "учеников и помогает выявлять трудности."
)

subjects = ["Математика", "Английский", "История"]

np.random.seed(42)

df = pd.DataFrame({
    "Ученик": [f"Ученик {i}" for i in range(1, 51)],
    "Математика": np.random.randint(40, 101, 50),
    "Английский": np.random.randint(40, 101, 50),
    "История": np.random.randint(40, 101, 50),
    "Посещаемость": np.random.randint(60, 101, 50),
    "Тест": np.random.randint(40, 101, 50)
})

st.header("📂 Загрузка данных")

uploaded_file = st.file_uploader(
    "Загрузите таблицу CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

df["Средний балл"] = df[
    subjects + ["Тест"]
].mean(axis=1).round(1)

st.header("📊 Общая статистика")

col1, col2, col3 = st.columns(3)

col1.metric("Количество учеников", len(df))
col2.metric("Средний балл", round(df["Средний балл"].mean(), 1))
col3.metric(
    "Посещаемость",
    f"{df['Посещаемость'].mean():.1f}%"
)

st.header("📈 Успеваемость по предметам")

subject_means = df[subjects].mean().reset_index()
subject_means.columns = ["Предмет", "Средний балл"]

fig1 = px.bar(
    subject_means,
    x="Предмет",
    y="Средний балл",
    color="Предмет",
    range_y=[0, 100]
)

st.plotly_chart(fig1, use_container_width=True)

st.header("📉 Посещаемость и успеваемость")

fig2 = px.scatter(
    df,
    x="Посещаемость",
    y="Средний балл",
    hover_name="Ученик",
    range_x=[0, 100],
    range_y=[0, 100]
)

st.plotly_chart(fig2, use_container_width=True)

st.header("👩‍🎓 Анализ учеников")
st.dataframe(df, use_container_width=True)

st.header("🤖 Рекомендации системы")

for _, student in df.iterrows():
    problems = []

    if student["Средний балл"] < 60:
        problems.append("Нужно улучшить общую успеваемость")

    if student["Посещаемость"] < 80:
        problems.append("Нужно улучшить посещаемость")

    for subject in subjects:
        if student[subject] < 50:
            problems.append(f"Нужно подтянуть предмет: {subject}")

    if problems:
        st.warning(
            f"**{student['Ученик']}**: " + "; ".join(problems)
        )

weakest_subject = df[subjects].mean().idxmin()

st.header("📌 Итоговый вывод")

st.write(
    f"Предмет, требующий наибольшего внимания: "
    f"**{weakest_subject}**."
)
