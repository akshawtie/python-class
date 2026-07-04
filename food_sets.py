PROTEIN_RICH_FOODS = {
	"chicken",
	"eggs",
	"fish",
	"greek yogurt",
	"lentils",
	"tofu",
}

WELL_BALANCED_FOODS = {
	"brown rice and chicken",
	"salad with beans",
	"oats with fruit",
	"whole grain sandwich",
	"vegetable stir fry",
	"yogurt with nuts",
}

BOOSTER_FOODS = {
	"banana",
	"peanut butter",
	"spinach",
	"sweet potato",
	"almonds",
	"berries",
}


def get_food_sets() -> dict[str, set[str]]:
	return {
		"Protein Rich Foods": PROTEIN_RICH_FOODS,
		"Well Balanced Foods": WELL_BALANCED_FOODS,
		"Booster Foods": BOOSTER_FOODS,
	}