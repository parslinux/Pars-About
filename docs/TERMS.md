# Terms of Service & Disclaimer (TERMS.md)

This document outlines the terms of use, limitations of warranty, and diagnostic data handling for **Pars About** (`org.parslinux.about`).

---

## 1. Scope and Purpose

Pars About is an open-source system and hardware inspection utility developed for Pars Linux and compatible GNU/Linux operating systems. It is intended to collect, display, and export technical system specifications, device states, and diagnostic metrics to aid users and administrators.

---

## 2. Disclaimer of Warranty (GPL-3.0+)

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the GNU General Public License for more details.

Neither the Pars Linux developers nor any contributors shall be liable for:
* Inaccurate or incomplete hardware telemetry reported by third-party drivers or BIOS/firmware.
* System instability caused by hardware overheating, stressed components, or third-party diagnostic utilities.
* Any indirect, incidental, or consequential damages resulting from the use or inability to use this software.

---

## 3. Diagnostic Data and Privacy

* **Local Execution**: All hardware inspection and diagnostic data collection are performed locally on the user's machine.
* **No Telemetry**: Pars About does not transmit hardware fingerprints, identifiers, or diagnostic archives to external cloud servers without explicit user instruction.
* **Sensitive Information in System Reports**: Generating a full system diagnostic archive (`/tmp/pars_system_report`) includes system logs and network configurations. Users are advised to review the contents of diagnostic archives before sharing them with third-party technical support teams.

---

## 4. Governing License

Pars About is licensed under the **GNU General Public License version 3 or later (GPL-3.0+)**. You are free to inspect, modify, and redistribute this software in accordance with the terms of the license.
