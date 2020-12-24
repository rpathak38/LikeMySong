import React from "react";
import { Navbar, Nav } from "react-bootstrap";

export default (props) => {
  return (
    <Navbar bg="success" variant="dark">
      <Navbar.Brand href="#home">Navbar</Navbar.Brand>
      <Nav className="mr-auto">
        <Nav.Link href="#home">Home</Nav.Link>
        <Nav.Link href="#Link 2">Link 2</Nav.Link>
        <Nav.Link href="#About Us">About Us</Nav.Link>
      </Nav>
    </Navbar>
  );
};
