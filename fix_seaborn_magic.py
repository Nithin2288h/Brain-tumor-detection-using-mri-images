import json

with open('model.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

last_cell = nb['cells'][-1]
src = ''.join(last_cell['source'])

if 'classification_report' in src:
    last_cell['source'] = [
        "!pip install seaborn -q\n",
        "\n",
        "# Classification Report & Confusion Matrix\n",
        "from sklearn.metrics import classification_report, confusion_matrix\n",
        "import seaborn as sns\n",
        "\n",
        "# Predict on test set\n",
        "y_pred = np.argmax(model.predict(X_test), axis=1)\n",
        "\n",
        "# Classification Report\n",
        "print('Classification Report:')\n",
        "print(classification_report(y_test, y_pred, target_names=classes))\n",
        "\n",
        "# Confusion Matrix\n",
        "cm = confusion_matrix(y_test, y_pred)\n",
        "plt.figure(figsize=(8, 6))\n",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',\n",
        "            xticklabels=classes, yticklabels=classes)\n",
        "plt.title('Confusion Matrix')\n",
        "plt.xlabel('Predicted')\n",
        "plt.ylabel('Actual')\n",
        "plt.tight_layout()\n",
        "plt.show()\n"
    ]
    print("Cell updated with !pip install seaborn magic command.")
else:
    print("Classification cell not found.")

with open('model.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Saved successfully.")
