<div align="center">

# JNEEG

**A brain-computer interface with a GPU on board.**

Open-source 8-channel shield that turns the NVIDIA Jetson Nano into an EEG, EMG and ECG device with the TI ADS1299.

[📖 Documentation](https://docs.pieeg.com/hardware/devices/jneeg/) ·
[🚀 How to Start](https://docs.pieeg.com/hardware/devices/jneeg/setup/) ·
[🛒 Buy](https://pieeg.com/jneeg/) ·
[💬 Discord](https://discord.gg/5Ps24p47)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/jneeg_board.jpg" alt="JNEEG shield on a Jetson Nano" width="320">

</div>

> [!WARNING]
> JNEEG is **not a medical device** and has not been certified by any regulator for use with the human body. It is a tool for research, education and engineering. You use it at your own risk.

> [!CAUTION]
> **Battery only.** The Jetson Nano, the shield and everything cabled to them (monitor, keyboard) must run from a **5 V power bank** while electrodes are on a person. Never use the Jetson's wall power supply, a mains-powered monitor, or an Ethernet cable. The board has **no isolation**. Read the [Safety page](https://docs.pieeg.com/hardware/devices/jneeg/safety/) and the [liability notice](https://pieeg.com/liability/).

## At a glance

| | |
|---|---|
| **Channels** | 8 biosignal inputs, plus reference and bias |
| **Converter** | TI ADS1299, 24-bit, simultaneous sampling |
| **Sample rate** | 250 SPS |
| **Signals** | EEG, EMG, ECG |
| **Host** | NVIDIA Jetson Nano Developer Kit |
| **Link to the Jetson** | SPI on the 40-pin header, DRDY on pin 7 |
| **Electrodes** | Dry or wet Ag/AgCl, 2.54 mm header |
| **Power** | 5 V power bank, 3 A, up to 10,000 mAh |
| **Software** | [PiEEG Server](https://github.com/pieeg-club/PiEEG-server) (`--device jneeg`), Python scripts (this repo) |

## How it works

```
 Electrodes 1–8 ─┐
 Reference (ear) ┼─► JNEEG ──SPI──► Jetson Nano ──► PiEEG Server
 Bias (ear) ─────┘   (ADS1299)      (GPU)          ├ dashboard :1617
                                      ▲            ├ WebSocket :1616
           5 V power bank ────────────┘            └ your ML models
```

The Jetson Nano's GPU lets you run neural networks on the EEG **right on the device**: real-time classification, neural decoding, or EEG combined with a camera.

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/jneeg_kit.jpg" alt="JNEEG kit: 1 JNEEG on the Jetson Nano, 2 ear-clip electrodes, 3 EEG cap, 4 power bank" width="560">

## Quick start

1. **Flash JetPack** to a microSD card and boot the Jetson Nano once.
2. **Enable SPI:**

```bash
sudo /opt/nvidia/jetson-io/jetson-io.py      # Configure 40-pin header → enable spi1 → Save and reboot
ls /dev/spidev0.0                            # check after the reboot
sudo groupadd -f spi && sudo usermod -aG spi,gpio "$USER"   # then log out and in
```

3. **Mount** the shield on the 40-pin header (Jetson switched off), and **connect** 8 electrodes, a reference ear clip and a bias ear clip.
4. **Power** the Jetson from a 5 V / 3 A **power bank** via its Micro-USB port. The LED on the shield lights up.
5. **Run** the live graph from this repo, or PiEEG Server:

```bash
# Python scripts (stock JetPack Python)
cd GUI && python3 1.Graph_real_time.py

# or PiEEG Server (needs Python 3.10+)
pip install "pieeg-server[rpi]"
pieeg-server --device jneeg                  # dashboard at http://localhost:1617
```

> [!NOTE]
> PiEEG Server needs **Python 3.10 or newer**. JetPack 4 for the Jetson Nano ships Python 3.6, so install a newer Python first, or use the Python scripts in this repo.

Full walkthrough: **[docs.pieeg.com → JNEEG → How to Start](https://docs.pieeg.com/hardware/devices/jneeg/setup/)**

## Wiring

| Input | Electrode | Purpose |
|---|---|---|
| **Channels 1–8** | EEG electrodes in a cap (10-20 system) | Signal |
| **Reference** | Ear clip on one earlobe | Common 0 µV point for all channels |
| **Bias** | Ear clip on the other earlobe | Cancels common-mode noise (mains hum) |

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/jneeg_pinout.png" alt="JNEEG: electrode header, ADS1299, low-noise regulators, status LED and 40-pin header" width="700">

### Jetson Nano pinout

| Header pin | Signal |
|---|---|
| 19 | SPI MOSI |
| 21 | SPI MISO |
| 23 | SPI SCK |
| 24 | SPI CS0 |
| 7 | DRDY (data ready) |

The scripts read DRDY as **board pin 7** with `Jetson.GPIO`; PiEEG Server reads it as line **216** on `/dev/gpiochip0`.

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/jneeg_on_nano.jpg" alt="JNEEG mounted on the Jetson Nano" width="360">

## Software

### Python scripts (this repo)

| Script | What it does |
|---|---|
| [`GUI/1.Graph_real_time.py`](GUI/1.Graph_real_time.py) | Live 8-channel graph, band-pass filtered (1–10 Hz by default) |
| [`GUI/2.Save_data.py`](GUI/2.Save_data.py) | Save raw µV for all 8 channels to Excel after 10,000 samples (40 s) |
| [`GUI/dataset/Data_visualisation.py`](GUI/dataset) | Plot a saved file |

```bash
sudo apt install -y python3-pip python3-matplotlib python3-scipy
pip3 install spidev pandas openpyxl
cd GUI
python3 1.Graph_real_time.py
```

The scripts use `Jetson.GPIO` (preinstalled on JetPack) and `spidev`, with SPI at 600 kHz, mode 1.

### PiEEG Server

`--device jneeg` applies the `jetson-nano` profile automatically (600 kHz SPI, GPIO on `/dev/gpiochip0`):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install "pieeg-server[rpi]"
pieeg-server doctor
pieeg-server --device jneeg
```

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2025/05/pieeg-1024x485.jpg" alt="PiEEG Server dashboard" width="650">

If samples never arrive, check the DRDY line offset for your JetPack release with `gpioinfo gpiochip0` and pass `--gpio-chip /dev/gpiochip0`.

All options: **[Software docs](https://docs.pieeg.com/hardware/devices/jneeg/software/)**

## Example recording

20 seconds from the dataset in [`GUI/dataset`](GUI/dataset), 8 channels, band-pass 1–40 Hz. The large bursts are artifacts such as blinks or chewing.

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/jneeg_recording.png" alt="JNEEG example recording: 8 channels, band-pass 1–40 Hz" width="700">

**Dataset:** [`GUI/dataset/output1.xlsx`](GUI/dataset): 8 channels, 10,000 samples (40 s at 250 SPS), raw µV.

## Ideas for the GPU

- **Eyes-closed detector:** alpha power once per second switches something on.
- **Blink and jaw-clench control:** use artifacts on the front channels as buttons.
- **EEG + camera:** combine a webcam model with EEG features in one app.
- **Mental-state classifier:** train a small network on band-power features and run it with PyTorch or TensorRT.

## What's in this repository

| Folder | Content |
|---|---|
| [`GUI`](GUI) | Python scripts: live graph and saving data |
| [`GUI/dataset`](GUI/dataset) | Example recording and plotting script |
| [`GUI/with_c_library_not_support`](GUI/with_c_library_not_support) | Older C version with `c-periphery` (no longer supported) |
| [`Supplementary files`](Supplementary%20files) | Images used in the original README |

## Documentation

| Page | |
|---|---|
| [JNEEG Intro](https://docs.pieeg.com/hardware/devices/jneeg/) | Overview, comparison with PiEEG-8 |
| [What's in the Box](https://docs.pieeg.com/hardware/devices/jneeg/required-equipment/) | What you need besides the shield |
| [How to Start](https://docs.pieeg.com/hardware/devices/jneeg/setup/) | Step-by-step setup and first signal checks |
| [Electrodes & Pinout](https://docs.pieeg.com/hardware/devices/jneeg/connections/) | Wiring, montage, header pins |
| [Software](https://docs.pieeg.com/hardware/devices/jneeg/software/) | PiEEG Server, Python scripts, ML on the GPU |
| [Signals & Datasets](https://docs.pieeg.com/hardware/devices/jneeg/examples/) | Example recording, dataset, project ideas |
| [Specification](https://docs.pieeg.com/hardware/devices/jneeg/specification/) | Data frame, µV conversion, ADS1299 registers |
| [Troubleshooting](https://docs.pieeg.com/hardware/devices/jneeg/troubleshooting/) | SPI, GPIO, Python version and noise fixes |
| [Safety](https://docs.pieeg.com/hardware/devices/jneeg/safety/) | Battery-only operation and responsible use |

Also: [Manual on Google Colab](https://colab.research.google.com/drive/1xW6fwzVdLH83zHoorjeWai6SdZoOanfA)

## Citation

If you use JNEEG in research, please cite:

```
I. Rakhmatulin. Device JNEEG to convert Jetson Nano to brain-computer interfaces.
Short report. arXiv:2301.11110, 2023.
```

## Contact

- 🌐 [pieeg.com](https://pieeg.com/)
- 📖 [docs.pieeg.com](https://docs.pieeg.com/)
- 💬 [Discord](https://discord.gg/5Ps24p47)
- ✉️ [pieeg@pieeg.com](mailto:pieeg@pieeg.com)
