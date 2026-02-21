import json

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

roc_cell_source = [
    "# ROC Curve (One-vs-Rest for Multiclass)\n",
    "from sklearn.preprocessing import label_binarize\n",
    "from sklearn.metrics import roc_curve, auc\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "\n",
    "# Binarize the labels for one-vs-rest\n",
    "y_test_bin = label_binarize(y_test, classes=[0, 1, 2, 3])\n",
    "y_score = model.predict(X_test)  # predicted probabilities\n",
    "\n",
    "colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']\n",
    "\n",
    "plt.figure(figsize=(10, 7))\n",
    "\n",
    "for i, (class_name, color) in enumerate(zip(classes, colors)):\n",
    "    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])\n",
    "    roc_auc = auc(fpr, tpr)\n",
    "    plt.plot(fpr, tpr, color=color, lw=2,\n",
    "             label=f'{class_name} (AUC = {roc_auc:.2f})')\n",
    "\n",
    "# Diagonal reference line\n",
    "plt.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Classifier')\n",
    "\n",
    "plt.xlim([0.0, 1.0])\n",
    "plt.ylim([0.0, 1.05])\n",
    "plt.xlabel('False Positive Rate', fontsize=13)\n",
    "plt.ylabel('True Positive Rate', fontsize=13)\n",
    "plt.title('ROC Curve - Brain Tumor Detection (One-vs-Rest)', fontsize=15)\n",
    "plt.legend(loc='lower right', fontsize=11)\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.tight_layout()\n",
    "plt.show()\n"
]

roc_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": roc_cell_source
}

nb['cells'].append(roc_cell)

with open('model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("ROC Curve cell added successfully.")
