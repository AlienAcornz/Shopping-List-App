import { useState } from "react";

import addIcon from "../assets/add.svg";
import "../css/ListSelectionScreen.css";
import ShoppingListCard from "../components/ShoppingListCard";

function ListSelectionScreen() {
  const [showNewList, setShowNewList] = useState(false);
  const [lists, setLists] = useState([
    { id: 0, name: "Weekly Shop", isShared: false },
    { id: 1, name: "Shared List", isShared: true },
    { id: 2, name: "Party food", isShared: true },
  ]);
  const [newName, setNewName] = useState("");
  const [newShared, setNewShared] = useState(false);

  const handleSubmit = () => {
    const newList = {
      id: lists.length,
      name: newName || "Untitled List",
      isShared: newShared,
      list: [],
    };
        setLists([...lists, newList])
        setShowNewList(false)
        setNewName("")
        setNewShared(false)
  };

  return (
    <div>
      <div>
        {lists.map((list) => (
          <ShoppingListCard shoppingList={list} key={list.id} />
        ))}
        <div className="newListButton" onClick={() => setShowNewList(true)}>
          <img src={addIcon} alt="Add a new list" />
        </div>
      </div>

      {showNewList && (
        <div className="popupModal" onClick={() => setShowNewList(false)}>
          <div className="newListDiv" onClick={(e) => e.stopPropagation()}>
            <h2>Create New List</h2>
            <form onSubmit={(e) => e.preventDefault()}>
              <div className="panel">
                <input
                  type="text"
                  id="nameBox"
                  name="listName"
                  placeholder="List Name:"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                />
              </div>
              <div className="panel">
                <p>Shared list?</p>
                <div className="spacer" />
                <input
                  type="checkbox"
                  checked={newShared}
                  onChange={(e) => setNewShared(e.target.checked)}
                />
              </div>
              <div className="finishButtons">
                <div className="cancel" onClick={() => setShowNewList(false)}>
                  <p>Cancel</p>
                </div>
                <div className="spacer" />
                <div className="submit" onClick={handleSubmit}>
                  <p>Submit</p>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default ListSelectionScreen;
