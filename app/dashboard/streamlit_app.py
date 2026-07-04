import httpx
import streamlit as st

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="AI Job Apply Ops", layout="wide")
st.title("AI Job Apply Operations")

try:
    profile = httpx.get(f"{API_URL}/profile/local", timeout=5).json()
except Exception:
    profile = None

if profile:
    st.caption(
        f"Local profile: {profile['full_name']} | Target role: {profile['target_role']} | "
        f"{profile['location']}"
    )
    if st.button("Run Product Manager Dry Run", type="primary"):
        with st.spinner("Analyzing resume against a safe Product Manager test job..."):
            response = httpx.post(f"{API_URL}/campaigns/product-manager-dry-run", timeout=60)
        if response.is_success:
            result = response.json()
            analysis = result.get("analysis", {})
            st.success("Dry run completed. No real application or email was sent.")
            st.json(
                {
                    "status": result.get("status"),
                    "match_score": analysis.get("match_score"),
                    "category": analysis.get("category"),
                    "approval_tasks": result.get("approval_tasks", []),
                }
            )
        else:
            st.error(response.text)

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
