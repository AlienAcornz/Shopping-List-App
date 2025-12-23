import React, { useState } from "react";

function AddNewItemForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: "",
    quantity: 0,
    unit: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  function handleSubmit(e) {
    e.preventDefault();

    const finalData = {
      name: formData.name || "",
      quantity: formData.quantity || "",
      unit: formData.unit || "null",
    };

    if (!finalData.name) return;
    onSubmit(finalData);
    setFormData({ name: "", quantity: "", unit: "" });
  }
  return (
    <div className="addNewItemForm">
      <form onSubmit={handleSubmit}>
        <label>Item Name:</label>
        <input
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          placeholder="e.g. Apples"
        ></input>

        <label>Quantity:</label>
        <input
          name="quantity"
          type="number"
          value={formData.quantity}
          onChange={handleChange}
          placeholder="e.g. 3"
        ></input>

        <label>Unit:</label>
        <input
          name="unit"
          type="text"
          value={formData.unit}
          onChange={handleChange}
          placeholder="e.g. kg"
        ></input>

        <button type="submit">Add Item</button>
      </form>
    </div>
  );
}

export default AddNewItemForm;
