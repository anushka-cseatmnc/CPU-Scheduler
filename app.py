import streamlit as st
import pandas as pd
import plotly.express as px

class Scheduler:
    def __init__(self, processes):
        # processes: list of dicts {'id': 'P1', 'at': 0, 'bt': 5}
        self.procs = processes

    def fcfs(self):
        procs = sorted([p.copy() for p in self.procs], key=lambda x: x['at'])
        time, gantt, results = 0, [], []
        for p in procs:
            if time < p['at']: time = p['at']
            start = time
            time += p['bt']
            gantt.append(dict(Task=p['id'], Start=start, Finish=time, Algo="FCFS"))
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
                time = procs[0]['at']
                continue
            
            ready_queue.sort(key=lambda x: x['bt'])
            p = ready_queue.pop(0)
            start = time
            time += p['bt']
            gantt.append(dict(Task=p['id'], Start=start, Finish=time, Algo="SJF"))
            results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

    def srtf_preemptive(self):
        procs = [p.copy() for p in self.procs]
        n = len(procs)
        rem_bt = {p['id']: p['bt'] for p in procs}
        time, completed, last_pid, start_time = 0, 0, None, 0
        results, gantt = [], []
        
        while completed < n:
            ready = [p for p in procs if p['at'] <= time and rem_bt[p['id']] > 0]
            if not ready:
                time += 1
                continue
            
            p = min(ready, key=lambda x: rem_bt[x['id']])
            
            if last_pid != p['id']:
                if last_pid is not None:
                    gantt.append(dict(Task=last_pid, Start=start_time, Finish=time, Algo="SRTF"))
                start_time = time
                last_pid = p['id']
            
            rem_bt[p['id']] -= 1
            time += 1
            
            if rem_bt[p['id']] == 0:
                completed += 1
                gantt.append(dict(Task=p['id'], Start=start_time, Finish=time, Algo="SRTF"))
                last_pid = None
                results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

    def round_robin(self, quantum):
        procs = sorted([p.copy() for p in self.procs], key=lambda x: x['at'])
        time, gantt, results = 0, [], []
        queue = []
        rem_bt = {p['id']: p['bt'] for p in procs}
        
        while procs or queue:
            while procs and procs[0]['at'] <= time:
                queue.append(procs.pop(0))
            if not queue:
                time = procs[0]['at']
                continue
            p = queue.pop(0)
            start = time
            exec_t = min(rem_bt[p['id']], quantum)
            time += exec_t
            rem_bt[p['id']] -= exec_t
            gantt.append(dict(Task=p['id'], Start=start, Finish=time, Algo="RR"))
            while procs and procs[0]['at'] <= time:
                queue.append(procs.pop(0))
            if rem_bt[p['id']] > 0: queue.append(p)
            else: results.append({**p, 'ct': time, 'tat': time - p['at'], 'wt': (time - p['at']) - p['bt']})
        return results, gantt

# --- STREAMLIT UI ---
st.set_page_config(page_title="OS Scheduler Expert", layout="wide")
st.title("📟 CPU Scheduling Simulator")

# Data Input Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    num_proc = st.number_input("Number of Processes", 1, 10, 3)
    data = []
    for i in range(num_proc):
        c1, c2 = st.columns(2)
        at = c1.number_input(f"P{i+1} Arrival", 0, 100, 0, key=f"at{i}")
        bt = c2.number_input(f"P{i+1} Burst", 1, 100, 2, key=f"bt{i}")
        data.append({'id': f"P{i+1}", 'at': at, 'bt': bt})
    
    q = st.slider("Round Robin Quantum", 1, 10, 2)

# Calculation
s = Scheduler(data)
res_fcfs, g_fcfs = s.fcfs()
res_sjf, g_sjf = s.sjf_non_preemptive()
res_srtf, g_srtf = s.srtf_preemptive()
res_rr, g_rr = s.round_robin(q)

# tabs
tab1, tab2 = st.tabs(["📊 Algorithm Analysis", "🏆 Performance Comparison"])

with tab1:
    algo_choice = st.selectbox("View Details For:", ["FCFS", "SJF", "SRTF (Preemptive)", "Round Robin"])
    mapping = {"FCFS": (res_fcfs, g_fcfs), "SJF": (res_sjf, g_sjf), 
               "SRTF (Preemptive)": (res_srtf, g_srtf), "Round Robin": (res_rr, g_rr)}
    
    current_res, current_gantt = mapping[algo_choice]
    
    # Gantt Chart
    df_gantt = pd.DataFrame(current_gantt)
    fig = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Task", title=f"{algo_choice} Gantt Chart")
    fig.layout.xaxis.type = 'linear'
    for i in range(len(fig.data)): fig.data[i].x = [df_gantt.iloc[i]['Finish'] - df_gantt.iloc[i]['Start']]
    st.plotly_chart(fig, use_container_width=True)
    
    st.table(pd.DataFrame(current_res)[['id', 'at', 'bt', 'ct', 'tat', 'wt']])

with tab2:
    comparison = {
        "Algorithm": ["FCFS", "SJF", "SRTF", "RR"],
        "Avg Waiting": [pd.DataFrame(res_fcfs)['wt'].mean(), pd.DataFrame(res_sjf)['wt'].mean(), 
                        pd.DataFrame(res_srtf)['wt'].mean(), pd.DataFrame(res_rr)['wt'].mean()],
        "Avg Turnaround": [pd.DataFrame(res_fcfs)['tat'].mean(), pd.DataFrame(res_sjf)['tat'].mean(), 
                           pd.DataFrame(res_srtf)['tat'].mean(), pd.DataFrame(res_rr)['tat'].mean()]
    }
    comp_df = pd.DataFrame(comparison)
    st.subheader("Efficiency Metrics")
    st.bar_chart(comp_df.set_index("Algorithm")["Avg Waiting"])
    st.table(comp_df)