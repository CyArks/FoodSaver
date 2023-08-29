import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import FridgePage from './containers/FridgePage';
import RecipePage from './containers/RecipePage';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/fridge">Fridge</Link>
            </li>
            <li>
              <Link to="/recipes">Recipes</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/fridge">
            <FridgePage />
          </Route>
          <Route path="/recipes">
            <RecipePage />
          </Route>
          <Route path="/">
            <h1>Welcome to the Home Page!</h1>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
