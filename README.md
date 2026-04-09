# 🖥️ CPU Scheduling Simulator (OS)

A high-performance web-based simulator designed to visualize and compare various CPU scheduling algorithms. This tool is built to help students and developers understand how Operating Systems manage process execution, timing, and resource allocation.

---

## 🚀 Live Demo
**View the App here:** https://cpu-scheduler-dedwtjcwkwrtjatk3txgpy.streamlit.app/ 

<img width="1919" height="966" alt="Screenshot 2026-04-09 142648" src="https://github.com/user-attachments/assets/b5acf6aa-50fb-4339-80ce-4f6e8b127636" />
<img width="1919" height="962" alt="Screenshot 2026-04-09 142702" src="https://github.com/user-attachments/assets/2caba1d9-6a1c-4043-81fc-0fd8cfe92eca" />
<img width="1917" height="973" alt="Screenshot 2026-04-09 142712" src="https://github.com/user-attachments/assets/ec29ce9e-415f-4347-bf63-f0c158587a7e" />
<img width="1919" height="965" alt="Screenshot 2026-04-09 142728" src="https://github.com/user-attachments/assets/669846df-8e1a-4529-b550-b26ebe2f3b37" />



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
