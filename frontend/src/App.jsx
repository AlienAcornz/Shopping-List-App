import ListSelectionScreen from "./pages/ListSelectionScreen"
import ListScreen from "./pages/ListScreen"
import {Routes, Route} from "react-router-dom"

import "./css/App.css"

function App() {

  return (
    <main className="main-content">
        <Routes>
            <Route path="/" element={<ListSelectionScreen/>}/>
            <Route path="/list/:id" element={<ListScreen/>}/>
        </Routes>
    </main>
  )
}

export default App
