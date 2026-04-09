import streamlit as st
import pandas as pd
import plotly.express as px

# --- SCHEDULER LOGIC (YOUR CORE CODE) ---
class Scheduler:
    def __init__(self, processes):
        self.procs = processes

    def fcfs(self):
        procs = sorted([p.copy() for p in self.procs], key=lambda x: x['at'])
        time, gantt, results = 0, [], []
        for p in procs:
            if time < p['at']: time = p['at']
            start = time
            time += p['bt']
            gantt.append(dict(Task=p['id'], Start=start, Finish=time))
            results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

    def sjf_non_preemptive(self):
        procs = [p.copy() for p in self.procs]
        time, gantt, results = 0, [], []
        ready_queue = []
        while procs or ready_queue:
            ready_queue += [p for p in procs if p['at'] <= time]
            procs = [p for p in procs if p['at'] > time]
            if not ready_queue:
                if procs: time = procs[0]['at']
                else: break
                continue
            ready_queue.sort(key=lambda x: x['bt'])
            p = ready_queue.pop(0)
            start, time = time, time + p['bt']
            gantt.append(dict(Task=p['id'], Start=start, Finish=time))
            results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

    def srtf_preemptive(self):
        procs = [p.copy() for p in self.procs]
        n, time, completed = len(procs), 0, 0
        rem_bt = {p['id']: p['bt'] for p in procs}
        last_pid, start_time = None, 0
        results, gantt = [], []
        while completed < n:
            ready = [p for p in procs if p['at'] <= time and rem_bt[p['id']] > 0]
            if not ready:
                time += 1
                continue
            p = min(ready, key=lambda x: rem_bt[x['id']])
            if last_pid != p['id']:
                if last_pid is not None:
                    gantt.append(dict(Task=last_pid, Start=start_time, Finish=time))
                start_time, last_pid = time, p['id']
            rem_bt[p['id']] -= 1
            time += 1
            if rem_bt[p['id']] == 0:
                completed += 1
                gantt.append(dict(Task=p['id'], Start=start_time, Finish=time))
                last_pid = None
                results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

    def round_robin(self, quantum):
        procs = sorted([p.copy() for p in self.procs], key=lambda x: x['at'])
        time, gantt, results = 0, [], []
        queue, rem_bt = [], {p['id']: p['bt'] for p in procs}
        while procs or queue:
            while procs and procs[0]['at'] <= time:
                queue.append(procs.pop(0))
            if not queue:
                if procs: time = procs[0]['at']
                else: break
                continue
            p = queue.pop(0)
            start = time
            exec_t = min(rem_bt[p['id']], quantum)
            time += exec_t
            rem_bt[p['id']] -= exec_t
            gantt.append(dict(Task=p['id'], Start=start, Finish=time))
            while procs and procs[0]['at'] <= time:
                queue.append(procs.pop(0))
            if rem_bt[p['id']] > 0: queue.append(p)
            else: results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

# --- MODERN UI UPGRADE ---
st.set_page_config(page_title="OS Scheduler Expert", layout="wide", page_icon="📟")

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.title("📟 CPU Scheduling Simulation Dashboard")
st.info("Input process details to analyze and compare Operating System scheduling efficiency.")

# 1. Configuration Section
with st.container(border=True):
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        num_proc = st.number_input("Number of Processes", 1, 10, 3)
    with c2:
        algo_choice = st.segmented_control(
            "Select Scheduling Algorithm",
            options=["FCFS", "SJF", "SRTF (Preemptive)", "Round Robin"],
            default="FCFS"
        )
    with c3:
        q = st.number_input("RR Quantum", 1, 10, 2)

# 2. Process Input Grid
st.subheader("📝 Process Entry")
data = []
cols = st.columns(num_proc)
for i in range(num_proc):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"**Process P{i+1}**")
            at = st.number_input(f"Arrival", 0, 100, 0, key=f"at{i}")
            bt = st.number_input(f"Burst", 1, 100, 2, key=f"bt{i}")
            data.append({'id': f"P{i+1}", 'at': at, 'bt': bt})

# 3. Calculation Logic
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

# 4. Result Tabs
tab1, tab2 = st.tabs(["📊 Performance Analysis", "🏆 Algorithm Comparison"])

with tab1:
    # Metric Summary
    res_df = pd.DataFrame(current_res)
    m1, m2, m3 = st.columns(3)
    m1.metric("Selected Algorithm", algo_choice)
    m2.metric("Avg Waiting Time", f"{res_df['wt'].mean():.2f}ms")
    m3.metric("Avg Turnaround Time", f"{res_df['tat'].mean():.2f}ms")

    # Gantt Chart
    st.subheader(f"Timeline Visualization: {algo_choice}")
    df_gantt = pd.DataFrame(current_gantt)
    fig = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Task", 
                      template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    fig.layout.xaxis.type = 'linear'
    for i in range(len(fig.data)): 
        fig.data[i].x = [df_gantt.iloc[i]['Finish'] - df_gantt.iloc[i]['Start']]
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Process Table
    st.dataframe(res_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']], use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Global Performance Comparison")
    comparison = {
        "Algorithm": ["FCFS", "SJF", "SRTF", "RR"],
        "Avg Waiting": [pd.DataFrame(res_fcfs)['wt'].mean(), pd.DataFrame(res_sjf)['wt'].mean(), 
                        pd.DataFrame(res_srtf)['wt'].mean(), pd.DataFrame(res_rr)['wt'].mean()],
        "Avg Turnaround": [pd.DataFrame(res_fcfs)['tat'].mean(), pd.DataFrame(res_sjf)['tat'].mean(), 
                           pd.DataFrame(res_srtf)['tat'].mean(), pd.DataFrame(res_rr)['tat'].mean()]
    }
    comp_df = pd.DataFrame(comparison)
    
    col_chart, col_table = st.columns([2, 1])
    with col_chart:
        fig_comp = px.bar(comp_df, x="Algorithm", y=["Avg Waiting", "Avg Turnaround"], 
                          barmode="group", title="Comparative Metrics")
        st.plotly_chart(fig_comp, use_container_width=True)
    with col_table:
        st.table(comp_df)
