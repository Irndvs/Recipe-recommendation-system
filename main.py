import json
import pandas as pd

# Load the JSON file
def load_recipes(file_path):
    """
    Load recipes data from a JSON file and convert it into a DataFrame.
    
    Parameters:
    file_path (str): Path to the JSON file containing recipes data.
    
    Returns:
    DataFrame: A cleaned DataFrame with recipes information.
    """
    with open(file_path, 'r') as f:
        recipes_data = json.load(f)

    # Convert JSON data into a DataFrame
    recipes_list = []
    for recipe in recipes_data:
        # Flattening the nested structure
        basic_info = recipe.get('basic_info', {})
        prep_data = recipe.get('prep_data', {})
        ingredients = recipe.get('ingridients', [])
        nutrition = recipe.get('nutritions', {})

        rating = basic_info.get('rating', 'N/A')
        if rating is not None:
            rating = str(rating).strip()

        reviews = basic_info.get('reviews', 'N/A')
        if reviews is not None:
            reviews = str(reviews).strip()

        recipes_list.append({
            'Title': basic_info.get('title', 'N/A'),
            'Category': basic_info.get('category', 'N/A'),
            'Rating': rating,
            'Reviews': reviews,
            'Prep Time': prep_data.get('prep_time:', 'N/A'),
            'Cook Time': prep_data.get('cook_time:', 'N/A'),
            'Total Time': prep_data.get('total_time:', 'N/A'),
            'Servings': prep_data.get('servings:', 'N/A'),
            'Ingredients': ', '.join(ingredients),
            'Calories': nutrition.get('calories', 'N/A'),
        })

    # Create and clean DataFrame
    recipes_df = pd.DataFrame(recipes_list)
    recipes_df['Rating'] = pd.to_numeric(recipes_df['Rating'], errors='coerce')
    recipes_df['Calories'] = pd.to_numeric(recipes_df['Calories'], errors='coerce')
    recipes_df['Category'] = recipes_df['Category'].fillna('Unknown')
    recipes_df['Reviews'] = recipes_df['Reviews'].fillna('0 Reviews')

    return recipes_df


# Define the recommend_recipes function
def recommend_recipes(available_ingredients, df):
    """
    Recommend recipes based on available ingredients.

    Parameters:
    available_ingredients (list): List of ingredients the user has.
    df (DataFrame): The recipes DataFrame.

    Returns:
    DataFrame: Matching recipes sorted by rating.
    """
    # Filter recipes containing at least one ingredient from the user's list
    matching_recipes = df[df['Ingredients'].apply(
        lambda x: any(ingredient.lower() in x.lower() for ingredient in available_ingredients)
    )]

    # Sort by rating
    matching_recipes['Rating'] = matching_recipes['Rating'].astype(float)
    return matching_recipes.sort_values(by='Rating', ascending=False)


# Example usage
if __name__ == "__main__":
    # Path to your JSON file
    file_path = r"C:\Users\irind\Downloads\allrecipes-complete-recipes-list-by-dmitriy-zub.json\allrecipes-complete-recipes-list-by-dmitriy-zub.json"
    
    # Load the recipes dataset
    recipes_df = load_recipes(file_path)
    
    # Display basic information about the dataset
    print("Dataset Info:")
    print(recipes_df.info())
    print("\nTop 5 Recipes by Rating:")
    print(recipes_df[['Title', 'Rating', 'Ingredients']].head())

    # Example user input
    user_ingredients = ['chicken', 'onion', 'garlic']
    recommended = recommend_recipes(user_ingredients, recipes_df)
    print("\nRecommended Recipes:")
    print(recommended[['Title', 'Rating', 'Ingredients']])
from main import recommend_recipes, load_recipes

# Dummy data for testing
test_ingredients = ['chicken', 'onion', 'garlic']
test_recipes_df = load_recipes("path_to_your_json_file.json")

print(recommend_recipes(test_ingredients, test_recipes_df))
