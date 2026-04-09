# --- STREAMLIT UI UPGRADE ---
st.set_page_config(page_title="OS Scheduler Expert", layout="wide", page_icon="📟")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 CPU Scheduling Simulator")
st.info("💡 Input your process details below to compare OS scheduling efficiency.")

# --- TOP INPUT SECTION ---
with st.container(border=True):
    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        num_proc = st.number_input("Number of Processes", 1, 10, 3)
    with c2:
        # PROFESSIONAL SELECTOR: Horizontal & Clean
        algo_choice = st.segmented_control(
            "Select Scheduling Algorithm to Visualize",
            options=["FCFS", "SJF", "SRTF (Preemptive)", "Round Robin"],
            default="FCFS"
        )
    with c3:
        q = st.number_input("RR Quantum", 1, 10, 2)

# --- PROCESS INPUT GRID ---
st.subheader("📝 Process Details")
data = []
# Create a grid of inputs so they don't take up too much vertical space
cols = st.columns(num_proc)
for i in range(num_proc):
    with cols[i]:
        st.markdown(f"**Process P{i+1}**")
        at = st.number_input(f"Arrival", 0, 100, 0, key=f"at{i}", label_visibility="collapsed")
        bt = st.number_input(f"Burst", 1, 100, 2, key=f"bt{i}", label_visibility="collapsed")
        data.append({'id': f"P{i+1}", 'at': at, 'bt': bt})

# --- CALCULATION LOGIC ---
s = Scheduler(data)
res_fcfs, g_fcfs = s.fcfs()
res_sjf, g_sjf = s.sjf_non_preemptive()
res_srtf, g_srtf = s.srtf_preemptive()
res_rr, g_rr = s.round_robin(q)

mapping = {
    "FCFS": (res_fcfs, g_fcfs), 
    "SJF": (res_sjf, g_sjf), 
    "SRTF (Preemptive)": (res_srtf, g_srtf), 
    "Round Robin": (res_rr, g_rr)
}
current_res, current_gantt = mapping[algo_choice]

# --- DASHBOARD LAYOUT ---
tab1, tab2 = st.tabs(["📊 Live Analysis", "🏆 Performance Comparison"])

with tab1:
    # Metric Highlights
    avg_wt = pd.DataFrame(current_res)['wt'].mean()
    avg_tat = pd.DataFrame(current_res)['tat'].mean()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Selected Algorithm", algo_choice)
    m2.metric("Avg Waiting Time", f"{avg_wt:.2f}ms")
    m3.metric("Avg Turnaround Time", f"{avg_tat:.2f}ms")

    # Gantt Chart
    st.subheader(f"Timeline: {algo_choice}")
    df_gantt = pd.DataFrame(current_gantt)
    fig = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Task", 
                      template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    fig.layout.xaxis.type = 'linear'
    for i in range(len(fig.data)): 
        fig.data[i].x = [df_gantt.iloc[i]['Finish'] - df_gantt.iloc[i]['Start']]
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Results Table
    st.dataframe(pd.DataFrame(current_res)[['id', 'at', 'bt', 'ct', 'tat', 'wt']], 
                 use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Comparative Efficiency")
    comparison = {
        "Algorithm": ["FCFS", "SJF", "SRTF", "RR"],
        "Avg Waiting": [pd.DataFrame(res_fcfs)['wt'].mean(), pd.DataFrame(res_sjf)['wt'].mean(), 
                        pd.DataFrame(res_srtf)['wt'].mean(), pd.DataFrame(res_rr)['wt'].mean()],
        "Avg Turnaround": [pd.DataFrame(res_fcfs)['tat'].mean(), pd.DataFrame(res_sjf)['tat'].mean(), 
                           pd.DataFrame(res_srtf)['tat'].mean(), pd.DataFrame(res_rr)['tat'].mean()]
    }
    comp_df = pd.DataFrame(comparison)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        # Combined chart for comparison
        fig_comp = px.bar(comp_df, x="Algorithm", y=["Avg Waiting", "Avg Turnaround"], 
                          barmode="group", title="Waiting vs Turnaround Time")
        st.plotly_chart(fig_comp, use_container_width=True)
    with c2:
        st.write("### Comparison Table")
        st.table(comp_df)
