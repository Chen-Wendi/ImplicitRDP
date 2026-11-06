

<h3 align="center">
    ImplicitRDP:
</h3>
<h4 align="center">
    An End-to-End Visual-Force Diffusion Policy with Structural Slow-Fast Learning
</h4>

<p align="center">
    <a href="https://wendichen.me">Wendi Chen</a><sup>12</sup>,
    <a href="https://hanxue.me">Han Xue</a><sup>2</sup>,
    Yi Wang<sup>12</sup>,
    <a href="https://uimicro.com">Fangyuan Zhou</a><sup>12</sup>,
    <a href="https://lyuj1998.github.io">Jun Lv</a><sup>23</sup>,
    <a href="https://github.com/EricJin2002">Yang Jin</a><sup>2</sup>,
    Shirun Tang<sup>3</sup>,
    <br>
    <a href="https://alvinwen428.github.io">Chuan Wen</a><sup>2†</sup>,
    <a href="https://www.mvig.org">Cewu Lu</a><sup>123†</sup>
    <br>
    <sup>1</sup>Shanghai Innovation Institute
    <sup>2</sup>Shanghai Jiao Tong University
    <sup>3</sup>Noematrix Ltd.
    <br>
    <sup>*</sup>Equal contribution
    <sup>†</sup>Equal advising
    <br>
</p>

<div align="center">
<a href='https://arxiv.org/abs/2512.10946'><img alt='arXiv' src='https://img.shields.io/badge/arXiv-2512.10946-red.svg'></a> &nbsp;&nbsp;&nbsp;&nbsp;
<a href='https://implicit-rdp.github.io'><img alt='project website' src='https://img.shields.io/website-up-down-green-red/http/cv.lbesson.qc.to.svg'></a> &nbsp;&nbsp;&nbsp;&nbsp;
<a href='https://huggingface.co/datasets/WendiChen/ImplicitRDP_dataset'><img alt='data' src='https://img.shields.io/badge/data-FFD21E?logo=huggingface&logoColor=000'></a> &nbsp;&nbsp;&nbsp;&nbsp;
<a href='https://huggingface.co/WendiChen/ImplicitRDP_model'><img alt='checkpoints' src='https://img.shields.io/badge/checkpoints-FFD21E?logo=huggingface&logoColor=000'></a> &nbsp;&nbsp;&nbsp;&nbsp;
<img alt='powered by Pytorch' src='https://img.shields.io/badge/PyTorch-❤️-F8C6B5?logo=pytorch&logoColor=white'> &nbsp;&nbsp;&nbsp;&nbsp;
</div>

<p align="center">
<img src="assets/teaser.png" alt="teaser" style="width:75%;" />
</p>

## ⚙️ Environment Setup
### 📝 Use Customized Force Sensors, Robots and Customized Tasks
Please refer to [docs/customized_deployment_guide.md](docs/customized_deployment_guide.md).

### Hardware
- Workstation with Ubuntu 22.04 for compatibility with ROS2 Humble.
    > A workstation with a GPU (e.g., NVIDIA RTX 3090) is required.
- 1 robot arms with a 6-axis force/torque sensor at the end effector.
    > We use [Flexiv Rizon 4s](https://www.flexiv.com/products/rizon).
- 1 USB camera or [RealSense](https://www.intelrealsense.com) camera.
    > We use an off-the-shelf USB camera for external camera.
      Follow the [official document](https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide) to install librealsense2 if you use RealSense camera.
- (Optional) A single-button keyboard for controlling kinematic teaching.
  > We assign this button as the “pause” key. When the button is pressed, the robot can be dragged for teaching. You can modify the used key in [ImplicitRDP/real_world/kinematic_teaching/kineteach_controller.py](ImplicitRDP/real_world/kinematic_teaching/kineteach_controller.py).

<p align="center">
<img src="assets/hardware_settings.png" alt="hardware settings" style="width:50%;" />
</p>

### Software
1. Follow the [official document](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) to install ROS2 Humble.
2. Since ROS2 has some compatibility issues with Conda, we recommend using a virtual environment with `venv`.
   ```bash
   python3 -m venv implicitrdp_venv
   source implicitrdp_venv/bin/activate
   pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121
   pip install -r requirements.txt
   ```
3. We perform manual CPU core binding to reducing the delay caused by the OS scheduler.
    1. Add config into `/etc/security/limits.conf` to ensure the user has the permission to set realtime priority.
        ```
        username - rtprio 99
        ```
    2. Edit `/etc/default/grub` and add `isolcpus=xxx` to the `GRUB_CMDLINE_LINUX_DEFAULT` line
    for isolating certain CPU cores.
    3. Modify the task config file (e.g. [ImplicitRDP/config/task/real_flip_one_usb_camera_kineteach_10fps.yaml](ImplicitRDP/config/task/real_flip_one_usb_camera_kineteach_10fps.yaml)) and the beginning several lines of all entry-point Python files (e.g. [control.py](control.py)) to adjust the corresponding core binding.

## 📦 Data Collection
### Kinematic Teaching
The environment and the task have to be configured first and then start several services for performing kinematic teaching, publishing sensor data and record the data.
  1. Environment and Task Configuration.
        - **Environment Configuration.**
          Edit [ImplicitRDP/config/task/real_robot_env.yaml](ImplicitRDP/config/task/real_robot_env.yaml) to configure the environment settings including `host_ip` and `robot_serial_number`.
          Note that the VR config options exist solely for compatibility with the original Reactive Diffusion Policy, so you don't need to modify them.
        - **Task Configuration.**
          Create task config file which assigns the camera and sensor to use.
          You can take [ImplicitRDP/config/task/real_flip_one_usb_camera_kineteach_10fps.yaml](ImplicitRDP/config/task/real_flip_one_usb_camera_kineteach_10fps.yaml)
          as an example.
          Refer to [docs/customized_deployment_guide.md](docs/customized_deployment_guide.md) for more details.
   2. Start services. Run each command in a separate terminal. You can use tmux to split the terminal.
      ```bash
      # start controlling service
      python control.py task=[task_config_file_name]
      # start camera node launcher
      python camera_node_launcher.py task=[task_config_file_name]
      # start data recorder
      python record_data.py --save_to_disk --vis_wrench --save_file_dir [task_data_dir] --save_file_name [record_seq_file_name]
      ```
  3. Press the "pause" button to enable the kinematic teaching.

### Data Collection Tips
Please refer to [docs/data_collection_tips.md](docs/data_collection_tips.md).

### Example Data
We provide the data we collected on [![data](https://img.shields.io/badge/data-FFD21E?logo=huggingface&logoColor=000)](https://huggingface.co/datasets/WendiChen/ImplicitRDP_dataset).

## 📚 Training
1. **Task Configuration.**
   In addition to the task config file used in [data collection](#-data-collection),
   another file is needed to configure dataset, runner, and model-related parameters such as `obs` and `action`.
   You can take [ImplicitRDP/config/task/real_flip_image_wrench_implicitrdp_10fps.yaml](ImplicitRDP/config/task/real_flip_image_wrench_implicitrdp_10fps.yaml) as an example.
   Refer to [docs/customized_deployment_guide.md](docs/customized_deployment_guide.md) for more details.
   > The `dp`, `at`, `ldp`, `dpt`, `vrr`, `fp`, `no aux` in the config file name indicate the Diffusion policy, Asymmetric Tokenizer, Latent Diffusion Policy, Diffusion Policy (Transformer), Virtual-target-based Representation Regularization, Force Prediction and No Auxiliary Task.
2. **Run the Training Script.**
   We provide training scripts for Diffusion Policy, Reactive Diffusion Policy, Diffusion Policy (Transformer) and ImplicitRDP.
   The scripts will first post-process the data and then train the model.
   You can modify the training script to train the desired task and model.
   ```bash
   # config multi-gpu training
   accelerate config
   # Diffusion Policy
   ./train_dp.sh
   # Reactive Diffusion Policy
   ./train_rdp.sh
   # Diffusion Policy (Transformer)
   ./train_dpt.sh
   # ImplicitRDP
   ./train_implicitrdp.sh
   ```
   > Make sure the `action_type` when post-processing the data is consistent with the task config file.

## 🚀 Inference
1. (Optional) Refer to `vcamera_server_ip` and `vcamera_server_port` in the task config file and start the corresponding vcamera server.
If you want to record experiment videos with MindVision cameras, follow [third_party/mvsdk/README.md](third_party/mvsdk/README.md) to install MindVision SDK.
We also support recording videos with RealSense or USB cameras.
   ```bash
   # run vcamera server
   python vcamera_server.py --host_ip [host_ip] --port [port] --camera_type [camera_type] --camera_id [camera_id] --fps [fps]
   ```
2. Modify [eval.sh](eval.sh) to set the task and model you want to evaluate and run the command in separate terminals.
   ```bash
   # start controlling service
   python control.py task=[task_config_file_name]
   # start camera node launcher
   python camera_node_launcher.py task=[task_config_file_name]
   # start inference
   ./eval.sh
   ```

### Checkpoints
We provide the checkpoints in our experiments on [![checkpoints](https://img.shields.io/badge/checkpoints-FFD21E?logo=huggingface&logoColor=000)](https://huggingface.co/WendiChen/ImplicitRDP_model).

## 🙏 Acknowledgement
Our work is built upon
[Reactive Diffusion Policy](https://github.com/xiaoxiaoxh/reactive_diffusion_policy),
[Diffusion Policy](https://github.com/real-stanford/diffusion_policy),
[VQ-BeT](https://github.com/jayLEE0301/vq_bet_official),
[Stable Diffusion](https://github.com/CompVis/stable-diffusion),
[UMI](https://github.com/real-stanford/universal_manipulation_interface)
and [Data Scaling Laws](https://github.com/Fanqi-Lin/Data-Scaling-Laws).
Thanks for their great work!

## 🔗 Citation
If you find our work useful, please consider citing:
```
@article{chen2025implicitrdp,
  title     = {ImplicitRDP: An End-to-End Visual-Force Diffusion Policy with Structural Slow-Fast Learning},
  author    = {Chen, Wendi and Xue, Han and Wang, Yi and Zhou, Fangyuan and Lv, Jun and Jin, Yang and Tang, Shirun and Wen, Chuan and Lu, Cewu},
  journal   = {arXiv preprint arXiv:2512.10946},
  year      = {2025}
}

@inproceedings{xue2025reactive,
  title     = {Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation},
  author    = {Xue, Han and Ren, Jieji and Chen, Wendi and Zhang, Gu and Fang, Yuan and Gu, Guoying and Xu, Huazhe and Lu, Cewu},
  booktitle = {Proceedings of Robotics: Science and Systems (RSS)},
  year      = {2025}
}
```
