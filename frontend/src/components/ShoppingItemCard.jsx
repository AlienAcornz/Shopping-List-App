import "../css/ShoppingItemCard.css"

function ShoppingItemCard({ Item, onToggleCompleted }) {

  return (
    <div className="itemCard" onClick={() => onToggleCompleted(Item)}> 
      <div className="itemInfo">
        <input type="checkbox" checked={Item.isCompleted} onChange={(e) => e.stopPropagation()}/>
        {
        isNaN(Item.quantity)
          ? <p>{Item.name}</p>
          : (
              Item.unit
                ? <p>{Item.name} • {Item.quantity} {Item.unit}</p>
                : <p>{Item.name} • {Item.quantity}</p>
            )
      }

        
      </div>
      {Item.price ? <p>£{Item.price.toFixed(2)}</p> : <p>----</p>}
    </div>
  );
}

export default ShoppingItemCard

