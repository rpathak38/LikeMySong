import React, { Component } from 'react'
import "./Search.css";

class Search extends Component {
 state = {
   query: '',
 }

 handleInputChange = () => {
   this.setState({
     query: this.search.value
   })
 }

 render() {
   return (
     <form>
       <input
         placeholder="Start Typing..."
         ref={input => this.search = input}
         onChange={this.handleInputChange}
         className="search"
       />
       <p>{this.state.query}</p>
     </form>
   )
 }
}

export default Search