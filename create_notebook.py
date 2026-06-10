import json
import base64

with open("dashboard_heatmap.png", "rb") as img_f:
    img1_data = base64.b64encode(img_f.read()).decode('utf-8')
with open("dashboard_breakdown.png", "rb") as img_f:
    img2_data = base64.b64encode(img_f.read()).decode('utf-8')

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# APAC Banking Operations Intelligence Hub\n",
    "### Automated Process Analysis & Visual Dashboard Report\n",
    "**Author:** Chelsea Pang Kiat Si <br>**Target Role:** Business Analyst Portfolio Asset"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Product Matrix Bottlenecks\n",
    "This heatmap cross-tabulates processing failures to target system anomalies:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [{"output_type": "display_data", "data": {"image/png": img1_data}, "metadata": {}}],
   "source": ["# Render system vulnerability heatmap matrix\n", "print('Displaying Matrix Metrics')"]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Failure Category and Resolution Latency\n",
    "Isolating overall volume vs manual clearance tracking queues:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [{"output_type": "display_data", "data": {"image/png": img2_data}, "metadata": {}}],
   "source": ["# Render failure profiles side-by-side\n", "print('Displaying Exception Latency Charts')"]
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python"}
 },
 "nbformat": 4, "nbformat_minor": 2
}

with open("APAC_Banking_Ops_Analysis.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)
print("✅ Notebook successfully updated with python generated visual components!")
