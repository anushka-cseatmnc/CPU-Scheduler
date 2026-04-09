# 🖥️ CPU Scheduling Simulator (OS)

A high-performance web-based simulator designed to visualize and compare various CPU scheduling algorithms. This tool is built to help students and developers understand how Operating Systems manage process execution, timing, and resource allocation.

---

## 🚀 Live Demo
**View the App here:** https://cpu-scheduler-dedwtjcwkwrtjatk3txgpy.streamlit.app/ 


---

## ✨ Features

### 🧩 Core Algorithms
The simulator supports four fundamental scheduling policies:
* **First Come First Serve (FCFS):** Non-preemptive, simple FIFO logic.
* **Shortest Job First (SJF):** Non-preemptive, prioritizes shortest burst times.
* **Shortest Remaining Time First (SRTF):** Preemptive version of SJF—swaps processes if a shorter task arrives.
* **Round Robin (RR):** Time-sliced scheduling with a customizable Time Quantum.

### 🔥 Advanced Visualization
* **Interactive Gantt Charts:** Dynamic timelines built with Plotly to show process switching and preemption.
* **Performance Metrics:** Automatic calculation of **Completion Time (CT)**, **Turnaround Time (TAT)**, and **Waiting Time (WT)**.
* **Side-by-Side Comparison:** A dedicated dashboard to compare the efficiency (Average WT/TAT) of all algorithms for the same data set.

---

## 📊 Mathematical Logic Used

The simulator calculates metrics based on the standard OS formulas:

- **Turnaround Time ($TAT$):** $Completion Time - Arrival Time$
- **Waiting Time ($WT$):** $Turnaround Time - Burst Time$

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Frontend Framework:** [Streamlit](https://streamlit.io/) (for UI/UX)
- **Data Handling:** Pandas
- **Visualization:** Plotly (for Gantt charts)

---

## ⚙️ Installation & Local Setup

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone git@github.com:anushka-cseatmnc/CPU-Scheduler.git
   cd CPU-Scheduler
