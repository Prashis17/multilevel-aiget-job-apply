import httpx
import streamlit as st

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="AI Job Apply Ops", layout="wide")
st.title("AI Job Apply Operations")

cols = st.columns(4)
try:
    analytics = httpx.get(f"{API_URL}/analytics", timeout=5).json()
except Exception:
    analytics = {}

cols[0].metric("Applications", sum(analytics.values()))
cols[1].metric("Pending", analytics.get("pending", 0))
cols[2].metric("Applied", analytics.get("applied", 0))
cols[3].metric("Failed", analytics.get("failed", 0))

st.subheader("Recent Jobs")
try:
    jobs = httpx.get(f"{API_URL}/jobs", timeout=5).json()
    st.dataframe(jobs, use_container_width=True)
except Exception as exc:
    st.info(f"API not reachable: {exc}")

