import os
import pickle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

font_path = "/Users/wendi/Library/Fonts/Calibri.ttf"
font_manager.fontManager.addfont(font_path)
bold_font_path = "/Users/wendi/Library/Fonts/Calibri-Bold.ttf"
font_manager.fontManager.addfont(bold_font_path)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

def smooth_curve(data, window_size):
    smoothed = []
    for i in range(len(data)):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(data), i + window_size // 2 + 1)
        smoothed.append(sum(data[start_idx:end_idx]) / (end_idx - start_idx))
    return smoothed

# Create a figure with 3 subplots (one above the other)
fig, axes = plt.subplots(3, 1, figsize=(10, 9), constrained_layout=True)

configs = zip(["assets/attention/switch_irdp", "assets/attention/switch_irdp_fp", "assets/attention/switch_irdp_vrr"], 
              ["ImplicitRDP w. None Auxiliary Task", "ImplicitRDP w. Force Prediction", "ImplicitRDP w. Virtual Target Prediction (Ours)"])

lines = []
labels = []

for i, ((attn_dir, fig_name), ax) in enumerate(zip(configs, axes)):

    attn_files = [f for f in os.listdir(attn_dir) if f.startswith("attn_weights_") and f.endswith(".pkl")]
    time_attn = []
    slow_img_obs_attn = []
    slow_tcp_obs_attn = []
    slow_wrench_obs_attn = []
    temporal_cond_attn = []
    for attn_file in sorted(attn_files, key=lambda x: int(x.split('_')[-1].split('.')[0])):
        with open(os.path.join(attn_dir, attn_file), 'rb') as f:
            attn_dict = pickle.load(f)
            time_attn.append(attn_dict["time"])
            slow_img_obs_attn.append(attn_dict["slow_img_obs"])
            slow_tcp_obs_attn.append(attn_dict["slow_tcp_obs"])
            slow_wrench_obs_attn.append(attn_dict["slow_wrench_obs"])
            temporal_cond_attn.append(attn_dict["temporal_cond"])

    # smoothing the curve
    window_size = 10
    time_attn = smooth_curve(time_attn, window_size)
    slow_img_obs_attn = smooth_curve(slow_img_obs_attn, window_size)
    slow_tcp_obs_attn = smooth_curve(slow_tcp_obs_attn, window_size)
    slow_wrench_obs_attn = smooth_curve(slow_wrench_obs_attn, window_size)
    temporal_cond_attn = smooth_curve(temporal_cond_attn, window_size)

    # Plot on the specific subplot
    l1, = ax.plot(slow_img_obs_attn, label='Slow Image Tokens', linewidth=3)
    l2, = ax.plot(temporal_cond_attn, label='Fast Force Tokens', linewidth=3)
    
    # Collect handles/labels for the shared legend from the first plot
    if i == 0:
        lines = [l1, l2]
        labels = [l.get_label() for l in lines]

    ax.set_xlabel('Steps', fontsize=22)
    ax.set_ylabel('Attention', fontsize=22)
    ax.set_yticks([0.0, 0.4])
    if "(Ours)" in fig_name:
        ax.set_title(fig_name, fontsize=22, fontweight='bold')
    else:
        ax.set_title(fig_name, fontsize=22)
    ax.tick_params(labelsize=18)

# Add a shared legend
fig.legend(lines, labels, fontsize=22, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)

# Save the figure as a PDF
plt.savefig('figs/attention/attention.pdf', dpi=300, bbox_inches='tight')
