import streamlit as st
from main import load_recipes, recommend_recipes
import sys
sys.path.append(r"C:\Users\irind\OneDrive\Desktop\Genai_project\main.py")
from main import recommend_recipes, load_recipes

# Set page title
st.title("Recipe Recommendation System")

# Load the dataset (update the file path as needed)
file_path = r"C:\Users\irind\Downloads\allrecipes-complete-recipes-list-by-dmitriy-zub.json\allrecipes-complete-recipes-list-by-dmitriy-zub.json"

st.sidebar.header("Configuration")
if "recipes_df" not in st.session_state:
    try:
        recipes_df = load_recipes(file_path)
        st.session_state.recipes_df = recipes_df
        st.sidebar.success("Dataset loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to load dataset: {e}")
        st.stop()

# User input for ingredients
st.sidebar.header("Search Recipes")
user_ingredients = st.sidebar.text_input("Enter your ingredients (comma-separated):")

# Recommend recipes based on input
if user_ingredients:
    ingredients_list = [x.strip() for x in user_ingredients.split(',')]
    try:
        recommendations = recommend_recipes(ingredients_list, st.session_state.recipes_df)
        if not recommendations.empty:
            st.write(f"## Recommended Recipes ({len(recommendations)} found)")
            for idx, row in recommendations.iterrows():
                st.write(f"### {row['Title']}")
                st.write(f"**Category:** {row['Category']}")
                st.write(f"**Rating:** {row['Rating']}")
                st.write(f"**Reviews:** {row['Reviews']}")
                st.write(f"**Ingredients:** {row['Ingredients']}")
                st.write("---")
        else:
            st.write("No matching recipes found. Try different ingredients.")
    except Exception as e:
        st.error(f"An error occurred while recommending recipes: {e}")
else:
    st.write("Enter some ingredients to find matching recipes!")
