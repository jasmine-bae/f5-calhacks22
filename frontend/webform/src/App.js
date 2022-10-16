import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import InitialForm from './components/InitialForm';
import SelectForm from './components/SelectForm';
import './App.css';

function App() {
    console.log("hi");
    return (
        <div className="App">
            <Router>
                <Switch>
                    <Route path="/f2">
                        <SelectForm />
                    </Route>
                    <Route path="/">
                        <InitialForm />
                    </Route>
                    <Route path="/answer">
                    </Route>

                </Switch>
            </Router>
        </div>
    );
}

export default App;