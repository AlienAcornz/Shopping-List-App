import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";

import backIcon from "../assets/arrow_forward.svg";
import "../css/ListScreen.css";
import shareIcon from "../assets/share.svg";
import ShoppingItemCard from "../components/ShoppingItemCard";
import AddNewItemForm from "../components/AddNewItemForm";
import { getPrice } from "../../services/api";

import { Link } from "react-router-dom";

function ListScreen({ lists, setLists }) {
  const { id } = useParams();
  const numericId = parseInt(id, 10);

  const [showNewItem, setShowNewItem] = useState(false);

  const [showHiddenItems, setShowHiddenItems] = useState(true);

  const list = lists.find((l) => l.id === numericId);
  const listId = lists.findIndex((l) => l.id === numericId);

  // 1. Normalization map
  const unitMap = {
    gram: "g",
    grams: "g",
    g: "g",

    kilogram: "kg",
    kilograms: "kg",
    kg: "kg",

    litre: "l",
    liter: "l",
    litres: "l",
    liters: "l",
    l: "l",

    millilitre: "ml",
    milliliter: "ml",
    millilitres: "ml",
    milliliters: "ml",
    ml: "ml",

    centilitre: "cl",
    centiliter: "cl",
    centilitres: "cl",
    centiliters: "cl",
    cl: "cl",

    each: "each",
  };

  function normalizeUnit(input) {
    if (!input) return null;
    const key = input.trim().toLowerCase();
    return unitMap[key] || null;
  }

  const fetchPrices = async (itemsToPrice) => {
    if (!itemsToPrice || itemsToPrice.length === 0) return;

    try {
      const responses = await Promise.all(
        itemsToPrice.map((item) => {
          const normalizedUnit = normalizeUnit(item.unit);

          if (!normalizedUnit) return null;

          return getPrice(item.name, item.quantity, normalizedUnit);
        }),
      );

      const updatedItems = itemsToPrice.map((item, index) => {
        const response = responses[index];

        if (!response || !response.price) {
          return item;
        }

        return {
          ...item,
          price: response.price * item.quantity,
          unit: normalizeUnit(item.unit),
        };
      });

      setLists((prevLists) =>
        prevLists.map((l) =>
          l.id === numericId ? { ...l, list: updatedItems } : l,
        ),
      );
    } catch (error) {
      console.error("Price fetch failed:", error);
    }
  };

  useEffect(() => {
    if (list?.list?.length > 0) {
      fetchPrices(list.list);
    }
  }, []);

  function handleAddItem(e) {
  const newItem = {
    id: Date.now(),
    name: e.name,
    quantity: Math.abs(parseInt(e.quantity)),
    unit: e.unit && e.unit !== "null" ? e.unit : null,
    isCompleted: false,
  };

  const updatedList = list ? [...list.list, newItem] : [newItem];

  setLists((prevLists) =>
    prevLists.map((l) =>
      l.id === numericId ? { ...l, list: updatedList } : l
    )
  );

  setShowNewItem(false);

  // Fetch prices using the updated list directly
  fetchPrices(updatedList);
}

  const toggleHiddenItems = () => {
    setShowHiddenItems(!showHiddenItems);
  };

  const toggleCompleted = (item) => {
    item.isCompleted = !item.isCompleted;
    setLists(
      lists.map(
        (l) => (l.id === numericId ? { ...l, list: [...l.list] } : l), // updates the list to hold the isCompleted value
      ),
    );
  };

  if (!list) return <p>List not found</p>;

  return (
    <div>
      <div className="navigationBar">
        <Link to="/" style={{ textDecoration: "none", color: "inherit" }}>
          <img
            src={backIcon}
            alt="Go back to main screen"
            style={{ transform: "scaleX(-1)" }}
          />
        </Link>

        <p>{list.name}</p>
        <img
          src={shareIcon}
          alt="Share the list"
          onClick={() => console.log(list)}
        />
      </div>
      <div className="background">
        <div>
          <p
            onClick={toggleHiddenItems}
            style={{
              cursor: "pointer",
              textDecoration: !showHiddenItems ? "line-through" : "none",
            }}
          >
            Show hidden items?
          </p>
        </div>
        <div>
          {list.list.map(
            (item) =>
              (!item.isCompleted || showHiddenItems) && (
                <ShoppingItemCard
                  Item={item}
                  key={item.id}
                  onToggleCompleted={(i) => toggleCompleted(i)}
                />
              ),
          )}
        </div>
        <div className="newItemButton" onClick={() => setShowNewItem(true)}>
          {showNewItem ? (
            <AddNewItemForm onSubmit={handleAddItem} />
          ) : (
            <p style={{ cursor: "pointer" }}> + Add Item</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ListScreen;
