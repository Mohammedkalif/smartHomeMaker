export default function FoodSuggestions({ foods = [], onSelect, selectedId }) {
  return (
    <div className="food-list">
      {foods.length === 0 && <p className="muted">No dishes found for this filter.</p>}
      {foods.map((food) => (
        <button
          key={food.id}
          type="button"
          className="food-item"
          style={{
            textAlign: "left",
            background: selectedId === food.id ? "#efe7db" : "white",
            color: "inherit",
            borderColor: selectedId === food.id ? "#2e5c45" : undefined,
          }}
          onClick={() => onSelect(food)}
        >
          <strong>{food.dish_name}</strong>
          <div className="muted">
            {food.state && `${food.state} · `}{food.meal_type || "AI recipe"}
          </div>
          <p>{food.description}</p>
        </button>
      ))}
    </div>
  );
}
