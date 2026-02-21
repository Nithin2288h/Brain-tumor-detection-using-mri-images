import json

notebook_path = 'model.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cell_source = [
    "# Classification Report & Confusion Matrix\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "import seaborn as sns\n",
    "\n",
    "# Predict on test set\n",
    "y_pred = np.argmax(model.predict(X_test), axis=1)\n",
    "\n",
    "# Classification Report\n",
    "print(\"Classification Report:\")\n",
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

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": new_cell_source
}

nb['cells'].append(new_cell)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("✅ Classification Report & Confusion Matrix cell added successfully!")
