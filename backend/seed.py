from models import Food, Recipe, State, User

DEMO_USER_ID = 1

STATES = [
    "Tamil Nadu",
    "Kerala",
    "Karnataka",
    "Andhra Pradesh",
    "Telangana",
    "Punjab",
    "Gujarat",
    "Rajasthan",
    "West Bengal",
    "Maharashtra",
]

FOODS = [
    {
        "state": "Tamil Nadu",
        "dish_name": "Idli Sambar",
        "meal_type": "breakfast",
        "description": "Steamed rice cakes served with lentil stew and coconut chutney.",
        "ingredients": "Idli rice, urad dal, fenugreek, toor dal, tamarind, sambar powder, vegetables, salt",
        "instructions": "Soak and grind idli batter, ferment overnight, steam in moulds. Cook sambar with dal, tamarind and vegetables. Serve hot with chutney.",
    },
    {
        "state": "Tamil Nadu",
        "dish_name": "Sambar Rice",
        "meal_type": "lunch",
        "description": "Comforting rice mixed with tangy sambar and vegetables.",
        "ingredients": "Rice, toor dal, tamarind, sambar powder, drumstick, carrot, onion, ghee",
        "instructions": "Cook rice and dal separately. Prepare sambar, mix with rice, finish with ghee and coriander.",
    },
    {
        "state": "Tamil Nadu",
        "dish_name": "Masala Dosa",
        "meal_type": "dinner",
        "description": "Crispy fermented crepe filled with spiced potato masala.",
        "ingredients": "Dosa batter, potatoes, onion, mustard seeds, curry leaves, turmeric, chilli",
        "instructions": "Spread thin dosa on a hot tawa, cook until crisp. Fill with potato masala and fold.",
    },
    {
        "state": "Kerala",
        "dish_name": "Puttu and Kadala",
        "meal_type": "breakfast",
        "description": "Steamed rice cylinders served with black chickpea curry.",
        "ingredients": "Rice flour, grated coconut, black chickpeas, coconut milk, spices",
        "instructions": "Layer rice flour and coconut in a puttu maker and steam. Serve with kadala curry.",
    },
    {
        "state": "Kerala",
        "dish_name": "Kerala Fish Curry",
        "meal_type": "lunch",
        "description": "Spicy coconut fish curry cooked in an earthen pot.",
        "ingredients": "Fish, coconut, kudampuli, chilli, turmeric, curry leaves, coconut oil",
        "instructions": "Grind coconut masala, simmer with kudampuli, add fish pieces and cook gently in coconut oil.",
    },
    {
        "state": "Kerala",
        "dish_name": "Appam with Stew",
        "meal_type": "dinner",
        "description": "Soft lacy hoppers paired with mild vegetable or chicken stew.",
        "ingredients": "Rice, coconut milk, yeast, mixed vegetables or chicken, pepper, coconut oil",
        "instructions": "Ferment appam batter and cook in an appachatti. Simmer stew in thin coconut milk until creamy.",
    },
    {
        "state": "Karnataka",
        "dish_name": "Ragi Mudde",
        "meal_type": "lunch",
        "description": "Finger millet balls usually eaten with sambar or bassaru.",
        "ingredients": "Ragi flour, water, salt, sambar or greens curry",
        "instructions": "Boil water with salt, mix ragi flour, cook into a dough and shape into balls. Serve with curry.",
    },
    {
        "state": "Karnataka",
        "dish_name": "Bisi Bele Bath",
        "meal_type": "lunch",
        "description": "Hot lentil-rice dish with vegetables and bisi bele bath powder.",
        "ingredients": "Rice, toor dal, mixed vegetables, tamarind, bisi bele bath powder, ghee",
        "instructions": "Cook rice, dal and vegetables together with spice powder. Temper with ghee, cashews and curry leaves.",
    },
    {
        "state": "Karnataka",
        "dish_name": "Mysore Masala Dosa",
        "meal_type": "dinner",
        "description": "Crisp dosa spread with red chutney and potato filling.",
        "ingredients": "Dosa batter, red chilli chutney, potato masala, butter",
        "instructions": "Spread dosa, smear red chutney, add potato filling and roast until crisp.",
    },
    {
        "state": "Andhra Pradesh",
        "dish_name": "Pesarattu",
        "meal_type": "breakfast",
        "description": "Green gram dosa often served with ginger chutney.",
        "ingredients": "Whole moong dal, rice, green chilli, ginger, onion, cumin",
        "instructions": "Soak and grind moong batter, spread on tawa, top with onion and cook both sides.",
    },
    {
        "state": "Andhra Pradesh",
        "dish_name": "Pulihora",
        "meal_type": "lunch",
        "description": "Tangy tamarind rice tempered with peanuts and spices.",
        "ingredients": "Cooked rice, tamarind, green chilli, peanuts, mustard, curry leaves, turmeric",
        "instructions": "Prepare tamarind paste, temper spices and peanuts, mix gently with cooled rice.",
    },
    {
        "state": "Andhra Pradesh",
        "dish_name": "Gongura Chicken",
        "meal_type": "dinner",
        "description": "Spicy Andhra chicken cooked with sour gongura leaves.",
        "ingredients": "Chicken, gongura leaves, red chilli, garlic, onion, oil",
        "instructions": "Cook chicken with spices, add sauteed gongura and simmer until thick and tangy.",
    },
    {
        "state": "Telangana",
        "dish_name": "Sarva Pindi",
        "meal_type": "breakfast",
        "description": "Savoury rice-flour pancake with peanuts and sesame.",
        "ingredients": "Rice flour, chana dal, peanuts, sesame, green chilli, onion, water",
        "instructions": "Mix a thick dough, flatten on a tawa with holes, and roast slowly with oil.",
    },
    {
        "state": "Telangana",
        "dish_name": "Hyderabadi Veg Biryani",
        "meal_type": "lunch",
        "description": "Layered fragrant rice with spiced vegetables and fried onions.",
        "ingredients": "Basmati rice, mixed vegetables, yogurt, biryani masala, saffron, mint, fried onion",
        "instructions": "Parboil rice, cook vegetable masala, layer both, and dum-cook until aromatic.",
    },
    {
        "state": "Telangana",
        "dish_name": "Mirchi ka Salan",
        "meal_type": "dinner",
        "description": "Hyderabadi chilli curry in a peanut-sesame gravy.",
        "ingredients": "Large green chillies, peanuts, sesame, coconut, tamarind, spices",
        "instructions": "Fry chillies, grind peanut-sesame masala, simmer into a thick gravy and add chillies.",
    },
    {
        "state": "Punjab",
        "dish_name": "Aloo Paratha",
        "meal_type": "breakfast",
        "description": "Stuffed whole-wheat flatbread with spiced potato.",
        "ingredients": "Wheat flour, potatoes, chilli, coriander, cumin, ghee",
        "instructions": "Stuff dough balls with potato mix, roll and cook on a tawa with ghee.",
    },
    {
        "state": "Punjab",
        "dish_name": "Sarson da Saag",
        "meal_type": "lunch",
        "description": "Slow-cooked mustard greens served with makki di roti.",
        "ingredients": "Mustard greens, spinach, maize flour, onion, garlic, ghee",
        "instructions": "Boil greens, mash with maize flour, simmer, and temper with onion-garlic ghee.",
    },
    {
        "state": "Punjab",
        "dish_name": "Butter Paneer",
        "meal_type": "dinner",
        "description": "Creamy tomato gravy with paneer cubes.",
        "ingredients": "Paneer, tomato, butter, cream, kasuri methi, garam masala",
        "instructions": "Make a smooth tomato-butter gravy, add paneer and finish with cream.",
    },
    {
        "state": "Gujarat",
        "dish_name": "Khaman Dhokla",
        "meal_type": "breakfast",
        "description": "Soft steamed gram-flour snack with a mustard tempering.",
        "ingredients": "Besan, lemon, sugar, eno, mustard seeds, green chilli, curry leaves",
        "instructions": "Steam spiced besan batter, temper with mustard and chilli, garnish with coriander.",
    },
    {
        "state": "Gujarat",
        "dish_name": "Thepla",
        "meal_type": "lunch",
        "description": "Spiced fenugreek flatbread that travels well.",
        "ingredients": "Wheat flour, methi leaves, yoghurt, turmeric, chilli powder, oil",
        "instructions": "Knead methi dough, roll thin theplas, and cook on a tawa with a little oil.",
    },
    {
        "state": "Gujarat",
        "dish_name": "Undhiyu",
        "meal_type": "dinner",
        "description": "Mixed winter vegetable casserole cooked with muthiya.",
        "ingredients": "Surti papdi, potato, brinjal, banana, muthiya, coconut, spices",
        "instructions": "Layer vegetables and muthiya with masala and slow-cook until tender.",
    },
    {
        "state": "Rajasthan",
        "dish_name": "Dal Baati",
        "meal_type": "lunch",
        "description": "Baked wheat balls served with spiced dal and ghee.",
        "ingredients": "Wheat flour, ghee, panchmel dal, chilli, turmeric, cumin",
        "instructions": "Bake or roast baati until golden. Serve cracked open with ghee and hot dal.",
    },
    {
        "state": "Rajasthan",
        "dish_name": "Gatte ki Sabzi",
        "meal_type": "dinner",
        "description": "Gram-flour dumplings in a yoghurt gravy.",
        "ingredients": "Besan, yoghurt, cumin, chilli, turmeric, ghee",
        "instructions": "Boil gatte, slice them, and simmer in a tempered yoghurt gravy.",
    },
    {
        "state": "West Bengal",
        "dish_name": "Luchi and Aloo Dum",
        "meal_type": "breakfast",
        "description": "Fluffy fried bread with spicy potato curry.",
        "ingredients": "Maida, oil, potatoes, tomato, cumin, chilli, turmeric",
        "instructions": "Roll and fry luchis. Cook baby potatoes in a thick Bengali-style gravy.",
    },
    {
        "state": "West Bengal",
        "dish_name": "Shukto",
        "meal_type": "lunch",
        "description": "Mild bitter-sweet mixed vegetable stew.",
        "ingredients": "Bitter gourd, potato, drumstick, milk, poppy paste, mustard, ghee",
        "instructions": "Fry vegetables lightly, simmer with poppy-mustard paste and finish with milk and ghee.",
    },
    {
        "state": "West Bengal",
        "dish_name": "Machher Jhol",
        "meal_type": "dinner",
        "description": "Light Bengali fish curry with potatoes.",
        "ingredients": "Rohu or catla, potato, turmeric, cumin, chilli, mustard oil",
        "instructions": "Marinate and fry fish, cook a thin cumin-chilli gravy, and simmer fish gently.",
    },
    {
        "state": "Maharashtra",
        "dish_name": "Poha",
        "meal_type": "breakfast",
        "description": "Flattened rice tempered with mustard, onion and peanuts.",
        "ingredients": "Thick poha, onion, mustard, turmeric, peanuts, lemon, coriander",
        "instructions": "Rinse poha, temper spices and onion, toss poha until fluffy, finish with lemon.",
    },
    {
        "state": "Maharashtra",
        "dish_name": "Misal Pav",
        "meal_type": "lunch",
        "description": "Spicy sprouted-bean curry topped with farsan and pav.",
        "ingredients": "Matki sprouts, goda masala, onion, farsan, pav, lemon",
        "instructions": "Cook misal gravy, add sprouts, serve with farsan, onion and pav.",
    },
    {
        "state": "Maharashtra",
        "dish_name": "Pav Bhaji",
        "meal_type": "dinner",
        "description": "Mashed vegetable curry served with buttered pav.",
        "ingredients": "Potato, tomato, mixed vegetables, pav bhaji masala, butter, pav",
        "instructions": "Mash cooked vegetables with masala and butter. Toast pav and serve with onion and lemon.",
    },
]


def seed_if_empty(db):
    if db.query(State).count() == 0:
        db.add_all([State(name=name) for name in STATES])

    if db.query(Food).count() == 0:
        for item in FOODS:
            food = Food(
                state=item["state"],
                dish_name=item["dish_name"],
                meal_type=item["meal_type"],
                description=item["description"],
            )
            db.add(food)
            db.flush()
            db.add(
                Recipe(
                    food_id=food.id,
                    dish_name=item["dish_name"],
                    ingredients=item["ingredients"],
                    instructions=item["instructions"],
                )
            )

    db.commit()
