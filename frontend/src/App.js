import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import FridgePage from './containers/FridgePage';
import RecipePage from './containers/RecipePage';
import CreateRecipeComponent from './components/CreateRecipeComponent';
import ListRecipesComponent from './components/ListRecipesComponent';
import LoginComponent from './components/LoginComponent';
import ProfileComponent from './components/ProfileComponent';
import GroceryListComponent from './components/GroceryListComponent';
import MealPlanComponent from './components/MealPlanComponent';
import SavingsFinder from './components/SavingsFinder';

function App() {
  return (
    <Router>
      <div>
        <nav>
          {/* Add your navigation links here */}
          <Link to="/fridge">Fridge</Link>
          <Link to="/recipes">Recipes</Link>
          {/* ... */}
        </nav>

        <Switch>
          {/* Fridge Page */}
          <Route path="/fridge">
            <FridgePage />
          </Route>

          {/* Recipe Page */}
          <Route path="/recipes">
            <RecipePage />
          </Route>

          {/* Create Recipe */}
          <Route path="/create-recipe">
            <CreateRecipeComponent />
          </Route>

          {/* List Recipes */}
          <Route path="/list-recipes">
            <ListRecipesComponent />
          </Route>

          {/* Login */}
          <Route path="/login">
            <LoginComponent />
          </Route>

          {/* Profile */}
          <Route path="/profile">
            <ProfileComponent />
          </Route>

          {/* Grocery List */}
          <Route path="/grocery-list">
            <GroceryListComponent />
          </Route>

          {/* Meal Plan */}
          <Route path="/meal-plan">
            <MealPlanComponent />
          </Route>

          {/* Savings Finder */}
          <Route path="/savings-finder">
            <SavingsFinder />
          </Route>

          {/* Add more routes as you implement them */}
        </Switch>
      </div>
    </Router>
  );
}

export default App;
