import "../css/ShoppingItemCard.css"

function ShoppingItemCard({ Item, onToggleCompleted }) {

  return (
    <div className="itemCard" onClick={() => onToggleCompleted(Item)}> 
      <div className="itemInfo">
        <input type="checkbox" checked={Item.isCompleted} onChange={(e) => e.stopPropagation()}/>
        <p>{Item.name} • {Item.quantity} {Item.unit}</p>
      </div>
      {Item.price ? <p>£{Item.price}</p> : <p>----</p>}
    </div>
  );
}

export default ShoppingItemCard

