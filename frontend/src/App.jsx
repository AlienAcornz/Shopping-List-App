import ListSelectionScreen from "./pages/ListSelectionScreen"
import ListScreen from "./pages/ListScreen"
import {Routes, Route} from "react-router-dom"
import React, { useState, useEffect } from "react";
import "./css/App.css"

function App() {

  const [lists, setLists] = useState([
    {
      id: 0,
      name: "Weekly Shop",
      token: "0",
      list: [
        {
          id: 0,
          name: "banana",
          quantity: 1,
          unit: "litre",
          isCompleted: false,
        },
        { id: 1, name: "Eggs", quantity: 6, unit: "each", isCompleted: true },
      ],
    },
    {
      id: 1,
      name: "Shared list",
      token: "THISISAFAKETOKEN",
      list: [
        { id: 0, name: "Cheese", quantity: 7, unit: "kg", isCompleted: false },
        { id: 1, name: "Bread", quantity: 2, unit: "kg", isCompleted: false },
      ],
    },
    {
      id: 2,
      name: "Party food",
      token: "0",
      list: [
        { id: 0, name: "Pizza", quantity: 7, unit: "each", isCompleted: false },
        {
          id: 1,
          name: "cucumber",
          quantity: 2,
          unit: "kg",
          isCompleted: false,
        },
      ],
    },
  ]);

  return (
    <main className="main-content">
        <Routes>
            <Route path="/" element={<ListSelectionScreen lists={lists} setLists={setLists}/>}/>
            <Route path="/list/:id" element={<ListScreen lists={lists} setLists={setLists}/>}/>
        </Routes>
    </main>
  )
}

export default App
