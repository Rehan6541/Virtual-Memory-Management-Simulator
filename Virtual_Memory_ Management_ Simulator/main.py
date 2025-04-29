# main.py

import streamlit as st
from memory_manager import MemoryManager
from page_table import PageTable
from tlb import TLB
from process import Process
from utils import calculate_utilization

st.set_page_config(page_title="Virtual Memory Simulator", layout="wide")

st.title("🧠 Virtual Memory Management Simulator")

# Sidebar Inputs
memory_size = st.sidebar.number_input("Memory Size (in Frames)", min_value=4, max_value=64, value=16)
tlb_size = st.sidebar.number_input("TLB Size", min_value=2, max_value=10, value=4)
max_page_number = st.sidebar.number_input("Max Page Number (Process)", min_value=2, max_value=50, value=10)

# Initialize
if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager(memory_size)
    st.session_state.page_table = PageTable()
    st.session_state.tlb = TLB(tlb_size)
    st.session_state.process = Process(max_page_number)
    st.session_state.page_faults = 0
    st.session_state.tlb_hits = 0
    st.session_state.tlb_misses = 0

if st.button("Reset Simulator"):
    st.session_state.memory = MemoryManager(memory_size)
    st.session_state.page_table = PageTable()
    st.session_state.tlb = TLB(tlb_size)
    st.session_state.process = Process(max_page_number)
    st.session_state.page_faults = 0
    st.session_state.tlb_hits = 0
    st.session_state.tlb_misses = 0

# Process Memory Request
if st.button("Next Memory Access"):
    requested_page = st.session_state.process.generate_memory_request()
    st.subheader(f"Generated Memory Access Request: Page {requested_page}")

    frame_number = st.session_state.tlb.get(requested_page)

    if frame_number is not None:
        st.success(f"✅ TLB Hit! Page {requested_page} found in Frame {frame_number}")
        st.session_state.tlb_hits += 1
    else:
        st.session_state.tlb_misses += 1
        frame_number = st.session_state.page_table.get_frame(requested_page)
        if frame_number is not None:
            st.info(f"ℹ️ Page Table Hit: Page {requested_page} found in Frame {frame_number}")
        else:
            st.session_state.page_faults += 1
            frame_number, replaced = st.session_state.memory.allocate_frame(requested_page)
            st.session_state.page_table.update_entry(requested_page, frame_number)
            if replaced:
                st.warning(f"⚠️ Memory Full: Replaced page with Page {requested_page}")
            else:
                st.info(f"ℹ️ Page {requested_page} loaded into Frame {frame_number}")

        st.session_state.tlb.put(requested_page, frame_number)

# Layout Display
st.subheader("📦 Memory Frames")
frames = st.session_state.memory.memory_snapshot()
st.write({i: frames[i] for i in range(len(frames))})

st.subheader("📜 Page Table")
page_table_entries = st.session_state.page_table.get_all_entries()
st.write({page: (entry.frame_number, entry.valid) for page, entry in page_table_entries.items()})

st.subheader("⚡ TLB Entries")
tlb_entries = st.session_state.tlb.snapshot()
st.write(tlb_entries)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Page Faults", st.session_state.page_faults)
col2.metric("TLB Hits", st.session_state.tlb_hits)
col3.metric("TLB Misses", st.session_state.tlb_misses)
col4.metric("Memory Utilization (%)", f"{calculate_utilization(frames):.2f}")
