# TroubleshootingSim

A **Linux Troubleshooting Simulator**.  
This app intentionally *breaks* a Linux system in controlled ways — your job is to fix it.

It is designed for sysadmins, students, and anyone who wants to practice real-world Linux troubleshooting without destroying a production machine.

---

##  Safety Warning

**Do NOT run this on bare metal.**

TroubleshootingSim is built to:
- Corrupt settings
- Break networking
- Mess with storage
- Change boot / login configuration

Always run it in a **virtual machine** on a hypervisor (for example: VMware, VirtualBox, Proxmox, etc.), and **take a snapshot** before starting a scenario.

---

## Project Goals

- Simulate **real Linux failures** in a safe environment.
- Train users to:
  - Read and understand logs.
  - Use core troubleshooting tools (`journalctl`, `dmesg`, `ip`, `ss`, `ps`, `top`, `lsblk`, etc.).
  - Fix misconfigurations under pressure.
- Provide **repeatable scenarios** with:
  - Clear description of the problem.
  - Hidden “fault injection” scripts.
  - An automated checker that verifies your solution.

---

## Tech Stack

- **Python**  
  - Core controller that:
    - Selects scenarios.
    - Executes Bash scripts.
    - Tracks progress.
    - Runs checks to see if the issue is fixed.

- **Bash**  
  - Scenario scripts that:
    - Break the system (fault injection).
    - Optionally prepare the environment.

---


## Requirements

- A **Linux VM** (recommended: Ubuntu, Debian, CentOS, RHEL, Rocky, Alma, etc.).
- A **hypervisor**:
  - Recommended: **VMware** (easy snapshot handling).
  - Others: VirtualBox, Proxmox, etc.
- Python **3.9+** (adjust based on your environment).
- Basic admin rights inside the VM (you will probably need `sudo`).

---

## Final Note

To get the most out of this simulator, it is **highly recommended** that the user has foundational Linux administration knowledge.  
Ideally, you should study and understand the topics covered in **RHCSA (Red Hat Certified System Administrator)** or equivalent level skills **before attempting advanced scenarios**.

You *can* use the simulator as a learning tool while studying, but having RHCSA-level fundamentals will make the troubleshooting process more realistic, effective, and enjoyable.

