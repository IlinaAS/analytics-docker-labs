import streamlit as st
import requests
import pandas as pd
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")
st.set_page_config(page_title="Support Tickets", layout="wide")
st.title("🎫 Система техподдержки")

st.header("🆕 Создать тикет")
with st.form("ticket_form", clear_on_submit=True):
    author = st.text_input("Автор *")
    urgency = st.selectbox("Срочность *", ["low", "medium", "high", "critical"])
    description = st.text_area("Описание проблемы *")
    submitted = st.form_submit_button("📤 Создать")

    if submitted and author and description:
        try:
            payload = {"author": author, "urgency": urgency, "description": description}
            resp = requests.post(f"{BACKEND_URL}/tickets", json=payload, timeout=10)
            if resp.status_code == 201:
                st.success(f"✅ Тикет #{resp.json()['id']} создан!")
            else:
                st.error(f"❌ Ошибка: {resp.text}")
        except Exception as e:
            st.error(f"🔌 Ошибка: {e}")

st.header("📋 Тикеты")
if st.button("🔄 Обновить"):
    st.rerun()
try:
    resp = requests.get(f"{BACKEND_URL}/tickets", timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            df = pd.DataFrame(data)
            df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
            st.dataframe(df[["id","description","author","urgency","status","created_at"]], use_container_width=True)

            # 🔽 Блок изменения статуса
            st.subheader("✏️ Изменить статус тикета")
            col1, col2 = st.columns(2)
            with col1:
                ticket_id = st.number_input("ID тикета", min_value=1, step=1)
            with col2:
                new_status = st.selectbox("Новый статус", ["open", "in_progress", "resolved", "closed"])

            if st.button("💾 Сохранить"):
                try:
                    update_resp = requests.put(f"{BACKEND_URL}/tickets/{ticket_id}", json={"status": new_status}, timeout=10)
                    if update_resp.status_code == 200:
                        st.success("✅ Статус обновлён!")
                        st.rerun()
                    else:
                        st.error(f"❌ Ошибка: {update_resp.text}")
                except Exception as e:
                    st.error(f"🔌 Ошибка: {e}")
        else:
            st.info("📭 Нет тикетов")
except Exception as e:
    st.error(f"⚠️ {e}")

