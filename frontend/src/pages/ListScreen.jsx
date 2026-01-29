import { useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";

import backIcon from "../assets/arrow_forward.svg";
import "../css/ListScreen.css";
import shareIcon from "../assets/share.svg";
import ShoppingItemCard from "../components/ShoppingItemCard";
import AddNewItemForm from "../components/AddNewItemForm";
import { getPrice } from "../../services/api";

import { Link } from "react-router-dom";

function ListScreen({lists, setLists}) {
  const { id } = useParams();
  const numericId = parseInt(id, 10);

  const [showNewItem, setShowNewItem] = useState(false);

  const [showHiddenItems, setShowHiddenItems] = useState(true);

  const list = lists.find((l) => l.id === numericId);
  const listId = lists.findIndex((l) => l.id === numericId);

  const fetchPrices = async () => {
    list.list.forEach(async (item) => {
      const response = await getPrice(item.name);
      const price = response.price;
      const unit = response.unit;

      console.log(price, unit);

      const newList = [...lists];
      if (listId !== -1) {
        const itemId = newList[listId].list.findIndex(
          (i) => i.name === item.name
        );

        if (itemId !== -1) {
          const updatedItem = {
            ...newList[listId].list[itemId],
            price: price,
            unit: unit,
          };

          const updatedItems = [...newList[listId].list];
          updatedItems[itemId] = updatedItem;

          newList[listId] = {
            ...newList[listId],
            list: updatedItems,
          };

          setLists(newList);
        }
      }
    });
  };

  useEffect(() => {
    if (!showNewItem && lists.length !== 0) {
      fetchPrices();
    }
  }, []);

  function handleAddItem(e) {
    const newList = [...lists];
    if (listId !== -1) {
      newList[listId].list.push({
        id: newList[listId].list.length - 1,
        name: e.name,
        quantity: parseInt(e.quantity),
        unit: e.unit,
        isCompleted: false,
      });
      setLists(newList);
      setShowNewItem(false);
      fetchPrices();
    } else {
      console.log("List not found");
    }
  }

  const toggleHiddenItems = () => {
    setShowHiddenItems(!showHiddenItems);
  };

  const toggleCompleted = (item) => {
    item.isCompleted = !item.isCompleted;
    setLists(
      lists.map(
        (l) => (l.id === numericId ? { ...l, list: [...l.list] } : l) // updates the list to hold the isCompleted value
      )
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
        <img src={shareIcon} alt="Share the list" onClick={() => console.log(list)} />
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
              )
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
