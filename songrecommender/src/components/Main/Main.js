import React, { Component } from "react";
import NavBar from "../NavBar/NavBar";
import "./Main.css";
import Search from "../Search/Search";

class Main extends Component {
  render() {
    return (
      <div className="App">
        <NavBar />
        <div className="body">
          <div className="center">
            <h1 className="logo">LIKEMYSONG</h1>
            <Search />
          </div>
        </div>
      </div>
    );
  }
}

export default Main;
