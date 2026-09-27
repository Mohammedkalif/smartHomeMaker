import { useEffect, useState } from "react";
import FoodSuggestions from "../components/FoodSuggestions";
import { getAIFoodSuggestions, getProfile } from "../api";

export default function Food() {
  const [profile, setProfile] = useState(null);
  const [state, setState] = useState("");
  const [mealType, setMealType] = useState("dinner");
  const [foods, setFoods] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { getProfile().then((data) => { setProfile(data); setState(data.state); }).catch(() => {}); }, []);
  async function findIdeas(event) {
    event?.preventDefault();
    if (!state) return;
    setLoading(true); setError(""); setSelected(null);
    try { const data = await getAIFoodSuggestions({ state, meal_type: mealType, language: profile?.language || "English" }); setFoods(data.dishes || []); }
    catch (err) { setFoods([]); setError(err.message); }
    finally { setLoading(false); }
  }
  if (!profile) return <div className="card">Loading food ideas...</div>;
  return <div className="food-page"><div className="page-heading"><p className="eyebrow">AI KITCHEN PLANNER</p><h1>Food ideas made for your table.</h1><p>Choose your region and meal. Your AI assistant will create several complete recipe ideas.</p></div><form className="card food-filters" onSubmit={findIdeas}>
    <div><label htmlFor="state">State</label><select id="state" value={state} onChange={(event) => setState(event.target.value)}>{profile.states.map((item) => <option key={item}>{item}</option>)}</select></div>
    <div><label htmlFor="meal">Meal type</label><select id="meal" value={mealType} onChange={(event) => setMealType(event.target.value)}><option value="breakfast">Breakfast</option><option value="lunch">Lunch</option><option value="dinner">Dinner</option><option value="snack">Snack</option></select></div>
    <button type="submit" disabled={loading}>{loading ? "Creating ideas..." : "Get AI ideas"}</button>
  </form>{error && <p className="error">{error}</p>}
  {!foods.length && !loading && !error && <div className="empty-state card">Select your preferences and let the AI plan a delicious meal.</div>}
  {foods.length > 0 && <div className="food-results"><div className="card"><h2>Choose a dish</h2><FoodSuggestions foods={foods} onSelect={setSelected} selectedId={selected?.id} /></div><div className="card recipe-card"><h2>Recipe</h2>{!selected ? <p className="muted">Select one of the AI suggestions to see its full recipe.</p> : <><h3>{selected.dish_name}</h3><p>{selected.description}</p><h4>Ingredients</h4><ul>{selected.ingredients.map((item, index) => <li key={index}>{item}</li>)}</ul><h4>Instructions</h4><ol>{selected.instructions.map((item, index) => <li key={index}>{item}</li>)}</ol></>}</div></div>}
  </div>;
}
