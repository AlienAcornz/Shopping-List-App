import shareIcon from "../assets/Users.svg"
import openIcon from "../assets/arrow_forward.svg"
import "../css/ShoppingListCard.css"
import { Link } from "react-router-dom";


function ShoppingListCard({shoppingList}) {
    return (
        <Link 
            to={`/list/${shoppingList.id}`} 
            style={{ textDecoration: "none", color: "inherit" }}
        >
        <div className="listCard">
            <h2>{shoppingList.name}</h2>
            {shoppingList.isShared === true && <img src={shareIcon} alt="Shared users icon"/>}
            <div className="spacer"/>
            <img src={openIcon} alt="Enter list icon"/>
        </div>
        </Link>
    )
}

export default ShoppingListCard