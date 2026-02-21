import json

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and replace the ROC curve cell (last cell)
last_cell = nb['cells'][-1]
src = ''.join(last_cell['source'])

if 'roc_curve' in src or 'ROC' in src:
    last_cell['source'] = [
        "%matplotlib inline\n",
        "\n",
        "# ROC Curve (One-vs-Rest for Multiclass)\n",
        "from sklearn.preprocessing import label_binarize\n",
        "from sklearn.metrics import roc_curve, auc\n",
        "import matplotlib\n",
        "import matplotlib.pyplot as plt\n",
        "import numpy as np\n",
        "\n",
        "# Binarize the labels for one-vs-rest\n",
        "y_test_bin = label_binarize(y_test, classes=[0, 1, 2, 3])\n",
        "y_score = model.predict(X_test)  # predicted probabilities\n",
        "\n",
        "colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(10, 7))\n",
        "\n",
        "for i, (class_name, color) in enumerate(zip(classes, colors)):\n",
        "    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])\n",
        "    roc_auc = auc(fpr, tpr)\n",
        "    ax.plot(fpr, tpr, color=color, lw=2,\n",
        "             label=f'{class_name} (AUC = {roc_auc:.2f})')\n",
        "\n",
        "ax.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Random Classifier')\n",
        "ax.set_xlim([0.0, 1.0])\n",
        "ax.set_ylim([0.0, 1.05])\n",
        "ax.set_xlabel('False Positive Rate', fontsize=13)\n",
        "ax.set_ylabel('True Positive Rate', fontsize=13)\n",
        "ax.set_title('ROC Curve - Brain Tumor Detection (One-vs-Rest)', fontsize=15)\n",
        "ax.legend(loc='lower right', fontsize=11)\n",
        "ax.grid(True, linestyle='--', alpha=0.5)\n",
        "plt.tight_layout()\n",
        "plt.savefig('roc_curve.png', dpi=100)\n",
        "plt.show()\n",
        "print('ROC Curve plotted and saved as roc_curve.png')\n"
    ]
    print("ROC cell updated with %matplotlib inline.")
else:
    print("ROC cell not found in last position.")

with open('model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Saved.")
